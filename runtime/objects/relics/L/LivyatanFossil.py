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


class LivyatanFossil(RelicSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=164,
                         sub_type_as_text="LivyatanFossil", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def shop_bought(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                    animation_event_sequence: AnimationEventSequence,
                    shop_snapshot: "ShopSnapshotSerializer" = None):
        e = Animations.ShopUpdatedRecruit(shop_id=self.shop_id,
                                          state_id=state_set.add_state(shop_state),
                                          battle_id=self.battle_id)
        animation_event_sequence.append(e)
        g = Group()
        for x in shop_state.friendly_recruits:
            if GameConstants.ScientificNames.Cetacea in x.binomial_nomenclature:
                x.shop_buff_stats(
                    armor=3,
                    health=20,
                    max_health=20,
                    shop_state=shop_state,
                    state_set=state_set,
                    stack_item=stack_item,
                    buffer=self,
                    group=g,
                    animation_event_sequence=animation_event_sequence)
        if len(g.animation_events) > 0:
            g.set_state_id(state_id=state_set.add_state(state=shop_state))
            animation_event_sequence.append(g)

