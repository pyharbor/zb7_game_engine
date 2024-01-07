from collections import deque
from typing import List, TYPE_CHECKING, Union

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.ExperienceMap import ExperienceLevelMap
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.Listeners import Listeners
from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature
from zb7_game_engine.runtime.misc.hooks.BasicArmor import BasicArmor
from zb7_game_engine.runtime.objects.base.BaseAbility import BaseAbility
from zb7_game_engine.runtime.objects.base.BaseListener import BaseListener
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


class BaseRecruit(BaseListener):
    def __init__(self,
                 sub_type_as_int: int = None,
                 sub_type_as_text: str = None,
                 team_index: int = None,
                 melee_attack: int = None,
                 ranged_attack: int = None,
                 armor: int = None,
                 health: int = None,
                 max_health: int = None,
                 initiative: float = None,
                 experience: int = 1,
                 cost: int = None,
                 name=None,
                 aaid: int = 0,
                 statuses: List["StatusSerializer"] = None,
                 triggers: List[str] = None,
                 shop_id: int = None,
                 battle_id: int = None,
                 random_seed=None,
                 binomial_nomenclature: BinomialNomenclature = None,
                 added_types: List[str] = None,
                 added_habitats: List[str] = None,
                 custom_data=None,
                 options=None,
                 bit_index: int = None,
                 ability: list = None,
                 rarity: str = None,
                 type: str = None,
                 habitats: str = None,
                 wikipedia_research_url: str = None,
                 arts: list = None,
                 stack_order_number: int = None,
                 main_species: str = None):
        self.sub_type_as_int: int = sub_type_as_int
        self.sub_type_as_text: str = sub_type_as_text
        immutable_data = ImmutableData.Subtype.from_int(sub_type_as_int)
        self.team_index: int = team_index or 0
        self._melee_attack: int
        self._ranged_attack: int
        self._armor: int
        self._health: int
        self._max_health: int
        self.rarity: str = immutable_data["rarity"]
        self.main_species: str = main_species
        self._initiative: float
        self._experience: int
        self._cost: int
        self._name: str
        self._aaid: int

        if melee_attack is None:
            self.melee_attack = immutable_data["melee_attack"]
        else:
            self.melee_attack = melee_attack
        if ranged_attack is None:
            self.ranged_attack = immutable_data["ranged_attack"]
        else:
            self.ranged_attack = ranged_attack
        if armor is None:
            self.armor = immutable_data["armor"]
        else:
            self.armor = armor
        if health is None:
            self.health = immutable_data["health"]
        else:
            self.health = health
        if max_health is None:
            self.max_health = immutable_data["max_health"]
        else:
            self.max_health = max_health
        if initiative is None:
            self.initiative = round(
                immutable_data["initiative"] + ImmutableData.Initiative.get_random_intiative(), 3)
        else:
            self.initiative = initiative

        try:
            if self.initiative < 0:
                ImmutableData.Initiative.to_int(abs(self.initiative))
            else:
                ImmutableData.Initiative.to_int(self.initiative)
        except KeyError:
            raise ValueError(f"Invalid initiative value: {{initiative}}")

        if experience is None:
            self.experience = 1
        else:
            self.experience = experience

        if cost is None:
            self.cost = immutable_data["cost"]
        else:
            self.cost = cost

        self.name = name or ""
        self.aaid = aaid

        self.statuses: List["StatusSerializer"] = statuses or []
        self.triggers: List[str] = triggers or immutable_data["triggers"]
        self.shop_id: int = shop_id
        self.battle_id: int = battle_id
        self.random_seed = random_seed
        self.binomial_nomenclature = BinomialNomenclature(**immutable_data["binomial_nomenclature"])
        self.habitats = immutable_data["habitats"]
        self.added_types = added_types or []
        self.added_habitats = added_habitats or []
        self.binomial_nomenclature.add_types(self.added_types)
        self.binomial_nomenclature.add_habitats(self.added_habitats)
        self.binomial_nomenclature.add_habitats(self.habitats)
        self.custom_data: dict = custom_data or {}
        self.options = immutable_data["options"] or options
        self.main_species = self.binomial_nomenclature.get_main_species()
        self.ability = immutable_data["ability"] or ability
        if self.ability:
            self.ability: List[BaseAbility] = [BaseAbility(**x) for x in self.ability]
        self.type = immutable_data["type"] or type
        self.wikipedia_research_url = immutable_data["wikipedia_research_url"] or wikipedia_research_url
        self.arts = arts
        self.probability = GameConstants.Rarity.rarity_to_probability_map[self.rarity]
        self.default_triggers = ["battle_attack_with_melee",
                                 "battle_attack_with_range",
                                 "battle_faint",
                                 "battle_level_up",
                                 "battle_gain_experience",
                                 "status_effect",
                                 "shop_level_up",
                                 "shop_gain_experience",
                                 "shop_set_object_data",
                                 "shop_faint"
                                 ]
        self.template_triggers = self.triggers
        self.triggers = list(set(self.triggers + self.default_triggers))
        self.stack_order_number = immutable_data.get("stack_order_number")
        self.listeners = Listeners()
        self.listeners.add_listener(hook=Listeners.Hooks.battle_receive_damage,
                                    listener=BasicArmor(listener_target=self))
        self.listeners.add_listener(hook=Listeners.Hooks.shop_receive_damage,
                                    listener=BasicArmor(listener_target=self))

    @property
    def melee_attack(self):
        return self._melee_attack

    @melee_attack.setter
    def melee_attack(self, value):
        if value > 65535:
            value = 65535
        self._melee_attack = value

    @property
    def ranged_attack(self):
        return self._ranged_attack

    @ranged_attack.setter
    def ranged_attack(self, value):
        if value > 65535:
            value = 65535
        self._ranged_attack = value

    @property
    def armor(self):
        return self._armor

    @armor.setter
    def armor(self, value):
        if value > 65535:
            value = 65535
        self._armor = value

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if value > 65535:
            value = 65535
        self._health = value

    @property
    def max_health(self):
        return self._max_health

    @max_health.setter
    def max_health(self, value):
        if value > 65535:
            value = 65535
        self._max_health = value

    @property
    def initiative(self):
        return self._initiative

    @initiative.setter
    def initiative(self, value):
        if value > 500.0:
            value = 500.0
        self._initiative = value

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value):
        if value > 65535:
            value = 65535
        self._experience = value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        if value > 255:
            value = 255
        self._cost = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is not None and len(value) > 17:
            value = value[:17]
        self._name = value

    @property
    def aaid(self):
        return self._aaid

    @aaid.setter
    def aaid(self, value):
        if 0 <= value <= 256:
            self._aaid = value
        else:
            raise ValueError(f"Invalid aaid value: {value}")

    def __eq__(self, other):
        if not isinstance(other, BaseRecruit):
            return False
        is_equal = self.shop_id == other.shop_id
        is_equal = is_equal and self.battle_id == other.battle_id
        is_equal = is_equal and self.sub_type_as_int == other.sub_type_as_int
        is_equal = is_equal and self.sub_type_as_text == other.sub_type_as_text
        is_equal = is_equal and self.melee_attack == other.melee_attack
        is_equal = is_equal and self.ranged_attack == other.ranged_attack
        is_equal = is_equal and self.health == other.health
        is_equal = is_equal and abs(self.initiative - other.initiative) < 0.0001
        is_equal = is_equal and self.armor == other.armor
        is_equal = is_equal and self.experience == other.experience
        return is_equal

    def __hash__(self):
        return hash((self.shop_id, self.battle_id, self.sub_type_as_int, self.sub_type_as_text))

    def shop_bought(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                    animation_event_sequence: AnimationEventSequence,
                    shop_snapshot: "ShopSnapshotSerializer" = None):
        pass

    def shop_sold(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                  animation_event_sequence: AnimationEventSequence):
        pass

    def shop_rolled(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                    animation_event_sequence: AnimationEventSequence):
        raise NotImplementedError()

    def shop_level_up(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                      animation_event_sequence: AnimationEventSequence):
        pass

    def battle_level_up(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                        animation_event_sequence: AnimationEventSequence):
        raise NotImplementedError()

    def shop_set_object_data(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                             user_input: "ShopUserInput", animation_event_sequence: AnimationEventSequence,
                             original_shop_snapshot: "ShopSnapshotSerializer" = None):
        if user_input.set_shop_object_data_opcode == GameConstants.Opcodes.ObjectData.shop_set_name:
            if len(user_input.target_object) > 17:
                raise Exception("Name too long, max 17 characters")
            if not isinstance(user_input.target_object, str):
                raise Exception("Name must be a string")
            self.name = user_input.target_object
        elif user_input.set_shop_object_data_opcode == GameConstants.Opcodes.ObjectData.shop_set_aaid:
            if not isinstance(user_input.target_object, int):
                raise Exception("Art ID must be an int")
            if 0 > user_input.target_object or user_input.target_object >= 256:
                raise Exception("Art ID must be between 0 and 256")
            self.aaid = user_input.target_object

    def shop_gain_experience(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                             animation_event_sequence: AnimationEventSequence):
        pass

    def battle_gain_experience(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                               animation_event_sequence: AnimationEventSequence):
        raise NotImplementedError()

    def battle_receive_status_damage(self, damage: int, battle_state: "BattleStateSerializer", state_set: "StateSet",
                                     animation_event_sequence: AnimationEventSequence, status: "StatusSerializer"):
        self.health -= damage
        e = Animations.ReceiveStatusDamage(
            shop_id=self.shop_id,
            battle_id=self.battle_id,
            status_sub_type_as_int=status.sub_type_as_int,
            amount=damage,
            state_id=state_set.add_state(battle_state)
        )
        animation_event_sequence.append(e)
        if self.health <= 0:
            battle_state.queue_ability_for(trigger=GameConstants.Opcodes.Stack.battle_faint,
                                           objects=[self], context={"enemy": None}, append_left=True)

    def battle_before_everything(self, battle_state: "BattleStateSerializer", state_set: "StateSet",
                                 stack_item: "StackItem", animation_event_sequence: AnimationEventSequence,
                                 original_shop_state: "ShopStateSerializer" = None):
        pass

    def shop_start_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                           animation_event_sequence: AnimationEventSequence,
                           shop_snapshot: "ShopSnapshotSerializer" = None):
        pass

    def shop_end_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                         animation_event_sequence: AnimationEventSequence,
                         shop_snapshot: "ShopSnapshotSerializer" = None):
        pass

    def battle_heal(self, heal: int, battle_state: "BattleStateSerializer", state_set: "StateSet",
                    healer: Union["RecruitSerializer", "RelicSerializer", "StatusSerializer"],
                    animation_event_sequence: AnimationEventSequence, group: Group = None):
        self.health = min(int(self.health + heal), self.max_health)
        e = Animations.Heal(
            state_id=None,
            shop_id=self.shop_id,
            battle_id=self.battle_id,
            amount=heal,
        )
        if group is None:
            e.state_id = state_set.add_state(state=battle_state)
            animation_event_sequence.append(e)
        else:
            group.add_animation_event(e)

    def shop_receive_damage(self, damage: int,
                            shop_state: "ShopStateSerializer",
                            enemy: "RecruitSerializer",
                            state_set: "StateSet",
                            animation_event_sequence: AnimationEventSequence,
                            origin: str = "melee",
                            original_run_snapshot: "ShopSnapshotSerializer" = None,
                            damage_reduction_stack: list[dict] = None
                            ) -> int:
        if damage_reduction_stack is None:
            damage_reduction_stack = [
                dict(amount=damage, sub_type_as_int=GameConstants.DamageReductionStack.UnModifiedDamage)]
        for x in self.listeners.get_listeners(hook=Listeners.Hooks.battle_receive_damage):
            damage, should_return = x.lt_shop_receive_damage(
                damage=damage,
                shop_state=shop_state,
                enemy=enemy,
                state_set=state_set,
                animation_event_sequence=animation_event_sequence,
                origin=origin,
                damage_reduction_stack=damage_reduction_stack,
                recruit=self,
            )
            if should_return:
                return
        overkill = damage - self.health
        if damage < 0:
            damage = 0
        self.health = max(self.health - damage, 0)
        self.max_health = max(self.max_health - damage, 0)
        initial_damage = damage_reduction_stack[0]["amount"]
        state_id = state_set.add_state(state=shop_state)
        if damage > 0:
            e = Animations.ReceiveDamage(
                state_id=state_id,
                damage_reduction_stack=damage_reduction_stack,
                damage_after_modifications=damage,
                damage_before_modifications=initial_damage,
                battle_id=self.battle_id,
                shop_id=self.shop_id,
            )
            animation_event_sequence.append(e)
        elif damage <= 0:
            e = Animations.FullBlock(
                state_id=state_id,
                damage_reduction_stack=damage_reduction_stack,
                damage_after_modifications=damage,
                damage_before_modifications=initial_damage,
                battle_id=self.battle_id,
                shop_id=self.shop_id,
            )
            animation_event_sequence.append(e)
        if self.health <= 0:
            shop_state.queue_ability_for(trigger=GameConstants.Opcodes.Stack.shop_faint,
                                         objects=[self], context={"enemy": enemy})
        return overkill

    def battle_receive_damage(self, damage: int,
                              battle_state: "BattleStateSerializer",
                              enemy: "RecruitSerializer",
                              state_set: "StateSet",
                              animation_event_sequence: AnimationEventSequence,
                              origin: str = "melee",
                              original_shop_state: "ShopStateSerializer" = None,
                              damage_reduction_stack: list[dict] = None
                              ) -> int:
        if damage_reduction_stack is None:
            damage_reduction_stack = [
                dict(amount=damage, sub_type_as_int=GameConstants.DamageReductionStack.UnModifiedDamage)]
        for x in self.listeners.get_listeners(hook=Listeners.Hooks.battle_receive_damage):
            damage, should_return = x.lt_battle_receive_damage(
                damage=damage,
                battle_state=battle_state,
                enemy=enemy,
                state_set=state_set,
                animation_event_sequence=animation_event_sequence,
                origin=origin,
                original_shop_state=original_shop_state,
                damage_reduction_stack=damage_reduction_stack,
                recruit=self,
            )
            if should_return:
                return
        overkill = damage - self.health
        if damage < 0:
            damage = 0
        self.health -= damage
        initial_damage = damage_reduction_stack[0]["amount"]
        state_id = state_set.add_state(state=battle_state)
        if damage > 0:
            e = Animations.ReceiveDamage(
                state_id=state_id,
                damage_reduction_stack=damage_reduction_stack,
                damage_after_modifications=damage,
                damage_before_modifications=initial_damage,
                battle_id=self.battle_id,
                shop_id=self.shop_id,
            )
            animation_event_sequence.append(e)
        elif damage <= 0:
            e = Animations.FullBlock(
                state_id=state_id,
                damage_reduction_stack=damage_reduction_stack,
                damage_after_modifications=damage,
                damage_before_modifications=initial_damage,
                battle_id=self.battle_id,
                shop_id=self.shop_id,
            )
            animation_event_sequence.append(e)
        if self.health <= 0:
            battle_state.queue_ability_for(trigger=GameConstants.Opcodes.Stack.battle_faint,
                                           objects=[self], context={"enemy": enemy}, append_left=True)
        return overkill

    def shop_receive_unblockable_damage(self, damage: int,
                                        shop_state: "ShopStateSerializer",
                                        enemy: "RecruitSerializer",
                                        animation_event_sequence: AnimationEventSequence,
                                        state_set: "StateSet",
                                        origin: str = "melee",
                                        group: Group = None,
                                        original_run_snapshot: "ShopSnapshotSerializer" = None
                                        ) -> int:
        pass

    def battle_receive_unblockable_damage(self, damage: int,
                                          battle_state: "BattleStateSerializer",
                                          enemy: "RecruitSerializer",
                                          animation_event_sequence: AnimationEventSequence,
                                          state_set: "StateSet",
                                          origin: str = "melee",
                                          group: Group = None,
                                          original_shop_state: "ShopStateSerializer" = None
                                          ) -> int:
        for x in self.listeners.get_listeners(hook=Listeners.Hooks.battle_receive_unblockable_damage):
            damage, should_return = x.lt_battle_receive_unblockable_damage(
                damage=damage,
                battle_state=battle_state,
                enemy=enemy,
                state_set=state_set,
                animation_event_sequence=animation_event_sequence,
                origin=origin,
                original_shop_state=original_shop_state
            )
            if should_return:
                return
        overkill = damage - self.health
        if damage < 0:
            damage = 0
        self.health -= damage

        if origin == "lightning":
            e = Animations.LightningDamage(
                state_id=state_set.add_state(state=battle_state),
                shop_id=self.shop_id,
                battle_id=self.battle_id,
                amount=damage,
            )
        elif origin == "fire":
            e = Animations.FireDamage(
                state_id=state_set.add_state(state=battle_state),
                shop_id=self.shop_id,
                battle_id=self.battle_id,
                amount=damage,
            )
        elif origin == "sandstorm":
            e = Animations.SandDamage(
                state_id=state_set.add_state(state=battle_state),
                shop_id=self.shop_id,
                battle_id=self.battle_id,
                amount=damage,
            )
        else:
            e = Animations.ReceiveUnblockableDamage(
                state_id=state_set.add_state(state=battle_state),
                shop_id=self.shop_id,
                battle_id=self.battle_id,
                amount=damage,
            )

        if group is None:
            e.state_id = state_set.add_state(state=battle_state)
            animation_event_sequence.append(e)
        else:
            group.add_animation_event(e)
        if self.health <= 0:
            battle_state.queue_ability_for(trigger=GameConstants.Opcodes.Stack.battle_faint,
                                           objects=[self], context={"enemy": enemy}, append_left=True)
        return overkill

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
        for x in self.listeners.get_listeners(hook=Listeners.Hooks.battle_debuff_stats):
            should_return = x.lt_battle_debuff_stats(
                battle_state=battle_state,
                state_set=state_set,
                animation_event_sequence=animation_event_sequence,
                original_shop_state=original_shop_state,
                melee=melee,
                ranged=ranged,
                health=health,
                armor=armor,
                initiative=initiative,
                stack_item=stack_item,
                buffer=buffer,
                group=group
            )
            if should_return:
                return
        self.melee_attack = max(0, self.melee_attack - melee)
        self.ranged_attack = max(0, self.ranged_attack - ranged)
        self.health -= health
        self.armor = max(0, self.armor - armor)
        self.health = max(1, self.health - health)
        self.initiative -= initiative
        self.initiative = round(self.initiative, 3)
        self.initiative = max(0.0, self.initiative)
        e = Animations.DebuffStats(
            state_id=None,
            shop_id=self.shop_id,
            battle_id=self.battle_id,
            melee=melee,
            ranged=ranged,
            health=health,
            max_health=health,
            armor=armor,
            initiative=initiative,
        )
        if group is None:
            e.state_id = state_set.add_state(state=battle_state)
            animation_event_sequence.append(e)
        else:
            group.add_animation_event(e)

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
        self.melee_attack = max(0, self.melee_attack - melee)
        self.ranged_attack = max(0, self.ranged_attack - ranged)
        self.health = max(1, self.health - health)
        self.max_health = max(1, self.max_health - max_health)
        self.armor = max(0, self.armor - armor)
        self.initiative -= initiative
        self.initiative = round(self.initiative, 3)
        self.initiative = float(max(0.0, self.initiative))
        e = Animations.DebuffStats(
            state_id=None,
            shop_id=self.shop_id,
            battle_id=self.battle_id,
            melee=melee,
            ranged=ranged,
            health=health,
            max_health=max_health,
            armor=armor,
            initiative=initiative,
        )
        if group is None:
            e.state_id = state_set.add_state(state=shop_state)
            animation_event_sequence.append(e)
        else:
            group.add_animation_event(e)

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
        self.melee_attack += melee
        self.ranged_attack += ranged
        self.health += health
        self.initiative += initiative
        self.initiative = round(self.initiative, 3)
        self.armor += armor
        self.melee_attack = self.melee_attack
        self.ranged_attack = self.ranged_attack
        self.health = max(1, self.health)
        self.max_health += max_health
        self.initiative = max(1, self.initiative)
        self.armor = max(0, self.armor)
        e = Animations.BuffStats(
            state_id=None,
            shop_id=self.shop_id,
            battle_id=self.battle_id,
            melee=melee,
            ranged=ranged,
            health=health,
            armor=armor,
            initiative=initiative,
            max_health=max_health,
        )
        if group is None:
            e.state_id = state_set.add_state(state=shop_state)
            animation_event_sequence.append(e)
        else:
            group.add_animation_event(e)

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

        for x in self.listeners.get_listeners(hook=Listeners.Hooks.battle_buff_stats):
            should_return = x.lt_battle_buff_stats(
                battle_state=battle_state,
                state_set=state_set,
                animation_event_sequence=animation_event_sequence,
                original_shop_state=original_shop_state,
                melee=melee,
                ranged=ranged,
                health=health,
                max_health=max_health,
                armor=armor,
                initiative=initiative,
                stack_item=stack_item,
                buffer=buffer,
                group=group
            )
            if should_return:
                return

        self.melee_attack += melee
        self.ranged_attack += ranged
        self.health += health
        self.max_health += max_health
        self.initiative += initiative
        self.initiative = round(self.initiative, 3)
        self.armor += armor
        self.health = max(1, self.health)
        self.max_health = max(1, self.max_health)
        self.initiative = max(1, self.initiative)
        self.armor = max(0, self.armor)
        e = Animations.BuffStats(
            state_id=None,
            shop_id=self.shop_id,
            battle_id=self.battle_id,
            melee=melee,
            ranged=ranged,
            health=health,
            max_health=max_health,
            armor=armor,
            initiative=initiative,
        )
        if group is None:
            e.state_id = state_set.add_state(state=battle_state)
            animation_event_sequence.append(e)
        else:
            group.add_animation_event(e)

    def generic_ability_notification(self,
                                     state_set: "StateSet",
                                     state: Union["BattleStateSerializer", "ShopStateSerializer"],
                                     animation_event_sequence: AnimationEventSequence,
                                     description: str = None,
                                     group: Group = None):
        if description is None:
            description = self.ability[0].name
        e = Animations.GenericAbilityNotification(
            state_id=None,
            shop_id=self.shop_id,
            battle_id=self.battle_id,
            description=description
        )
        if group is None:
            e.state_id = state_set.add_state(state=state)
            animation_event_sequence.append(e)
        else:
            group.add_animation_event(e)

    def get_random_enemy(self, battle_state: "BattleStateSerializer"):
        enemy_recruits = battle_state.get_battle_info(battle_id=self.battle_id).enemy_recruits
        # check for a baboon on the enemy team
        enemy_recruits = sorted(enemy_recruits, key=lambda x: x.initiative, reverse=True)
        enemy_recruits = [x for x in enemy_recruits if x.get_status("Camouflage") is None]
        for x in enemy_recruits:
            if x.sub_type_as_text == "Baboon":
                return x
        if len([x for x in enemy_recruits if x.health > 0]) == 0:
            return None
        random_enemy = battle_state.random.choice([x for x in enemy_recruits if x.health > 0])
        return random_enemy

    def get_completely_random_enemy(self, battle_state: "BattleStateSerializer"):
        enemy_recruits = battle_state.get_battle_info(battle_id=self.battle_id).enemy_recruits
        # check for a baboon on the enemy team
        enemy_recruits = sorted(enemy_recruits, key=lambda x: x.initiative, reverse=True)
        if len([x for x in enemy_recruits if x.health > 0]) == 0:
            return None
        random_enemy = battle_state.random.choice([x for x in enemy_recruits if x.health > 0])
        return random_enemy

    def shop_attack_with_range(self, shop_state: "ShopStateSerializer",
                               state_set: "StateSet",
                               stack_item: "StackItem",
                               animation_event_sequence: AnimationEventSequence,
                               original_run_snapshot: "ShopSnapshotSerializer" = None,
                               damage_type: str = "default",
                               group: Group = None) -> Union["RecruitSerializer", None]:
        pass

    def battle_attack_with_range(self, battle_state: "BattleStateSerializer",
                                 state_set: "StateSet",
                                 stack_item: "StackItem",
                                 animation_event_sequence: AnimationEventSequence,
                                 original_shop_state: "ShopStateSerializer" = None,
                                 damage_type: str = "default",
                                 group: Group = None) -> Union["RecruitSerializer", None]:
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
                                                   original_shop_state=original_shop_state,
                                                   animation_event_sequence=animation_event_sequence,
                                                   origin="ranged")
            elif damage_type == "unblockable":
                random_enemy.battle_receive_unblockable_damage(damage=damage,
                                                               enemy=self,
                                                               state_set=state_set,
                                                               battle_state=battle_state,
                                                               original_shop_state=original_shop_state,
                                                               animation_event_sequence=animation_event_sequence,
                                                               origin="ranged")
            return random_enemy

    def shop_revive(self, shop_state: "ShopStateSerializer",
                    state_set: "StateSet",
                    stack_item: "StackItem",
                    animation_event_sequence: AnimationEventSequence,
                    original_run_snapshot: "ShopSnapshotSerializer" = None):
        pass

    def battle_revive(self, battle_state: "BattleStateSerializer",
                      state_set: "StateSet",
                      stack_item: "StackItem",
                      animation_event_sequence: AnimationEventSequence,
                      original_shop_state: "ShopStateSerializer" = None):
        pass

    def shop_attack_with_melee(self, shop_state: "ShopStateSerializer",
                               state_set: "StateSet",
                               stack_item: "StackItem",
                               animation_event_sequence: AnimationEventSequence,
                               original_run_snapshot: "ShopSnapshotSerializer" = None,
                               damage_type: str = "default"):
        pass

    def battle_attack_with_melee(self, battle_state: "BattleStateSerializer",
                                 state_set: "StateSet",
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
                                                  original_shop_state=original_shop_state,
                                                  animation_event_sequence=animation_event_sequence,
                                                  origin="melee")
            elif damage_type == "unblockable":
                front_enemy.battle_receive_unblockable_damage(damage=damage,
                                                              enemy=self,
                                                              state_set=state_set,
                                                              battle_state=battle_state,
                                                              original_shop_state=original_shop_state,
                                                              animation_event_sequence=animation_event_sequence,
                                                              origin="melee")

            return front_enemy

    def shop_faint(self, shop_state: "ShopStateSerializer",
                   state_set: "StateSet",
                   stack_item: "StackItem",
                   animation_event_sequence: AnimationEventSequence,
                   original_shop_state: "ShopStateSerializer" = None):
        for x in self.listeners.get_listeners(hook=Listeners.Hooks.shop_faint):
            # basically we allow arbitrary other objects to affect the 'fainting' of a unit
            # if that unit is revived it doesn't actually need to faint and thus returns immediately
            should_return = x.lt_shop_faint(
                shop_state=shop_state,
                state_set=state_set,
                stack_item=stack_item,
                animation_event_sequence=animation_event_sequence,
                original_shop_state=original_shop_state
            )
            if should_return:
                return
        e = Animations.Faint(
            state_id=state_set.add_state(state=shop_state),
            shop_id=self.shop_id,
            battle_id=self.battle_id,
        )
        animation_event_sequence.append(e)
        shop_state.revert_to_empty_slot(recruit_index=self.team_index)
        shop_state.queue_ability_for_all_objects(trigger=GameConstants.Opcodes.Stack.shop_friendly_recruit_faints,
                                                 context={"target": self})
        shop_state.stack = deque([x for x in shop_state.stack if x.object.shop_id != self.shop_id])

    def battle_faint(self, battle_state: "BattleStateSerializer",
                     state_set: "StateSet",
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

    def remove_status(self, status: "StatusSerializer"):
        found_index = None
        for i, x in enumerate(self.statuses):
            if x.sub_type_as_int == status.sub_type_as_int:
                found_index = i
                break
        if found_index is None:
            raise Exception(f"Status {status.sub_type_as_text} not found on {self.sub_type_as_text}")
        else:
            self.statuses.pop(found_index)

    def passive_battle_ability(self,
                               battle_state: "BattleStateSerializer",
                               state_set: "StateSet",
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

    def start_of_battle(self,
                        battle_state: "BattleStateSerializer",
                        state_set: "StateSet",
                        stack_item: "StackItem",
                        animation_event_sequence: AnimationEventSequence,
                        original_shop_state: "ShopStateSerializer" = None):
        for x in self.listeners.get_listeners(hook=Listeners.Hooks.start_of_battle):
            # basically we allow arbitrary other objects to affect the 'fainting' of a unit
            # if that unit is revived it doesn't actually need to faint and thus returns immediately
            should_return = x.lt_start_of_battle(
                battle_state=battle_state,
                state_set=state_set,
                stack_item=stack_item,
                animation_event_sequence=animation_event_sequence,
                original_shop_state=original_shop_state
            )
            if should_return:
                return

    def battle_friendly_recruit_faints(self, battle_state: "BattleStateSerializer",
                                       state_set: "StateSet",
                                       stack_item: "StackItem",
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

    def battle_friendly_recruit_summoned(self, battle_state: "BattleStateSerializer",
                                         state_set: "StateSet",
                                         stack_item: "StackItem",
                                         animation_event_sequence: AnimationEventSequence,
                                         original_shop_state: "ShopStateSerializer" = None):
        for x in self.listeners.get_listeners(hook=Listeners.Hooks.battle_friendly_recruit_summoned):
            # basically we allow arbitrary other objects to affect the 'fainting' of a unit
            # if that unit is revived it doesn't actually need to faint and thus returns immediately
            should_return = x.lt_battle_friendly_recruit_summoned(
                battle_state=battle_state,
                state_set=state_set,
                stack_item=stack_item,
                animation_event_sequence=animation_event_sequence,
                original_shop_state=original_shop_state
            )
            if should_return:
                return

    def shop_friendly_recruit_faints(self, shop_state: "ShopStateSerializer",
                                     state_set: "StateSet",
                                     stack_item: "StackItem",
                                     animation_event_sequence: AnimationEventSequence,
                                     original_run_snapshot: "ShopSnapshotSerializer" = None):
        pass

    def shop_friendly_recruit_summoned(self, shop_state: "ShopStateSerializer",
                                       state_set: "StateSet",
                                       stack_item: "StackItem",
                                       animation_event_sequence: AnimationEventSequence,
                                       original_run_snapshot: "ShopSnapshotSerializer" = None):
        pass

    def shop_friendly_recruit_sold(self, shop_state: "ShopStateSerializer",
                                   state_set: "StateSet",
                                   stack_item: "StackItem",
                                   animation_event_sequence: AnimationEventSequence,
                                   original_run_snapshot: "ShopSnapshotSerializer" = None):
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

    def get_status(self, sub_type_as_text: str):
        for status in self.statuses:
            if status.sub_type_as_text == sub_type_as_text:
                return status
        return None

    def add_status(self, status: "StatusSerializer",
                   battle_state: "BattleStateSerializer",
                   state_set: "StateSet",
                   enemy: "RecruitSerializer",
                   animation_event_sequence: AnimationEventSequence,
                   origin: str = "melee",
                   original_shop_state: "ShopStateSerializer" = None,
                   group: Group = None,
                   ):
        for x in self.listeners.get_listeners(hook=Listeners.Hooks.add_status):
            status, should_return = x.lt_add_status(
                status=status,
                battle_state=battle_state,
                enemy=enemy,
                state_set=state_set,
                animation_event_sequence=animation_event_sequence,
                origin=origin,
                original_shop_state=original_shop_state
            )
            if should_return:
                return
        for x in self.statuses:
            if x.sub_type_as_text == status.sub_type_as_text:
                # stack the status if its stackable
                x.stack(other=status, recruit=self,
                        battle_state=battle_state,
                        state_set=state_set,
                        group=group,
                        animation_event_sequence=animation_event_sequence)
                return

        self.statuses.append(status)
        status.on_append(recruit=self, battle_state=battle_state,
                         state_set=state_set,
                         group=group,
                         animation_event_sequence=animation_event_sequence)

    def update_battle_state(self, battle_state: "BattleStateSerializer",
                            state_set: "StateSet",
                            stack_item: "StackItem",
                            animation_event_sequence: AnimationEventSequence,
                            original_shop_state: "ShopStateSerializer" = None):

        friendly_recruits = battle_state.get_battle_info(battle_id=self.battle_id).friendly_recruits
        if friendly_recruits != battle_state.friendly_recruits:
            original_shop_state = None

        # is_chlorotoxin = self.get_status(sub_type_as_text="Chlorotoxin")
        # if is_chlorotoxin is not None and stack_item.op not in [GameConstants.Opcodes.Stack.battle_faint,
        #                                                         GameConstants.Opcodes.Stack.battle_revive,
        #                                                         GameConstants.Opcodes.Stack.status_effect]:
        #     # prevent all abilities immediatly after chlorotoxin, don't animate this because its
        #     return

        if stack_item.op == GameConstants.Opcodes.Stack.battle_attack_with_melee:
            enemy = self.battle_attack_with_melee(battle_state=battle_state,
                                                  state_set=state_set,
                                                  animation_event_sequence=animation_event_sequence,
                                                  stack_item=stack_item, original_shop_state=original_shop_state)
            # Hooks.post_attack_with_melee(self=self, battle_state=battle_state,
            #                              state_set=state_set,
            #                              enemy=enemy,
            #                              animation_event_sequence=animation_event_sequence)
            # Hooks.post_attack(self=enemy,
            #                   battle_state=battle_state,
            #                   state_set=state_set,
            #                   stack_item=stack_item,
            #                   enemy=self,
            #                   animation_event_sequence=animation_event_sequence)
        elif stack_item.op == GameConstants.Opcodes.Stack.passive_battle_ability:
            self.passive_battle_ability(battle_state=battle_state,
                                        state_set=state_set,
                                        animation_event_sequence=animation_event_sequence,
                                        stack_item=stack_item,
                                        original_shop_state=original_shop_state)
        elif stack_item.op == GameConstants.Opcodes.Stack.start_of_battle:
            self.start_of_battle(battle_state=battle_state,
                                 state_set=state_set,
                                 animation_event_sequence=animation_event_sequence,
                                 stack_item=stack_item, original_shop_state=original_shop_state)
        elif stack_item.op == GameConstants.Opcodes.Stack.battle_attack_with_ranged:
            enemy = self.battle_attack_with_range(battle_state=battle_state,
                                                  state_set=state_set,
                                                  animation_event_sequence=animation_event_sequence,
                                                  stack_item=stack_item, original_shop_state=original_shop_state)
            # Hooks.post_attack(self=self,
            #                   battle_state=battle_state,
            #                   state_set=state_set,
            #                   stack_item=stack_item,
            #                   enemy=enemy,
            #                   animation_event_sequence=animation_event_sequence)
        elif stack_item.op == GameConstants.Opcodes.Stack.battle_faint:
            self.battle_faint(battle_state=battle_state,
                              state_set=state_set,
                              animation_event_sequence=animation_event_sequence,
                              stack_item=stack_item, original_shop_state=original_shop_state)
        elif stack_item.op == GameConstants.Opcodes.Stack.status_effect:
            self.update_statuses(battle_state=battle_state,
                                 state_set=state_set,
                                 stack_item=stack_item,
                                 animation_event_sequence=animation_event_sequence,
                                 original_shop_state=original_shop_state)
        elif stack_item.op == GameConstants.Opcodes.Stack.battle_revive:
            self.battle_revive(battle_state=battle_state,
                               state_set=state_set,
                               stack_item=stack_item,
                               animation_event_sequence=animation_event_sequence,
                               original_shop_state=original_shop_state)
        elif stack_item.op == GameConstants.Opcodes.Stack.battle_friendly_recruit_faints:
            self.battle_friendly_recruit_faints(battle_state=battle_state,
                                                state_set=state_set,
                                                stack_item=stack_item,
                                                animation_event_sequence=animation_event_sequence,
                                                original_shop_state=original_shop_state)
        elif stack_item.op == GameConstants.Opcodes.Stack.battle_friendly_recruit_summoned:
            self.battle_friendly_recruit_summoned(battle_state=battle_state,
                                                  state_set=state_set,
                                                  stack_item=stack_item,
                                                  animation_event_sequence=animation_event_sequence,
                                                  original_shop_state=original_shop_state)

    def update_shop_state(self, shop_state: "ShopStateSerializer",
                          state_set: "StateSet",
                          stack_item: "StackItem",
                          animation_event_sequence: AnimationEventSequence,
                          shop_snapshot: "ShopSnapshotSerializer"):

        if stack_item.op == GameConstants.Opcodes.Stack.shop_level_up:
            self.shop_level_up(shop_state=shop_state,
                               state_set=state_set,
                               stack_item=stack_item,
                               animation_event_sequence=animation_event_sequence)
        elif stack_item.op == GameConstants.Opcodes.Stack.shop_end_of_turn:
            self.shop_end_of_turn(shop_state=shop_state,
                                  state_set=state_set,
                                  stack_item=stack_item,
                                  shop_snapshot=shop_snapshot,
                                  animation_event_sequence=animation_event_sequence)
        elif stack_item.op == GameConstants.Opcodes.Stack.shop_start_of_turn:
            self.shop_start_of_turn(shop_state=shop_state,
                                    state_set=state_set,
                                    stack_item=stack_item,
                                    shop_snapshot=shop_snapshot,
                                    animation_event_sequence=animation_event_sequence)
        elif stack_item.op == GameConstants.Opcodes.Stack.shop_gain_experience:
            self.shop_gain_experience(shop_state=shop_state,
                                      state_set=state_set,
                                      stack_item=stack_item,
                                      animation_event_sequence=animation_event_sequence)
        elif stack_item.op == GameConstants.Opcodes.Stack.shop_bought:
            self.shop_bought(shop_state=shop_state,
                             state_set=state_set,
                             stack_item=stack_item,
                             animation_event_sequence=animation_event_sequence)
        elif stack_item.op == GameConstants.Opcodes.Stack.shop_sold:
            self.shop_sold(shop_state=shop_state,
                           state_set=state_set,
                           stack_item=stack_item,
                           animation_event_sequence=animation_event_sequence)
        elif stack_item.op == GameConstants.Opcodes.Stack.shop_roll:
            self.shop_rolled(shop_state=shop_state,
                             state_set=state_set,
                             stack_item=stack_item,
                             animation_event_sequence=animation_event_sequence)
        elif stack_item.op == GameConstants.Opcodes.Stack.shop_friendly_recruit_summoned:
            self.shop_friendly_recruit_summoned(shop_state=shop_state,
                                                state_set=state_set,
                                                stack_item=stack_item,
                                                animation_event_sequence=animation_event_sequence)
        elif stack_item.op == GameConstants.Opcodes.Stack.shop_faint:
            self.shop_faint(shop_state=shop_state,
                            state_set=state_set,
                            stack_item=stack_item,
                            animation_event_sequence=animation_event_sequence)
        elif stack_item.op == GameConstants.Opcodes.Stack.shop_friendly_recruit_sold:
            self.shop_friendly_recruit_sold(shop_state=shop_state,
                                            state_set=state_set,
                                            stack_item=stack_item,
                                            animation_event_sequence=animation_event_sequence)

    def get_logical_level(self):
        return ExperienceLevelMap.map[self.experience]

    def __str__(self):
        sub_type = self.sub_type_as_text.ljust(30)
        stats = f"{self.melee_attack}/{self.ranged_attack}/{self.armor}/{self.health}/{self.max_health}".ljust(20)
        return f"{sub_type} {stats} {self.initiative} {self.experience} lvl={self.get_logical_level()} sid={self.shop_id} bid={self.battle_id} {self.statuses} {self.custom_data}"
