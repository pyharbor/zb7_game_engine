from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from collections import defaultdict
from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature
from zb7_game_engine.runtime.objects.base.BaseRecruit import BaseRecruit
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus
from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.StateSet import StateSet
from typing import List, TYPE_CHECKING, Union
from zb7_game_engine.runtime.core.StackItem import StackItem
from zb7_game_engine.serialization.animation_events.Animations import Animations
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer
from zb7_game_engine.runtime.core.Listeners import Listeners
from zb7_game_engine.serialization.animation_events.Animations import Animations
from zb7_game_engine.runtime.core.RandomEngine import random_engine
from zb7_game_engine.serialization.animation_events.G.Group import Group
from zb7_game_engine.runtime.objects.statuses.Statuses import Statuses
from zb7_game_engine.serialization.shared.custom_data.ShopIDTarget import ShopIDTarget
from zb7_game_engine.runtime.core.ObjectParser import ObjectParser
from zb7_game_engine.serialization.shared.custom_data.SuperNestCD import SuperNestCD
from zb7_game_engine.serialization.shared.custom_data.Rewards import Rewards


if TYPE_CHECKING:
    from zb7_game_engine.serialization.ShopStateSerializer import ShopStateSerializer
    from zb7_game_engine.serialization.BattleStateSerializer import BattleStateSerializer
    from zb7_game_engine.runtime.core.StackItem import StackItem
    from zb7_game_engine.runtime.core.StateSet import StateSet
    from zb7_game_engine.runtime.core.shop_opcodes.ShopUserInput import ShopUserInput
    from zb7_game_engine.serialization.BattleSnapshotSerializer import BattleSnapshotSerializer
    from zb7_game_engine.serialization.ShopSnapshotSerializer import ShopSnapshotSerializer
    from zb7_game_engine.serialization.RelicSerializer import RelicSerializer
    from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
    from zb7_game_engine.serialization.StatusSerializer import StatusSerializer


class CrystalBall(RelicSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=165,
                         sub_type_as_text="CrystalBall", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def shop_start_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                           animation_event_sequence: AnimationEventSequence):
        self.generic_ability_notification(
            state=shop_state,
            state_set=state_set,
            animation_event_sequence=animation_event_sequence)
        g = Group()
        g2 = Group()
        for x in shop_state.friendly_recruits:
            if x.type == "EmptySlot":
                continue
            x.experience += 1
            shop_state.queue_ability_for(trigger=GameConstants.Opcodes.Shop.shop_gain_experience,
                                         objects=[x],
                                         context={})
            if x.experience in GameConstants.Levels.all:
                g2.add_animation_event(
                    Animations.ShopLevelUp(
                        shop_id=x.shop_id,
                        battle_id=x.battle_id,
                        amount=1,
                        state_id=None
                    )
                )
                shop_state.queue_ability_for(objects=[x],
                                             trigger=GameConstants.Opcodes.Shop.shop_level_up,
                                             context={"recruit": x})
            e = Animations.ShopGainExperience(
                shop_id=x.shop_id,
                battle_id=x.battle_id,
                amount=1,
                state_id=None
            )
            g.add_animation_event(e)
        if len(g.animation_events) > 0:
            g.set_state_id(state_id=state_set.add_state(state=shop_state))
            g2.set_state_id(state_id=state_set.add_state(state=shop_state))
            animation_event_sequence.append(g)
            animation_event_sequence.append(g2)

