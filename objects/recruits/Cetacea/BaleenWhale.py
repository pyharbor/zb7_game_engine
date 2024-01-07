from typing import List

from collections import deque        
from zb7_game_engine.runtime.objects.statuses.Statuses import Statuses
from zb7_game_engine.serialization.animation_events.G.Group import Group
from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature
from zb7_game_engine.runtime.objects.base.BaseRecruit import BaseRecruit
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.StateSet import StateSet
from typing import List, TYPE_CHECKING, Union
from zb7_game_engine.runtime.core.StackItem import StackItem
from zb7_game_engine.serialization.animation_events.Animations import Animations
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.Listeners import Listeners
from zb7_game_engine.runtime.core.RandomEngine import random_engine
from zb7_game_engine.serialization.EmptySlotSerializer import EmptySlotSerializer
from zb7_game_engine.serialization.shared.custom_data.ShopIDTarget import ShopIDTarget
from zb7_game_engine.serialization.shared.custom_data.Uint8ArrayOfScientificNomenclature import Uint8ArrayOfScientificNomenclature
from zb7_game_engine.serialization.shared.custom_data.Uint8Counter import Uint8Counter
from zb7_game_engine.serialization.shared.custom_data.Uint16Counter import Uint16Counter
from zb7_game_engine.runtime.objects.relics.Relics import Relics
from zb7_game_engine.serialization.shared.custom_data.CarpenterAntCD import CarpenterAntCD
from zb7_game_engine.serialization.shared.custom_data.SeaOtterCD import SeaOtterCD


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


class BaleenWhale(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=43,
                         sub_type_as_text="BaleenWhale", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def shop_start_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                           animation_event_sequence: AnimationEventSequence,
                           shop_snapshot: "ShopSnapshotSerializer" = None):
        pass

    def start_of_battle(self,
                        battle_state: "BattleStateSerializer",
                        state_set: "StateSet",
                        stack_item: "StackItem",
                        animation_event_sequence: AnimationEventSequence,
                        original_shop_state: "ShopStateSerializer" = None):
        # info = battle_state.get_battle_info(battle_id=self.battle_id)
        # krill = [x for x in info.friendly_recruits if
        #          x.sub_type_as_text == "Krill"]
        # self.generic_ability_notification(
        #     state=battle_state,
        #     state_set=state_set,
        #     animation_event_sequence=animation_event_sequence)
        # buff = 0.75 * len(krill)
        # self.battle_buff_stats(
        #     battle_state=battle_state,
        #     animation_event_sequence=animation_event_sequence,
        #     state_set=state_set,
        #     stack_item=stack_item,
        #     melee=int(self.melee_attack * buff),
        #     ranged=int(self.ranged_attack * buff)
        # )
        pass

    def shop_end_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                         animation_event_sequence: AnimationEventSequence,
                         shop_snapshot: "ShopSnapshotSerializer" = None):
        krill_count = len([x for x in shop_state.friendly_recruits if
                           x.sub_type_as_text == "Krill"])
        if self.experience < GameConstants.Levels.level_3:
            boost = krill_count * 0.07
            self.generic_ability_notification(
                state=shop_state,
                state_set=state_set,
                animation_event_sequence=animation_event_sequence)
            self.shop_buff_stats(
                shop_state=shop_state,
                animation_event_sequence=animation_event_sequence,
                state_set=state_set,
                stack_item=stack_item,
                health=int(self.max_health * boost),
                max_health=int(self.max_health * boost),
                ranged=int(self.ranged_attack * boost),
            )

    def shop_level_up(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                      animation_event_sequence: AnimationEventSequence):
        logical_level = self.get_logical_level()
        if 3 <= logical_level <= 6:
            krill_count = len([x for x in shop_state.friendly_recruits if
                               x.sub_type_as_text == "Krill"])
            boost = krill_count * 0.09
            self.generic_ability_notification(
                state=shop_state,
                state_set=state_set,
                animation_event_sequence=animation_event_sequence)
            self.shop_buff_stats(
                shop_state=shop_state,
                animation_event_sequence=animation_event_sequence,
                state_set=state_set,
                stack_item=stack_item,
                health=int(self.max_health * boost),
                max_health=int(self.max_health * boost),
                ranged=int(self.ranged_attack * boost),
            )

