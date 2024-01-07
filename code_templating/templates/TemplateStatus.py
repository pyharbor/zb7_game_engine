from typing import Union

from zoo_game_engine.game_engine.objects.AnimationEvent import AnimationEvent
from zoo_game_engine.game_engine.objects.AnimationList import AnimationList
from zoo_game_engine.game_engine.objects.StackItem import StackItem
from zoo_game_engine.game_engine.objects.hooks.Hooks import Hooks
import importlib
import inspect

from zb7_game_engine.code_templating.FunctionSourceCode import FunctionSourceCode
from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.serialization.StatusSerializer import StatusSerializer
from zb7_game_engine.serialization.animation_events.G.Group import Group


class TemplateStatus(StatusSerializer):

    def status_effect(self,
                      recruit: "RecruitSerializer",
                      battle_state: "BattleStateSerializer",
                      state_set: "StateSet",
                      stack_item: "StackItem",
                      animation_event_sequence: AnimationEventSequence,
                      original_shop_state: "ShopStateSerializer" = None):
        pass

    def stack(self,
              other: "StatusSerializer",
              recruit: "RecruitSerializer",
              battle_state: "BattleStateSerializer",
              state_set: "StateSet",
              animation_event_sequence: AnimationEventSequence,
              group: Group = None):
        self.counter += other.counter

    def on_append(self, recruit: "RecruitSerializer",
                  battle_state: "BattleStateSerializer",
                  state_set: "StateSet",
                  animation_event_sequence: AnimationEventSequence,
                  group: Group = None):
        pass

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
