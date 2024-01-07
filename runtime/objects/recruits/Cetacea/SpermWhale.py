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


class SpermWhale(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=5,
                         sub_type_as_text="SpermWhale", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------
        self.armor_boost = 0

        
    def start_of_battle(self,
                        battle_state: "BattleStateSerializer",
                        state_set: "StateSet",
                        stack_item: "StackItem",
                        animation_event_sequence: AnimationEventSequence,
                        original_shop_state: "ShopStateSerializer" = None):
        self.generic_ability_notification(
            state=battle_state,
            state_set=state_set,
            animation_event_sequence=animation_event_sequence)
        cumulative_health = sum([recruit.health for recruit in battle_state.friendly_recruits])
        deep_sea_recruits = len([recruit for recruit in battle_state.friendly_recruits
                             if GameConstants.Habitats.DeepSea in recruit.binomial_nomenclature])
        cetcea_recruits = len([recruit for recruit in battle_state.friendly_recruits
                             if GameConstants.ScientificNames.Cetacea in recruit.binomial_nomenclature])
        armor_buff = int(cumulative_health / 5)
        armor_buff = max(0, armor_buff)
        armor_buff = min(100, armor_buff)
        health_buff = int(cetcea_recruits * 5)
        ranged_buff = int(deep_sea_recruits * 5)
        self.battle_buff_stats(
            battle_state=battle_state,
            state_set=state_set,
            stack_item=stack_item,
            animation_event_sequence=animation_event_sequence,
            original_shop_state=original_shop_state,
            armor=armor_buff,
            health=health_buff,
            ranged=ranged_buff,
            max_health=health_buff
        )
        self.armor_boost = armor_buff

    # def battle_receive_damage(self, damage: int,
    #                           battle_state: "BattleStateSerializer",
    #                           enemy: "RecruitSerializer",
    #                           state_set: StateSet,
    #                           animation_event_sequence: AnimationEventSequence,
    #                           origin: str = "melee",
    #                           original_shop_state: "ShopStateSerializer" = None,
    #                           damage_reduction_stack: list[dict] = None
    #                           ) -> int:
    #     overkill = super().battle_receive_damage(damage, battle_state, enemy, state_set, animation_event_sequence,
    #                                              origin, original_shop_state, damage_reduction_stack)
    #     armor_buff = int((self.health - 80) / 2)
    #     if self.experience < GameConstants.Levels.level_2:
    #         armor_buff = min(10, armor_buff)
    #     elif self.experience < GameConstants.Levels.level_3:
    #         armor_buff = min(20, armor_buff)
    #     elif self.experience < GameConstants.Levels.level_4:
    #         armor_buff = min(40, armor_buff)
    #     else:
    #         armor_buff = min(80, armor_buff)
    #     armor_buff = max(0, armor_buff)
    #     difference = self.armor_boost - armor_buff
    #     if difference > 0:
    #         self.battle_debuff_stats(
    #             battle_state=battle_state,
    #             state_set=state_set,
    #             stack_item=None,
    #             animation_event_sequence=animation_event_sequence,
    #             original_shop_state=original_shop_state,
    #             armor=difference
    #         )
    #     self.armor_boost = armor_buff
    #     return overkill

    # def battle_heal(self, heal: int, battle_state: "BattleStateSerializer", state_set: "StateSet",
    #                 healer: Union["RecruitSerializer", "RelicSerializer", "StatusSerializer"],
    #                 animation_event_sequence: AnimationEventSequence, group=None):
    #     super().battle_heal(heal, battle_state, state_set, healer, animation_event_sequence, group)
        # armor_buff = int((self.health - 80) / 2)
        # if self.experience < GameConstants.Levels.level_2:
        #     armor_buff = min(10, armor_buff)
        # elif self.experience < GameConstants.Levels.level_3:
        #     armor_buff = min(20, armor_buff)
        # elif self.experience < GameConstants.Levels.level_4:
        #     armor_buff = min(40, armor_buff)
        # else:
        #     armor_buff = min(80, armor_buff)
        # armor_buff = max(0, armor_buff)
        # difference = self.armor_boost - armor_buff
        # if difference < 0:
        #     self.battle_buff_stats(
        #         battle_state=battle_state,
        #         state_set=state_set,
        #         stack_item=None,
        #         animation_event_sequence=animation_event_sequence,
        #         original_shop_state=None,
        #         armor=abs(difference)
        #     )
        # self.armor_boost = armor_buff

