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


class AmberAmulet(RelicSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=201,
                         sub_type_as_text="AmberAmulet", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def shop_end_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                         animation_event_sequence: AnimationEventSequence):
        logical_level = self.get_logical_level()
        if logical_level == 1:
            boost = 1
        elif logical_level == 2:
            boost = 2
        else:
            boost = 3

        self.generic_ability_notification(
            state=shop_state,
            state_set=state_set,
            animation_event_sequence=animation_event_sequence)
        g = Group()
        for x in [x for x in shop_state.friendly_recruits if x.type != "EmptySlot"]:
            x.shop_buff_stats(
                shop_state=shop_state,
                state_set=state_set,
                stack_item=stack_item,
                animation_event_sequence=animation_event_sequence,
                initiative=boost,
                group=g
            )

        g.set_state_id(state_id=state_set.add_state(state=shop_state))
        animation_event_sequence.append(g)

    def shop_set_object_data(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                             user_input: "ShopUserInput", animation_event_sequence: AnimationEventSequence,
                             original_shop_snapshot: "ShopSnapshotSerializer" = None):
        if user_input.set_shop_object_data_opcode == GameConstants.Opcodes.ObjectData.shop_upgrade_object:
            logical_level = self.get_logical_level()
            if logical_level >= 3:
                raise Exception("AmberAmulet cannot be upgraded past level 3")

            if shop_state.money < 10:
                raise Exception(f"Not enough money to upgrade {self.__class__.__name__}")
            shop_state.money -= 10

            if logical_level == 1:
                self.experience = GameConstants.Levels.level_2
            elif logical_level == 2:
                self.experience = GameConstants.Levels.level_3
            e = Animations.ShopUpdatedRelic(shop_id=self.shop_id,
                                            state_id=state_set.add_state(shop_state),
                                            battle_id=self.battle_id)
            animation_event_sequence.append(e)
        else:
            super().shop_set_object_data(shop_state=shop_state, state_set=state_set,
                                         stack_item=stack_item, user_input=user_input,
                                         animation_event_sequence=animation_event_sequence)

