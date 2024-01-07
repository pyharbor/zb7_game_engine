# from typing import TYPE_CHECKING, List
#
# from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
# from zb7_game_engine.runtime.core.GameConstants import GameConstants
# from zb7_game_engine.runtime.objects.statuses.Statuses import Statuses
# from zb7_game_engine.serialization.animation_events.Animations import Animations
#
# if TYPE_CHECKING:
#     from zb7_game_engine.serialization.ShopStateSerializer import ShopStateSerializer
#     from zb7_game_engine.serialization.BattleStateSerializer import BattleStateSerializer
#     from zb7_game_engine.runtime.core.StackItem import StackItem
#     from zb7_game_engine.runtime.core.StateSet import StateSet
#     from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
#
#
# class Hooks:
#     # @staticmethod
#     # def _get_damage_diff(earlier: int, current: int, sub_type: str, damage_reduction_stack: List[dict]):
#     #     diff = earlier - current
#     #     if diff > 0:
#     #         damage_reduction_stack.append(dict(amount=diff, sub_type_as_int=sub_type))
#
#     @staticmethod
#     def pre_receive_damage(self, damage,
#                            battle_state: "BattleStateSerializer",
#                            state_set: "StateSet",
#                            enemy: "RecruitSerializer",
#                            animation_event_sequence: AnimationEventSequence, origin: str,
#                            original_shop_state: "ShopStateSerializer",
#                            damage_reduction_stack) -> int:
#         damage_reduction_stack.append(
#             dict(amount=damage, sub_type_as_int=GameConstants.DamageReductionStack.UnModifiedDamage))
#         was_protected = Hooks.handle_protected_status(self=self, battle_state=battle_state,
#                                                       state_set=state_set,
#                                                       animation_event_sequence=animation_event_sequence,
#                                                       damage=damage,
#                                                       damage_reduction_stack=damage_reduction_stack)
#         if was_protected:
#             return 0
#
#         damage = Hooks.handle_protective_canopy(self=self, damage=damage, battle_state=battle_state,
#                                                 state_set=state_set,
#                                                 animation_event_sequence=animation_event_sequence, origin=origin,
#                                                 damage_reduction_stack=damage_reduction_stack)
#         if damage == 0:
#             return 0
#
#         damage = Hooks.thick_blubber_reduce_damage(self=self, damage=damage, battle_state=battle_state,
#                                                    state_set=state_set,
#                                                    animation_event_sequence=animation_event_sequence,
#                                                    damage_reduction_stack=damage_reduction_stack)
#         if damage == 0:
#             return 0
#
#         Hooks.burrowed(self=self, damage=damage, battle_state=battle_state,
#                        state_set=state_set,
#                        animation_event_sequence=animation_event_sequence, origin=origin,
#                        damage_reduction_stack=damage_reduction_stack)
#         if damage == 0:
#             return 0
#
#         damage = Hooks.handle_default_airborne_damage_reduction(self=self, damage=damage,
#                                                                 battle_state=battle_state,
#                                                                 state_set=state_set,
#                                                                 animation_event_sequence=animation_event_sequence,
#                                                                 damage_reduction_stack=damage_reduction_stack)
#         if damage == 0:
#             return 0
#
#         damage = Hooks.coral_reef_protection(self=self, damage=damage, battle_state=battle_state,
#                                              state_set=state_set,
#                                              animation_event_sequence=animation_event_sequence,
#                                              damage_reduction_stack=damage_reduction_stack)
#         if damage == 0:
#             return 0
#
#         damage = Hooks.shell_armor(self=self, damage=damage, battle_state=battle_state,
#                                    animation_event_sequence=animation_event_sequence,
#                                    state_set=state_set,
#                                    damage_reduction_stack=damage_reduction_stack)
#         if damage == 0:
#             return 0
#
#         # all of this can effectively scale, we can make it resolve in any order to favor relic interactions
#         damage = Hooks.handle_reptile_shed_tail(self=self, damage=damage,
#                                                 battle_state=battle_state,
#                                                 state_set=state_set,
#                                                 animation_event_sequence=animation_event_sequence,
#                                                 damage_reduction_stack=damage_reduction_stack)
#         return damage
#
#     @staticmethod
#     def post_attack_with_melee(self, battle_state: "BattleStateSerializer",
#                                enemy: "RecruitSerializer",
#                                state_set: "StateSet",
#                                animation_event_sequence: AnimationEventSequence):
#         Hooks.handle_submerged(self=self, battle_state=battle_state,
#                                state_set=state_set,
#                                animation_event_sequence=animation_event_sequence)
#
#     @staticmethod
#     def post_attack(self,
#                     battle_state: "BattleStateSerializer",
#                     state_set: "StateSet",
#                     stack_item: "StackItem",
#                     enemy: "RecruitSerializer",
#                     animation_event_sequence: AnimationEventSequence):
#         if self is not None:
#             Hooks.handle_corrosive_spit(self=self, battle_state=battle_state, state_set=state_set, enemy=enemy,
#                                         animation_event_sequence=animation_event_sequence)
#             Hooks.acrid_slime_skin_receive_damage(self=self, battle_state=battle_state, state_set=state_set,
#                                                   enemy=enemy,
#                                                   stack_item=stack_item,
#                                                   animation_event_sequence=animation_event_sequence)
#             Hooks.anemone_attachment(self=self, battle_state=battle_state, state_set=state_set, enemy=enemy,
#                                      animation_event_sequence=animation_event_sequence)
#
#     @staticmethod
#     def handle_protected_status(self,
#                                 battle_state: "BattleStateSerializer",
#                                 state_set: "StateSet",
#                                 damage: int,
#                                 animation_event_sequence: AnimationEventSequence,
#                                 damage_reduction_stack: List[dict]
#                                 ) -> bool:
#         is_protected = self.get_status(sub_type_as_int="Protected")
#         if is_protected:
#             damage_reduction_stack.append(dict(amount=damage,
#                                                sub_type_as_int=GameConstants.DamageReductionStack.Protected))
#         return is_protected is not None
#
#     @staticmethod
#     def handle_protective_canopy(self,
#                                  damage,
#                                  battle_state: "BattleStateSerializer",
#                                  state_set: "StateSet",
#                                  animation_event_sequence: AnimationEventSequence, origin: str,
#                                  damage_reduction_stack: List[dict]
#                                  ):
#         protective_canopy_exists = "ProtectiveCanopy" in [x.sub_type_as_text for x in battle_state.get_battle_info(
#             battle_id=self.battle_id).friendly_relics]
#         if origin == "ranged" and protective_canopy_exists:
#             reduced_damage = int(damage * 0.9)
#             damage_reduction_stack.append(
#                 dict(amount=damage - reduced_damage,
#                      sub_type_as_int=GameConstants.DamageReductionStack.ProtectiveCanopy))
#             return reduced_damage
#         return damage
#
#     @staticmethod
#     def handle_reptile_shed_tail(self,
#                                  damage: int,
#                                  battle_state: "BattleStateSerializer",
#                                  state_set: "StateSet",
#                                  animation_event_sequence: AnimationEventSequence,
#                                  damage_reduction_stack: List[dict]):
#         shed_tail_exists = "ShedTail" in [x.sub_type_as_text for x in battle_state.get_battle_info(
#             battle_id=self.battle_id).friendly_relics]
#         if shed_tail_exists and damage > int(self.health / 2):
#             original_damage = damage
#             damage = min(int(self.health / 2), damage)
#             damage_reduction_stack.append(dict(amount=original_damage - damage,
#                                                sub_type_as_int=GameConstants.DamageReductionStack.ShedTail))
#         return damage
#
#     @staticmethod
#     def handle_submerged(self,
#                          battle_state: "BattleStateSerializer",
#                          state_set: "StateSet",
#                          animation_event_sequence: AnimationEventSequence,
#                          original_shop_state: "ShopStateSerializer" = None):
#         status = self.get_status(Statuses.Submerged)
#         if status:
#             self.remove_status(status)
#
#     @staticmethod
#     def hymenoptera_durability_faint(self: "RecruitSerializer",
#                                      battle_state: "BattleStateSerializer",
#                                      state_set: "StateSet",
#                                      stack_item: "StackItem",
#                                      animation_event_sequence: AnimationEventSequence) -> bool:
#         completely_dead_and_should_remove = True
#         for status in self.statuses:
#             if status.sub_type_as_text == "HymenopteraDurability":
#                 status.counter -= 1
#                 if status.counter <= 0:
#                     self.remove_status(status=status)
#                 self.health = self.max_health
#                 battle_info = battle_state.get_battle_info(battle_id=self.battle_id)
#                 objects = [x for x in battle_info.friendly_recruits + battle_info.friendly_relics if
#                            x.battle_id != self.battle_id]
#                 battle_state.queue_ability_for(trigger=GameConstants.Opcodes.Battle.friendly_recruit_summoned,
#                                                objects=objects,
#                                                context={"target": self})
#
#                 e = Animations.HymenopteraReinforcements()
#                 animation_event_sequence.append(e)
#
#                 completely_dead_and_should_remove = False
#                 return completely_dead_and_should_remove
#         return completely_dead_and_should_remove
#
#     @staticmethod
#     def handle_corrosive_spit(self: "RecruitSerializer",
#                               battle_state: "BattleStateSerializer",
#                               state_set: "StateSet",
#                               enemy: "RecruitSerializer",
#                               animation_event_sequence: AnimationEventSequence):
#         if self is None:
#             print("self is None")
#         for status in self.statuses:
#             if status.sub_type_as_text == "CorrosiveSpit":
#                 enemy.armor -= status.counter
#                 break
#
#     @staticmethod
#     def coral_reef_protection(self, damage: int,
#                               battle_state: "BattleStateSerializer",
#                               state_set: "StateSet",
#                               animation_event_sequence: AnimationEventSequence,
#                               damage_reduction_stack: List[dict]) -> int:
#         for status in self.statuses:
#             if status.sub_type == "CoralProtection":
#                 reduced_damage = int(max(0, int(damage - status.counter)))
#                 counter_reduction = status.counter - damage
#                 damage_prevented = damage - reduced_damage
#                 damage_reduction_stack.append(dict(amount=damage_prevented,
#                                                    sub_type_as_int=GameConstants.DamageReductionStack.CoralProtection))
#                 status.counter -= counter_reduction
#                 return damage
#         return damage
#
#     @staticmethod
#     def anemone_attachment(self,
#                            battle_state: "BattleStateSerializer",
#                            state_set: "StateSet",
#                            enemy: "RecruitSerializer",
#                            animation_event_sequence: AnimationEventSequence):
#         for status in self.statuses:
#             if status.sub_type == "AnemoneAttachment":
#                 enemy.battle_receive_unblockable_damage(damage=3 * status.counter, battle_state=battle_state,
#                                                         state_set=state_set,
#                                                         origin="anemone_attachment",
#                                                         enemy=None, animation_event_sequence=animation_event_sequence)
#                 # e = AnimationEvent.create_battle_state_type(
#                 #     animation_type=GameConstants.Types.Animations.anemone_attachment_damage,
#                 #     animation_description=f"{enemy.sub_type}'s has been damaged by sea anemone for {3 * status.counter}",
#                 #     state=battle_state.copy()
#                 # )
#                 # animation_event_sequence.append(e)
#                 return
#
#     @staticmethod
#     def shell_armor(self, damage: int,
#                     battle_state: "BattleStateSerializer",
#                     state_set: "StateSet",
#                     animation_event_sequence: AnimationEventSequence,
#                     damage_reduction_stack: List[dict]) -> int:
#         for status in self.statuses:
#             if status.sub_type == "ShellArmor":
#                 reduced_damage = int(max(0, int(damage - status.counter)))
#                 shell_counter_reduction = status.counter - int(damage / 3)
#                 damage_reduction_stack.append(dict(amount=shell_counter_reduction,
#                                                    sub_type_as_int=GameConstants.DamageReductionStack.ShellArmor))
#                 status.counter -= shell_counter_reduction
#                 return damage
#         return damage
#
#     @staticmethod
#     def handle_default_airborne_damage_reduction(self,
#                                                  damage: int,
#                                                  battle_state: "BattleStateSerializer",
#                                                  state_set: "StateSet",
#                                                  animation_event_sequence: AnimationEventSequence,
#                                                  damage_reduction_stack: List[dict]) -> int:
#         status = self.get_status(sub_type_as_text="Airborne")
#         if status is not None:
#             evasion = 0.5
#             if self.sub_type in ["AndeanCondor"]:
#                 evasion = 0.75
#             elif self.sub_type in ["GriffonVulture"]:
#                 evasion = 1.0
#
#             num = battle_state.random.random()
#             if num < evasion:
#                 e = Animations.Dodge()
#                 animation_event_sequence.append(e)
#                 damage_reduction_stack.append(
#                     dict(amount=damage, sub_type_as_int=GameConstants.DamageReductionStack.AirborneEvasion))
#                 return 0
#             else:
#                 damage_multiplier = 0.5
#                 if self.sub_type in ["AndeanCondor"]:
#                     damage_multiplier = 0.75
#                 elif self.sub_type in ["GriffonVulture"]:
#                     damage_multiplier = 1.0
#                 original_damage = damage
#                 damage_reduction = 1 - damage_multiplier
#                 damage = int(damage * damage_reduction)
#                 damage_reduction_stack.append(
#                     dict(amount=original_damage - damage,
#                          sub_type_as_int=GameConstants.DamageReductionStack.AirborneDefense))
#                 return damage
#         else:
#             return damage
#
#     @staticmethod
#     def burrowed(self,
#                  damage: int,
#                  battle_state: "BattleStateSerializer",
#                  state_set: "StateSet",
#                  animation_event_sequence: AnimationEventSequence,
#                  origin: str,
#                  damage_reduction_stack: List[dict]) -> int:
#         if origin == "ranged" or origin.startswith("ranged_"):
#             for status in self.statuses:
#                 if status.sub_type == "Burrowed":
#                     original_damage = damage
#                     damage = round(damage - 60, 1)
#                     damage = int(max(0, int(damage)))
#                     damage_reduction_stack.append(dict(amount=original_damage - damage,
#                                                        sub_type_as_int=GameConstants.DamageReductionStack.Burrowed))
#                     return damage
#         return damage
#
#     @staticmethod
#     def acrid_slime_skin_receive_damage(self,
#                                         battle_state: "BattleStateSerializer",
#                                         state_set: "StateSet",
#                                         stack_item: "StackItem",
#                                         enemy: "RecruitSerializer",
#                                         animation_event_sequence: AnimationEventSequence):
#         if enemy is None:
#             return
#         for status in self.statuses:
#             if status.sub_type == "AcridSlimeSkin":
#                 enemy.battle_debuff_stats(
#                     battle_state=battle_state,
#                     state_set=state_set,
#                     stack_item=stack_item,
#                     animation_event_sequence=animation_event_sequence,
#                     original_shop_state=None,
#                     melee=-status.counter,
#                     ranged=-status.counter,
#                     buffer=self
#                 )
#                 return
#
#     @staticmethod
#     def thick_blubber_reduce_damage(self,
#                                     damage: int,
#                                     battle_state: "BattleStateSerializer",
#                                     state_set: "StateSet",
#                                     animation_event_sequence: AnimationEventSequence,
#                                     damage_reduction_stack: List[dict]) -> int:
#         for status in self.statuses:
#             if status.sub_type == "ThickBlubber":
#                 percent_reduction = 1 - (32 / ((status.counter + 1) ** 1.37 + 31))
#                 original_damage = damage
#                 damage -= int(damage * percent_reduction)
#                 damage_reduction_stack.append(dict(amount=original_damage - damage,
#                                                    sub_type_as_int=GameConstants.DamageReductionStack.ThickBlubber))
#                 return damage
#         return damage
