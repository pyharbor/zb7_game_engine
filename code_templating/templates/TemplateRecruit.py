from typing import Union
from zb7_game_engine.code_templating.FunctionSourceCode import FunctionSourceCode
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.Listeners import Listeners
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from collections import deque
from typing import List, TYPE_CHECKING, Union

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.serialization.ShopStateSerializer import ShopStateSerializer
from zb7_game_engine.serialization.BattleStateSerializer import BattleStateSerializer
from zb7_game_engine.runtime.core.StackItem import StackItem
from zb7_game_engine.runtime.core.StateSet import StateSet
from zb7_game_engine.runtime.core.shop_opcodes.ShopUserInput import ShopUserInput
from zb7_game_engine.serialization.animation_events.Animations import Animations
from zb7_game_engine.serialization.animation_events.G.Group import Group


# from zb7_game_engine.serialization.BattleSnapshotSerializer import BattleSnapshotSerializer
# from zb7_game_engine.serialization.ShopSnapshotSerializer import ShopSnapshotSerializer
# from zb7_game_engine.serialization.RelicSerializer import RelicSerializer
# from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
# from zb7_game_engine.serialization.StatusSerializer import StatusSerializer


class TemplateRecruit(RecruitSerializer):

    def update_shop_state(self, shop_state: "ShopStateSerializer",
                          state_set: StateSet,
                          stack_item: StackItem,
                          animation_event_sequence: AnimationEventSequence,
                          original_shop_state: "ShopStateSerializer" = None):
        super().update_shop_state(shop_state, state_set, stack_item, animation_event_sequence, original_shop_state)

    def update_battle_state(self, battle_state: "BattleStateSerializer",
                            state_set: StateSet,
                            stack_item: StackItem,
                            animation_event_sequence: AnimationEventSequence,
                            original_shop_state: "ShopStateSerializer" = None):
        super().update_battle_state(battle_state, state_set, stack_item, animation_event_sequence,
                                    original_shop_state)

    @classmethod
    def bytes_to_custom_data(cls, _bytes: bytes, current_index: int) -> dict:
        return {}

    def custom_data_to_bytes(self) -> bytes:
        return b""

    def passive_battle_ability(self,
                               battle_state: "BattleStateSerializer",
                               state_set: StateSet,
                               stack_item: "StackItem",
                               animation_event_sequence: AnimationEventSequence,
                               original_shop_state: "ShopStateSerializer" = None):
        for x in self.listeners.get_listeners(hook=Listeners.Hooks.passive_battle_ability):
            # basically we allow arbitrary other objects to affect the 'fainting' of a unit
            # if that unit is revived it doesn't actually need to faint and thus returns immediately
            should_return = x.lt_passive_battle_ability(
                battle_state=battle_state,
                state_set=state_set,
                stack_item=stack_item,
                animation_event_sequence=animation_event_sequence,
                original_shop_state=original_shop_state
            )
            if should_return:
                return
        super().passive_battle_ability(battle_state, state_set, stack_item, animation_event_sequence,
                                       original_shop_state)

    def start_of_battle(self,
                        battle_state: "BattleStateSerializer",
                        state_set: "StateSet",
                        stack_item: "StackItem",
                        animation_event_sequence: AnimationEventSequence,
                        original_shop_state: "ShopStateSerializer" = None):
        super().start_of_battle(battle_state, state_set, stack_item, animation_event_sequence, original_shop_state)

    def battle_friendly_recruit_faints(self, battle_state: "BattleStateSerializer",
                                       state_set: StateSet,
                                       stack_item: StackItem,
                                       animation_event_sequence: AnimationEventSequence,
                                       original_shop_state: "ShopStateSerializer" = None):
        for x in self.listeners.get_listeners(hook=Listeners.Hooks.battle_friendly_recruit_faints):
            # basically we allow arbitrary other objects to affect the 'fainting' of a unit
            # if that unit is revived it doesn't actually need to faint and thus returns immediately
            should_return = x.lt_battle_friendly_recruit_faints(
                battle_state=battle_state,
                state_set=state_set,
                stack_item=stack_item,
                animation_event_sequence=animation_event_sequence,
                original_shop_state=original_shop_state
            )
            if should_return:
                return
        super().battle_friendly_recruit_faints(battle_state, state_set, stack_item, animation_event_sequence,
                                               original_shop_state)

    def battle_friendly_recruit_summoned(self, battle_state: "BattleStateSerializer",
                                         state_set: StateSet,
                                         stack_item: StackItem,
                                         animation_event_sequence: AnimationEventSequence,
                                         original_shop_state: "ShopStateSerializer" = None):
        for x in self.listeners.get_listeners(hook=Listeners.Hooks.battle_friendly_recruit_summoned):
            # basically we allow arbitrary other objects to affect the 'fainting' of a unit
            # if that unit is revived it doesn't actually need to faint and thus returns immediately
            should_return = x.battle_friendly_recruit_summoned(
                battle_state=battle_state,
                state_set=state_set,
                stack_item=stack_item,
                animation_event_sequence=animation_event_sequence,
                original_shop_state=original_shop_state
            )
            if should_return:
                return
        super().battle_friendly_recruit_summoned(battle_state, state_set, stack_item, animation_event_sequence,
                                                 original_shop_state)

    def shop_friendly_recruit_faints(self, shop_state: "ShopStateSerializer",
                                     state_set: StateSet,
                                     stack_item: StackItem,
                                     animation_event_sequence: AnimationEventSequence,
                                     original_shop_state: "ShopSnapshotSerializer" = None):
        super().shop_friendly_recruit_faints(shop_state, state_set, stack_item, animation_event_sequence,
                                             original_shop_state)

    def shop_friendly_recruit_summoned(self, shop_state: "ShopStateSerializer",
                                       state_set: StateSet,
                                       stack_item: StackItem,
                                       animation_event_sequence: AnimationEventSequence,
                                       original_shop_state: "ShopSnapshotSerializer" = None):
        super().shop_friendly_recruit_summoned(shop_state, state_set, stack_item, animation_event_sequence,
                                               original_shop_state)

    def shop_faint(self, shop_state: "ShopStateSerializer",
                   state_set: StateSet,
                   stack_item: "StackItem",
                   animation_event_sequence: AnimationEventSequence,
                   original_shop_state: "ShopStateSerializer" = None):
        super().shop_faint(shop_state, state_set, stack_item, animation_event_sequence, original_shop_state)

    def battle_faint(self, battle_state: "BattleStateSerializer",
                     state_set: StateSet,
                     stack_item: "StackItem",
                     animation_event_sequence: AnimationEventSequence,
                     original_shop_state: "ShopStateSerializer" = None):
        for x in self.listeners.get_listeners(hook=Listeners.Hooks.battle_faint):
            # basically we allow arbitrary other objects to affect the 'fainting' of a unit
            # if that unit is revived it doesn't actually need to faint and thus returns immediately
            should_return = x.lt_battle_faint(
                battle_state=battle_state,
                state_set=state_set,
                stack_item=stack_item,
                animation_event_sequence=animation_event_sequence,
                original_shop_state=original_shop_state
            )
            if should_return:
                return
        e = Animations.Faint(
            state_id=state_set.add_state(state=battle_state),
            shop_id=self.shop_id,
            battle_id=self.battle_id,
        )
        animation_event_sequence.append(e)

        battle_info = battle_state.get_battle_info(battle_id=self.battle_id)
        objects = battle_info.friendly_recruits + battle_info.friendly_relics
        objects = [x for x in objects if x.battle_id != self.battle_id]
        battle_state.queue_ability_for(trigger=GameConstants.Opcodes.Stack.battle_friendly_recruit_faints,
                                       objects=objects,
                                       context={"target": self})

        battle_state.remove_recruit_from_battle(self)
        battle_state.stack = deque([x for x in battle_state.stack if x.object.battle_id != self.battle_id])

    def shop_attack_with_melee(self, shop_state: "ShopStateSerializer",
                               state_set: StateSet,
                               stack_item: "StackItem",
                               animation_event_sequence: AnimationEventSequence,
                               original_shop_state: "ShopStateSerializer" = None,
                               damage_type: str = "default"):
        super().shop_attack_with_melee(shop_state, state_set, stack_item, animation_event_sequence,
                                       original_shop_state, damage_type)

    def battle_attack_with_melee(self, battle_state: "BattleStateSerializer",
                                 state_set: StateSet,
                                 stack_item: "StackItem",
                                 animation_event_sequence: AnimationEventSequence,
                                 original_shop_state: "ShopStateSerializer" = None,
                                 damage_type: str = "default"):
        if self.team_index == 0 and self.melee_attack > 0:
            damage = self.melee_attack
            enemy_recruits = battle_state.get_battle_info(battle_id=self.battle_id).enemy_recruits
            if len(enemy_recruits) == 0:
                return
            front_enemy = enemy_recruits[0]

            for x in self.listeners.get_listeners(hook=Listeners.Hooks.battle_attack_with_melee):
                # basically we allow arbitrary other objects to affect the 'fainting' of a unit
                # if that unit is revived it doesn't actually need to faint and thus returns immediately
                damage, should_return = x.lt_battle_attack_with_melee(
                    battle_state=battle_state,
                    damage=damage,
                    enemy=front_enemy,
                    state_set=state_set,
                    stack_item=stack_item,
                    animation_event_sequence=animation_event_sequence,
                    original_shop_state=original_shop_state
                )
                if should_return:
                    return

            e = Animations.MeleeAttack(
                state_id=state_set.add_state(state=battle_state),
                shop_id=self.shop_id,
                battle_id=self.battle_id,
                target_battle_id=front_enemy.battle_id,
                target_shop_id=front_enemy.shop_id,
                amount=damage,
            )
            animation_event_sequence.append(e)
            if damage_type == "default":
                front_enemy.battle_receive_damage(damage=damage,
                                                  enemy=self,
                                                  state_set=state_set,
                                                  battle_state=battle_state,
                                                  animation_event_sequence=animation_event_sequence,
                                                  origin="melee")
            elif damage_type == "unblockable":
                front_enemy.battle_receive_unblockable_damage(damage=damage,
                                                              enemy=self,
                                                              state_set=state_set,
                                                              battle_state=battle_state,
                                                              animation_event_sequence=animation_event_sequence,
                                                              origin="melee")

            return front_enemy

    def shop_revive(self, shop_state: "ShopStateSerializer",
                    state_set: StateSet,
                    stack_item: "StackItem",
                    animation_event_sequence: AnimationEventSequence,
                    original_shop_state: "ShopStateSerializer" = None):
        super().shop_revive(shop_state, state_set, stack_item, animation_event_sequence, original_shop_state)

    def battle_revive(self, battle_state: "BattleStateSerializer",
                      state_set: StateSet,
                      stack_item: "StackItem",
                      animation_event_sequence: AnimationEventSequence,
                      original_shop_state: "ShopStateSerializer" = None):
        super().battle_revive(battle_state, state_set, stack_item, animation_event_sequence, original_shop_state)

    def shop_attack_with_range(self, shop_state: "ShopStateSerializer",
                               state_set: StateSet,
                               stack_item: "StackItem",
                               animation_event_sequence: AnimationEventSequence,
                               original_shop_state: "ShopStateSerializer" = None,
                               damage_type: str = "default",
                               group=None) -> Union["RecruitSerializer", None]:
        return super().shop_attack_with_range(shop_state, state_set, stack_item, animation_event_sequence,
                                              original_shop_state, damage_type, group)

    def battle_attack_with_range(self, battle_state: "BattleStateSerializer",
                                 state_set: StateSet,
                                 stack_item: "StackItem",
                                 animation_event_sequence: AnimationEventSequence,
                                 original_shop_state: "ShopStateSerializer" = None,
                                 damage_type: str = "default",
                                 group=None) -> Union["RecruitSerializer", None]:
        if self.team_index != 0 and self.ranged_attack > 0:
            random_enemy = self.get_random_enemy(battle_state=battle_state)
            if random_enemy is None:
                return
            damage = self.ranged_attack
            for x in self.listeners.get_listeners(hook=Listeners.Hooks.battle_attack_with_range):
                # basically we allow arbitrary other objects to affect the 'fainting' of a unit
                # if that unit is revived it doesn't actually need to faint and thus returns immediately
                damage, should_return = x.lt_battle_attack_with_range(
                    battle_state=battle_state,
                    enemy=random_enemy,
                    damage=damage,
                    state_set=state_set,
                    stack_item=stack_item,
                    animation_event_sequence=animation_event_sequence,
                    original_shop_state=original_shop_state
                )
                if should_return:
                    return

            e = Animations.RangedAttack(
                state_id=None,
                shop_id=self.shop_id,
                battle_id=self.battle_id,
                target_battle_id=random_enemy.battle_id,
                target_shop_id=random_enemy.shop_id,
                amount=damage,
            )
            if group is None:
                e.state_id = state_set.add_state(state=battle_state)
                animation_event_sequence.append(e)
            else:
                group.add_animation_event(e)

            if damage_type == "default":
                random_enemy.battle_receive_damage(damage=damage,
                                                   enemy=self,
                                                   state_set=state_set,
                                                   battle_state=battle_state,
                                                   animation_event_sequence=animation_event_sequence,
                                                   origin="ranged")
            elif damage_type == "unblockable":
                random_enemy.battle_receive_unblockable_damage(damage=damage,
                                                               enemy=self,
                                                               state_set=state_set,
                                                               battle_state=battle_state,
                                                               animation_event_sequence=animation_event_sequence,
                                                               origin="ranged")
            return random_enemy

    def battle_buff_stats(self, battle_state: "BattleStateSerializer",
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
        super().battle_buff_stats(battle_state, stack_item, state_set, animation_event_sequence,
                                  original_shop_state, melee, ranged, health, armor, initiative, buffer, group)

    def shop_buff_stats(self, shop_state: "ShopStateSerializer",
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
        super().shop_buff_stats(shop_state, stack_item, state_set, animation_event_sequence,
                                original_shop_state, melee, ranged, health, armor, initiative, buffer, group)

    def shop_debuff_stats(self,
                          shop_state: "ShopStateSerializer",
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
        super().shop_debuff_stats(shop_state, stack_item, state_set, animation_event_sequence,
                                  original_shop_state, melee, ranged, health, armor, initiative, buffer, group)

    def battle_debuff_stats(self,
                            battle_state: "BattleStateSerializer",
                            state_set: "StateSet",
                            animation_event_sequence: AnimationEventSequence,
                            original_shop_state: "ShopStateSerializer" = None,
                            melee: int = 0,
                            ranged: int = 0,
                            health: int = 0,
                            armor: int = 0,
                            initiative: int = 0,
                            stack_item: "StackItem" = None,
                            buffer: Union["RecruitSerializer", "RelicSerializer"] = None,
                            group: Group = None):
        super().battle_debuff_stats(battle_state, stack_item, state_set, animation_event_sequence,
                                    original_shop_state, melee, ranged, health, armor, initiative, buffer, group)

    def shop_receive_unblockable_damage(self, damage: int,
                                        shop_state: "ShopStateSerializer",
                                        enemy: "RecruitSerializer",
                                        animation_event_sequence: AnimationEventSequence,
                                        state_set: StateSet,
                                        origin: str = "melee",
                                        group=None,
                                        original_shop_state: "ShopStateSerializer" = None
                                        ) -> int:
        return super().shop_receive_unblockable_damage(damage, shop_state, enemy, animation_event_sequence,
                                                       state_set, origin, group, original_shop_state)

    def battle_receive_unblockable_damage(self, damage: int,
                                          battle_state: "BattleStateSerializer",
                                          enemy: "RecruitSerializer",
                                          animation_event_sequence: AnimationEventSequence,
                                          state_set: StateSet,
                                          origin: str = "melee",
                                          group=None,
                                          original_shop_state: "ShopStateSerializer" = None
                                          ) -> int:
        return super().battle_receive_unblockable_damage(damage, battle_state, enemy, animation_event_sequence,
                                                         state_set, origin, group, original_shop_state)

    def battle_receive_damage(self, damage: int,
                              battle_state: "BattleStateSerializer",
                              enemy: "RecruitSerializer",
                              state_set: StateSet,
                              animation_event_sequence: AnimationEventSequence,
                              origin: str = "melee",
                              original_shop_state: "ShopStateSerializer" = None,
                              damage_reduction_stack: list[dict] = None
                              ) -> int:
        return super().battle_receive_damage(damage, battle_state, enemy, state_set, animation_event_sequence,
                                             origin, original_shop_state, damage_reduction_stack)

    def shop_receive_damage(self, damage: int,
                            shop_state: "ShopStateSerializer",
                            enemy: "RecruitSerializer",
                            state_set: StateSet,
                            animation_event_sequence: AnimationEventSequence,
                            origin: str = "melee",
                            original_shop_state: "ShopSnapshotSerializer" = None,
                            damage_reduction_stack: list[dict] = None
                            ) -> int:
        return super().shop_receive_damage(damage, shop_state, enemy, state_set, animation_event_sequence,
                                           origin, original_shop_state, damage_reduction_stack)

    def battle_heal(self, heal: int, battle_state: "BattleStateSerializer", state_set: "StateSet",
                    healer: Union["RecruitSerializer", "RelicSerializer", "StatusSerializer"],
                    animation_event_sequence: AnimationEventSequence, group=None):
        super().battle_heal(heal, battle_state, state_set, healer, animation_event_sequence, group)

    def battle_receive_status_damage(self, damage: int, battle_state: "BattleStateSerializer", state_set: "StateSet",
                                     animation_event_sequence: AnimationEventSequence, status: "StatusSerializer"):
        super().battle_receive_status_damage(damage, battle_state, state_set, animation_event_sequence, status)

    def battle_before_everything(self, battle_state: "BattleStateSerializer", state_set: "StateSet",
                                 stack_item: "StackItem", animation_event_sequence: AnimationEventSequence,
                                 shop_snapshot: "ShopSnapshotSerializer" = None):
        super().battle_before_everything(battle_state, state_set, stack_item, animation_event_sequence,
                                         shop_snapshot)

    def shop_start_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                           animation_event_sequence: AnimationEventSequence,
                           shop_snapshot: "ShopSnapshotSerializer" = None):
        super().shop_start_of_turn(shop_state, state_set, stack_item, animation_event_sequence, shop_snapshot)

    def shop_end_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                         animation_event_sequence: AnimationEventSequence,
                         shop_snapshot: "ShopSnapshotSerializer" = None):
        super().shop_end_of_turn(shop_state, state_set, stack_item, animation_event_sequence)

    def shop_bought(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                    animation_event_sequence: AnimationEventSequence,
                    shop_snapshot: "ShopSnapshotSerializer" = None):
        raise NotImplementedError()

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

    def update_statuses(self, battle_state: "BattleStateSerializer",
                        state_set: "StateSet",
                        stack_item: "StackItem",
                        animation_event_sequence: AnimationEventSequence,
                        original_shop_state: "ShopStateSerializer" = None):
        for status in self.statuses:
            status.status_effect(recruit=self,
                                 state_set=state_set,
                                 battle_state=battle_state,
                                 stack_item=stack_item,
                                 animation_event_sequence=animation_event_sequence)

    def shop_friendly_recruit_sold(self, shop_state: "ShopStateSerializer",
                                   state_set: "StateSet",
                                   stack_item: "StackItem",
                                   animation_event_sequence: AnimationEventSequence,
                                   original_run_snapshot: "ShopSnapshotSerializer" = None):
        raise NotImplementedError()


if __name__ == "__main__":
    for k, v in TemplateRecruit.__dict__.items():
        if k.startswith("__"):
            continue
        x = FunctionSourceCode.from_function(v)
