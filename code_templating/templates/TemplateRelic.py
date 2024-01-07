from typing import Union, TYPE_CHECKING

from zoo_game_engine.game_engine.objects.AnimationEvent import AnimationEvent
from zoo_game_engine.game_engine.objects.AnimationList import AnimationList
from zoo_game_engine.game_engine.objects.StackItem import StackItem
from zoo_game_engine.game_engine.objects.hooks.Hooks import Hooks
import importlib
import inspect

from zb7_game_engine.code_templating.FunctionSourceCode import FunctionSourceCode
from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.StateSet import StateSet
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.ExperienceMap import ExperienceLevelMap
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus
from zb7_game_engine.serialization.animation_events.Animations import Animations
from zb7_game_engine.serialization.animation_events.G.Group import Group

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


class TemplateRelic(RelicSerializer):

    def shop_bought(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                    animation_event_sequence: AnimationEventSequence,
                    shop_snapshot: "ShopSnapshotSerializer" = None):
        super().shop_bought(shop_state, state_set, stack_item, animation_event_sequence, original_shop_state)

    def shop_sold(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                  animation_event_sequence: AnimationEventSequence):
        super().shop_sold(shop_state, state_set, stack_item, animation_event_sequence)

    def shop_rolled(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                    animation_event_sequence: AnimationEventSequence):
        super().shop_rolled(shop_state, state_set, stack_item, animation_event_sequence)

    def shop_level_up(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                      animation_event_sequence: AnimationEventSequence):
        super().shop_level_up(shop_state, state_set, stack_item, animation_event_sequence)

    def battle_level_up(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                        animation_event_sequence: AnimationEventSequence):
        super().battle_level_up(shop_state, state_set, stack_item, animation_event_sequence)

    def shop_set_object_data(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                             user_input: "ShopUserInput", animation_event_sequence: AnimationEventSequence,
                             original_shop_snapshot: "ShopSnapshotSerializer" = None):
        super().shop_set_object_data(shop_state, state_set, stack_item, user_input, animation_event_sequence)

    def shop_gain_experience(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                             animation_event_sequence: AnimationEventSequence):
        super().shop_gain_experience(shop_state, state_set, stack_item, animation_event_sequence)

    def battle_gain_experience(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                               animation_event_sequence: AnimationEventSequence):
        super().battle_gain_experience(shop_state, state_set, stack_item, animation_event_sequence)

    def battle_before_everything(self, battle_state: "BattleStateSerializer", state_set: "StateSet",
                                 stack_item: "StackItem", animation_event_sequence: AnimationEventSequence,
                                 original_run_snapshot: "BattleSnapshotSerializer" = None):
        super().battle_before_everything(battle_state, state_set, stack_item, animation_event_sequence,
                                         original_run_snapshot)

    def shop_start_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                           animation_event_sequence: AnimationEventSequence):
        super().shop_start_of_turn(shop_state, state_set, stack_item, animation_event_sequence)

    def shop_friendly_recruit_summoned(self, shop_state: "ShopStateSerializer", state_set: "StateSet",
                                       stack_item: "StackItem", animation_event_sequence: AnimationEventSequence):
        super().shop_friendly_recruit_summoned(shop_state, state_set, stack_item, animation_event_sequence)

    def shop_end_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                         animation_event_sequence: AnimationEventSequence):
        super().shop_end_of_turn(shop_state, state_set, stack_item, animation_event_sequence)

    def battle_heal(self, heal: int, battle_state: "BattleStateSerializer", state_set: "StateSet",
                    healer: Union["RecruitSerializer", "RelicSerializer", "StatusSerializer"],
                    animation_event_sequence: AnimationEventSequence):
        super().battle_heal(heal, battle_state, state_set, healer, animation_event_sequence)

    def battle_receive_damage(self, damage: int,
                              battle_state: "BattleStateSerializer",
                              enemy: "RecruitSerializer",
                              state_set: StateSet,
                              animation_event_sequence: AnimationEventSequence,
                              origin: str = "melee",
                              original_run_snapshot: "BattleSnapshotSerializer" = None,
                              damage_reduction_stack: list[dict] = None
                              ) -> int:
        return super().battle_receive_damage(damage, battle_state, enemy, state_set, animation_event_sequence, origin,
                                             original_run_snapshot, damage_reduction_stack)

    def battle_receive_unblockable_damage(self, damage: int,
                                          battle_state: "BattleStateSerializer",
                                          enemy: "RecruitSerializer",
                                          animation_event_sequence: AnimationEventSequence,
                                          state_set: StateSet,
                                          origin: str = "melee",
                                          group=None,
                                          original_run_snapshot: "BattleSnapshotSerializer" = None
                                          ) -> int:
        return super().battle_receive_unblockable_damage(damage, battle_state, enemy, animation_event_sequence,
                                                         state_set, origin,
                                                         group, original_run_snapshot)

    def battle_debuff_stats(self,
                            battle_state: "BattleStateSerializer",
                            stack_item: "StackItem",
                            state_set: "StateSet",
                            animation_event_sequence: AnimationEventSequence,
                            original_run_snapshot: "BattleSnapshotSerializer" = None,
                            melee: int = 0,
                            ranged: int = 0,
                            health: int = 0,
                            armor: int = 0,
                            initiative: int = 0,
                            buffer: Union["RecruitSerializer", "RelicSerializer"] = None,
                            group=None):
        super().battle_debuff_stats(battle_state, stack_item, state_set, animation_event_sequence,
                                    original_run_snapshot,
                                    melee, ranged, health, armor, initiative, buffer, group)

    def battle_buff_stats(self, battle_state: "BattleStateSerializer",
                          stack_item: "StackItem",
                          state_set: "StateSet",
                          animation_event_sequence: AnimationEventSequence,
                          original_run_snapshot: "BattleSnapshotSerializer" = None,
                          melee: int = 0,
                          ranged: int = 0,
                          health: int = 0,
                          armor: int = 0,
                          initiative: int = 0,
                          buffer: Union["RecruitSerializer", "RelicSerializer"] = None,
                          group=None):
        super().battle_buff_stats(battle_state, stack_item, state_set, animation_event_sequence, original_run_snapshot,
                                  melee, ranged, health, armor, initiative, buffer, group)

    def generic_ability_notification(self,
                                     description: str,
                                     state_set: "StateSet",
                                     state: Union["BattleSnapshotSerializer", "ShopStateSerializer"],
                                     animation_event_sequence: AnimationEventSequence,
                                     group=None):
        super().generic_ability_notification(description, state_set, state, animation_event_sequence, group)

    def passive_battle_ability(self,
                               battle_state: "BattleStateSerializer",
                               state_set: StateSet,
                               stack_item: "StackItem",
                               animation_event_sequence: AnimationEventSequence,
                               original_shop_state: "ShopStateSerializer" = None):
        super().passive_battle_ability(battle_state, state_set, stack_item, animation_event_sequence,
                                       original_shop_state)

    def start_of_battle(self,
                        battle_state: "BattleStateSerializer",
                        state_set: StateSet,
                        stack_item: "StackItem",
                        animation_event_sequence: AnimationEventSequence,
                        original_run_snapshot: "BattleSnapshotSerializer" = None):
        super().start_of_battle(battle_state, state_set, stack_item, animation_event_sequence, original_run_snapshot)

    def battle_friendly_recruit_faints(self, battle_state: "BattleStateSerializer",
                                       state_set: StateSet,
                                       stack_item: StackItem,
                                       animation_event_sequence: AnimationEventSequence,
                                       original_run_snapshot: "BattleSnapshotSerializer" = None):
        super().battle_friendly_recruit_faints(battle_state, state_set, stack_item, animation_event_sequence,
                                               original_run_snapshot)

    def battle_friendly_recruit_summoned(self, battle_state: "BattleStateSerializer",
                                         state_set: StateSet,
                                         stack_item: StackItem,
                                         animation_event_sequence: AnimationEventSequence,
                                         original_run_snapshot: "BattleSnapshotSerializer" = None):
        super().battle_friendly_recruit_summoned(battle_state, state_set, stack_item, animation_event_sequence,
                                                 original_run_snapshot)

    def update_battle_state(self, battle_state: "BattleStateSerializer",
                            state_set: StateSet,
                            stack_item: StackItem,
                            animation_event_sequence: AnimationEventSequence,
                            original_run_snapshot: "BattleSnapshotSerializer" = None):
        super().update_battle_state(battle_state, state_set, stack_item, animation_event_sequence,
                                    original_run_snapshot)

    def update_shop_state(self, shop_state: "ShopStateSerializer",
                          state_set: StateSet,
                          stack_item: StackItem,
                          animation_event_sequence: AnimationEventSequence,
                          original_run_snapshot: "ShopSnapshotSerializer"):
        super().update_shop_state(shop_state, state_set, stack_item, animation_event_sequence,
                                  original_run_snapshot)

    def shop_player_decision(self, shop_state: "ShopStateSerializer",
                             state_set: "StateSet",
                             stack_item: "StackItem",
                             animation_event_sequence: AnimationEventSequence,
                             original_run_snapshot: "ShopSnapshotSerializer" = None):
        super().shop_player_decision(shop_state, state_set, stack_item, animation_event_sequence,
                                     original_run_snapshot)

    def lt_shop_bought(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                       animation_event_sequence: AnimationEventSequence):
        raise NotImplementedError()

    def lt_shop_sold(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                     animation_event_sequence: AnimationEventSequence):
        raise NotImplementedError()

    def lt_shop_rolled(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                       animation_event_sequence: AnimationEventSequence):
        raise NotImplementedError()

    def lt_shop_level_up(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                         animation_event_sequence: AnimationEventSequence):
        raise NotImplementedError()

    def lt_battle_level_up(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                           animation_event_sequence: AnimationEventSequence):
        raise NotImplementedError()

    def lt_shop_set_object_data(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                                user_input: "ShopUserInput", animation_event_sequence: AnimationEventSequence):
        raise NotImplementedError()

    def lt_shop_gain_experience(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                                animation_event_sequence: AnimationEventSequence):
        raise NotImplementedError()

    def lt_battle_gain_experience(self, shop_state: "ShopStateSerializer", state_set: "StateSet",
                                  stack_item: "StackItem",
                                  animation_event_sequence: AnimationEventSequence):
        raise NotImplementedError()

    def lt_battle_receive_status_damage(self, damage: int, battle_state: "BattleStateSerializer", state_set: "StateSet",
                                        animation_event_sequence: AnimationEventSequence):
        raise NotImplementedError()

    def lt_battle_before_everything(self, battle_state: "BattleStateSerializer", state_set: "StateSet",
                                    stack_item: "StackItem", animation_event_sequence: AnimationEventSequence,
                                    original_shop_state: "ShopStateSerializer" = None):
        raise NotImplementedError()

    def lt_shop_start_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                              animation_event_sequence: AnimationEventSequence):
        raise NotImplementedError()

    def lt_shop_end_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                            animation_event_sequence: AnimationEventSequence):
        raise NotImplementedError()

    def lt_battle_heal(self, heal: int, battle_state: "BattleStateSerializer", state_set: "StateSet",
                       healer: Union["RecruitSerializer", "RelicSerializer", "StatusSerializer"],
                       animation_event_sequence: AnimationEventSequence, group: Group = None):
        raise NotImplementedError()

    def lt_shop_receive_damage(self, damage: int,
                               shop_State: "ShopStateSerializer",
                               enemy: "RecruitSerializer",
                               state_set: "StateSet",
                               recruit: "RecruitSerializer",
                               animation_event_sequence: AnimationEventSequence,
                               origin: str = "melee",
                               original_run_snapshot: "ShopSnapshotSerializer" = None,
                               damage_reduction_stack: list[dict] = None
                               ) -> list[int, bool]:
        raise NotImplementedError()

    def lt_battle_receive_damage(self, damage: int,
                                 battle_state: "BattleStateSerializer",
                                 enemy: "BaseRecruit",
                                 state_set: "StateSet",
                                 animation_event_sequence: AnimationEventSequence,
                                 recruit: "RecruitSerializer",
                                 origin: str = "melee",
                                 original_shop_state: "ShopStateSerializer" = None,
                                 damage_reduction_stack: list[dict] = None,
                                 ) -> list[int, bool]:
        raise NotImplementedError()

    def lt_shop_receive_unblockable_damage(self, damage: int,
                                           shop_state: "ShopStateSerializer",
                                           enemy: "RecruitSerializer",
                                           animation_event_sequence: AnimationEventSequence,
                                           state_set: "StateSet",
                                           origin: str = "melee",
                                           group: Group = None,
                                           original_run_snapshot: "ShopSnapshotSerializer" = None
                                           ) -> int:
        pass

    def lt_battle_receive_unblockable_damage(self, damage: int,
                                             battle_state: "BattleStateSerializer",
                                             enemy: "RecruitSerializer",
                                             animation_event_sequence: AnimationEventSequence,
                                             state_set: "StateSet",
                                             origin: str = "melee",
                                             group: Group = None,
                                             original_shop_state: "ShopStateSerializer" = None
                                             ) -> int:
        raise NotImplementedError()

    def lt_battle_debuff_stats(self,
                               battle_state: "BattleStateSerializer",
                               stack_item: "StackItem",
                               state_set: "StateSet",
                               animation_event_sequence: AnimationEventSequence,
                               original_shop_state: "ShopStateSerializer" = None,
                               melee: int = 0,
                               ranged: int = 0,
                               health: int = 0,
                               armor: int = 0,
                               initiative: int = 0,
                               buffer: Union["RecruitSerializer", "RelicSerializer"] = None,
                               group: Group = None):
        raise NotImplementedError()

    def lt_shop_debuff_stats(self,
                             shop_state: "ShopStateSerializer",
                             stack_item: "StackItem",
                             state_set: "StateSet",
                             animation_event_sequence: AnimationEventSequence,
                             original_shop_state: "ShopStateSerializer" = None,
                             melee: int = 0,
                             ranged: int = 0,
                             health: int = 0,
                             armor: int = 0,
                             initiative: int = 0,
                             buffer: Union["RecruitSerializer", "RelicSerializer"] = None,
                             group: Group = None):
        raise NotImplementedError()

    def lt_shop_buff_stats(self, shop_state: "ShopStateSerializer",
                           stack_item: "StackItem",
                           state_set: "StateSet",
                           animation_event_sequence: AnimationEventSequence,
                           original_shop_state: "ShopStateSerializer" = None,
                           melee: int = 0,
                           ranged: int = 0,
                           health: int = 0,
                           max_health: int = 0,
                           armor: int = 0,
                           initiative: int = 0,
                           buffer: Union["RecruitSerializer", "RelicSerializer"] = None,
                           group: Group = None):
        raise NotImplementedError()

    def lt_battle_buff_stats(self, battle_state: "BattleStateSerializer",
                             stack_item: "StackItem",
                             state_set: "StateSet",
                             animation_event_sequence: AnimationEventSequence,
                             original_shop_state: "ShopStateSerializer" = None,
                             melee: int = 0,
                             ranged: int = 0,
                             health: int = 0,
                             max_health: int = 0,
                             armor: int = 0,
                             initiative: int = 0,
                             buffer: Union["RecruitSerializer", "RelicSerializer"] = None,
                             group: Group = None):
        raise NotImplementedError()

    def lt_shop_attack_with_range(self, shop_state: "ShopStateSerializer",
                                  state_set: "StateSet",
                                  stack_item: "StackItem",
                                  animation_event_sequence: AnimationEventSequence,
                                  original_run_snapshot: "ShopSnapshotSerializer" = None,
                                  damage_type: str = "default",
                                  group: Group = None) -> Union["RecruitSerializer", None]:
        raise NotImplementedError()

    def lt_shop_revive(self, shop_state: "ShopStateSerializer",
                       state_set: "StateSet",
                       stack_item: "StackItem",
                       animation_event_sequence: AnimationEventSequence,
                       original_run_snapshot: "ShopSnapshotSerializer" = None):
        raise NotImplementedError()

    def lt_battle_revive(self, battle_state: "BattleStateSerializer",
                         state_set: "StateSet",
                         stack_item: "StackItem",
                         animation_event_sequence: AnimationEventSequence,
                         original_shop_state: "ShopStateSerializer" = None):
        raise NotImplementedError()

    def lt_shop_attack_with_melee(self, shop_state: "ShopStateSerializer",
                                  state_set: "StateSet",
                                  stack_item: "StackItem",
                                  animation_event_sequence: AnimationEventSequence,
                                  original_run_snapshot: "ShopSnapshotSerializer" = None,
                                  damage_type: str = "default"):
        raise NotImplementedError()

    def lt_battle_attack_with_melee(self, battle_state: "BattleStateSerializer",
                                    damage: int,
                                    enemy: "RecruitSerializer",
                                    state_set: "StateSet",
                                    stack_item: "StackItem",
                                    animation_event_sequence: AnimationEventSequence,
                                    original_shop_state: "ShopStateSerializer" = None,
                                    damage_type: str = "default"):
        raise NotImplementedError()

    def lt_battle_attack_with_range(self, battle_state: "BattleStateSerializer",
                                    damage: int,
                                    enemy: "RecruitSerializer",
                                    state_set: "StateSet",
                                    stack_item: "StackItem",
                                    animation_event_sequence: AnimationEventSequence,
                                    original_shop_state: "ShopStateSerializer" = None,
                                    damage_type: str = "default",
                                    group: Group = None) -> list[int, bool]:
        raise NotImplementedError()

    def lt_shop_faint(self, shop_state: "ShopStateSerializer",
                      state_set: "StateSet",
                      stack_item: "StackItem",
                      animation_event_sequence: AnimationEventSequence,
                      original_shop_state: "ShopStateSerializer" = None):
        raise NotImplementedError()

    def lt_battle_faint(self, battle_state: "BattleStateSerializer",
                        state_set: "StateSet",
                        stack_item: "StackItem",
                        animation_event_sequence: AnimationEventSequence,
                        original_shop_state: "ShopStateSerializer" = None):
        raise NotImplementedError()

    def lt_passive_battle_ability(self,
                                  battle_state: "BattleStateSerializer",
                                  state_set: "StateSet",
                                  stack_item: "StackItem",
                                  animation_event_sequence: AnimationEventSequence,
                                  original_shop_state: "ShopStateSerializer" = None):
        raise NotImplementedError()

    def lt_start_of_battle(self,
                           battle_state: "BattleStateSerializer",
                           state_set: "StateSet",
                           stack_item: "StackItem",
                           animation_event_sequence: AnimationEventSequence,
                           original_shop_state: "ShopStateSerializer" = None):
        raise NotImplementedError()

    def lt_battle_friendly_recruit_faints(self, battle_state: "BattleStateSerializer",
                                          state_set: "StateSet",
                                          stack_item: "StackItem",
                                          animation_event_sequence: AnimationEventSequence,
                                          original_shop_state: "ShopStateSerializer" = None):
        raise NotImplementedError()

    def lt_battle_friendly_recruit_summoned(self, battle_state: "BattleStateSerializer",
                                            state_set: "StateSet",
                                            stack_item: "StackItem",
                                            animation_event_sequence: AnimationEventSequence,
                                            original_shop_state: "ShopStateSerializer" = None):
        raise NotImplementedError()

    def lt_shop_friendly_recruit_faints(self, shop_state: "ShopStateSerializer",
                                        state_set: "StateSet",
                                        stack_item: "StackItem",
                                        animation_event_sequence: AnimationEventSequence,
                                        original_run_snapshot: "ShopSnapshotSerializer" = None):
        raise NotImplementedError()

    def lt_shop_friendly_recruit_summoned(self, shop_state: "ShopStateSerializer",
                                          state_set: "StateSet",
                                          stack_item: "StackItem",
                                          animation_event_sequence: AnimationEventSequence,
                                          original_run_snapshot: "ShopSnapshotSerializer" = None):
        raise NotImplementedError()

    def lt_add_status(self, status: BaseStatus,
                      battle_state: "BattleStateSerializer",
                      state_set: "StateSet",
                      enemy: "RecruitSerializer",
                      animation_event_sequence: AnimationEventSequence,
                      origin: str = "melee",
                      original_shop_state: "ShopStateSerializer" = None
                      ):
        raise NotImplementedError()

    @classmethod
    def bytes_to_custom_data(cls, _bytes: bytes, current_index: int) -> dict:
        return {}

    def custom_data_to_bytes(self) -> bytes:
        return b""

    def shop_friendly_recruit_sold(self, shop_state: "ShopStateSerializer",
                                   state_set: "StateSet",
                                   stack_item: "StackItem",
                                   animation_event_sequence: AnimationEventSequence,
                                   original_run_snapshot: "ShopSnapshotSerializer" = None):
        raise NotImplementedError()