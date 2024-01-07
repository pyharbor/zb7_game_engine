import base64
import json
from typing import List

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.ExperienceMap import ExperienceLevelMap
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from typing import List, TYPE_CHECKING, Union

from zb7_game_engine.runtime.objects.base.BaseAbility import BaseAbility
from zb7_game_engine.runtime.objects.base.BaseListener import BaseListener
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


class BaseRelic(BaseListener):
    def __init__(self,
                 sub_type_as_int: int = None,
                 sub_type_as_text: str = None,
                 initiative: float = None,
                 experience: int = 1,
                 cost: int = None,
                 aaid: int = 0,
                 triggers: List[str] = None,
                 shop_id: int = None,
                 battle_id: int = None,
                 random_seed=None,
                 custom_data=None,
                 options=None,
                 bit_index: int = None,
                 ability: list = None,
                 rarity: str = None,
                 type: str = None,
                 arts: list = None,
                 stack_order_number: int = None,
                 ):
        self.sub_type_as_int: int = sub_type_as_int
        self.sub_type_as_text: str = sub_type_as_text
        if self.sub_type_as_text == "GraduationCap":
            pass
        immutable_data = ImmutableData.Subtype.from_int(sub_type_as_int)
        self._initiative: float
        self._experience: int
        self._cost: int
        self._aaid: int
        if initiative is None:
            self.initiative = round(
                immutable_data["initiative"] + ImmutableData.Initiative.get_random_intiative(), 3)
        else:
            self.initiative = initiative
        if experience is None:
            self.experience = 0
        else:
            self.experience = experience

        if cost is None:
            self.cost = immutable_data["cost"]
        else:
            self.cost = cost

        self.aaid = aaid
        self.triggers: List[str] = triggers or immutable_data["triggers"]
        self.shop_id: int = shop_id
        self.battle_id: int = battle_id
        self.random_seed = random_seed
        self.custom_data = custom_data or {}
        self.options = options or immutable_data.get("options", [])
        self.bit_index = bit_index or immutable_data["bit_index"]
        self.ability = immutable_data["ability"] or ability
        if self.ability:
            self.ability: List[BaseAbility] = [BaseAbility(**x) for x in self.ability]
        self.rarity = rarity or immutable_data["rarity"]
        self.type = type or immutable_data["type"]
        self.arts = arts or immutable_data["arts"]
        self.probability = GameConstants.Rarity.rarity_to_probability_map[self.rarity]
        self.stack_order_number = immutable_data.get("stack_order_number")
        self.default_triggers = []
        try:
            ImmutableData.Initiative.to_int(self.initiative)
        except KeyError:
            raise ValueError(f"Invalid initiative value: {self.initiative}")

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
    def aaid(self):
        return self._aaid

    @aaid.setter
    def aaid(self, value):
        if 0 <= value <= 256:
            self._aaid = value
        else:
            raise ValueError(f"Invalid aaid value: {value}")

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
        raise NotImplementedError()

    def battle_level_up(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                        animation_event_sequence: AnimationEventSequence):
        raise NotImplementedError()

    def shop_set_object_data(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                             user_input: "ShopUserInput", animation_event_sequence: AnimationEventSequence,
                             original_shop_snapshot: "ShopSnapshotSerializer" = None):
        if user_input.set_shop_object_data_opcode == GameConstants.Opcodes.ObjectData.shop_set_aaid:
            if not isinstance(user_input.target_object, int):
                raise Exception("Art ID must be an int")
            if 0 > user_input.target_object or user_input.target_object >= 256:
                raise Exception("Art ID must be between 0 and 256")
            self.aaid = user_input.target_object

    def shop_gain_experience(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                             animation_event_sequence: AnimationEventSequence):
        raise NotImplementedError()

    def battle_gain_experience(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                               animation_event_sequence: AnimationEventSequence):
        raise NotImplementedError()

    def battle_before_everything(self, battle_state: "BattleStateSerializer", state_set: "StateSet",
                                 stack_item: "StackItem", animation_event_sequence: AnimationEventSequence,
                                 original_shop_state: "ShopStateSerializer" = None):
        pass

    def shop_start_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                           animation_event_sequence: AnimationEventSequence):
        pass

    def shop_friendly_recruit_summoned(self, shop_state: "ShopStateSerializer", state_set: "StateSet",
                                       stack_item: "StackItem", animation_event_sequence: AnimationEventSequence):
        pass

    def shop_friendly_recruit_sold(self, shop_state: "ShopStateSerializer",
                                   state_set: "StateSet",
                                   stack_item: "StackItem",
                                   animation_event_sequence: AnimationEventSequence,
                                   original_run_snapshot: "ShopSnapshotSerializer" = None):
        raise NotImplementedError()

    def shop_end_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                         animation_event_sequence: AnimationEventSequence):
        pass

    def battle_heal(self, heal: int, battle_state: "BattleStateSerializer", state_set: "StateSet",
                    healer: Union["RecruitSerializer", "RelicSerializer", "StatusSerializer"],
                    animation_event_sequence: AnimationEventSequence):
        self.health = min(int(self.health + heal), self.max_health)

    def battle_receive_damage(self, damage: int,
                              battle_state: "BattleStateSerializer",
                              enemy: "BaseRecruit",
                              state_set: "StateSet",
                              animation_event_sequence: AnimationEventSequence,
                              origin: str = "melee",
                              original_shop_state: "ShopStateSerializer" = None,
                              damage_reduction_stack: list[dict] = None
                              ) -> int:
        pass

    def battle_receive_unblockable_damage(self, damage: int,
                                          battle_state: "BattleStateSerializer",
                                          enemy: "BaseRecruit",
                                          animation_event_sequence: AnimationEventSequence,
                                          state_set: "StateSet",
                                          origin: str = "melee",
                                          group=None,
                                          original_shop_state: "ShopStateSerializer" = None
                                          ) -> int:
        pass

    def battle_debuff_stats(self,
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
                            group=None):
        pass

    def battle_buff_stats(self, battle_state: "BattleStateSerializer",
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
                          group=None):

        pass

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
        for x in enemy_recruits:
            if x.sub_type_as_text == "Baboon":
                return x
            elif x.sub_type_as_text == "AnglerFish":
                try:
                    target = enemy_recruits[x.team_index - 1]
                    return target
                except IndexError:
                    pass
        if len([x for x in enemy_recruits if x.health > 0]) == 0:
            return None
        random_enemy = battle_state.random.choice([x for x in enemy_recruits if x.health > 0])
        return random_enemy

    def passive_battle_ability(self,
                               battle_state: "BattleStateSerializer",
                               state_set: "StateSet",
                               stack_item: "StackItem",
                               animation_event_sequence: AnimationEventSequence,
                               original_shop_state: "ShopStateSerializer" = None):
        pass

    def start_of_battle(self,
                        battle_state: "BattleStateSerializer",
                        state_set: "StateSet",
                        stack_item: "StackItem",
                        animation_event_sequence: AnimationEventSequence,
                        original_run_snapshot: "ShopStateSerializer" = None):
        pass

    def battle_friendly_recruit_faints(self, battle_state: "BattleStateSerializer",
                                       state_set: "StateSet",
                                       stack_item: "StackItem",
                                       animation_event_sequence: AnimationEventSequence,
                                       original_shop_state: "ShopStateSerializer" = None):
        pass

    def battle_friendly_recruit_summoned(self, battle_state: "BattleStateSerializer",
                                         state_set: "StateSet",
                                         stack_item: "StackItem",
                                         animation_event_sequence: AnimationEventSequence,
                                         original_shop_state: "ShopStateSerializer" = None):
        pass

    def shop_player_decision(self, shop_state: "ShopStateSerializer",
                             state_set: "StateSet",
                             stack_item: "StackItem",
                             animation_event_sequence: AnimationEventSequence,
                             original_run_snapshot: "ShopSnapshotSerializer" = None):
        pass

    def update_battle_state(self, battle_state: "BattleStateSerializer",
                            state_set: "StateSet",
                            stack_item: "StackItem",
                            animation_event_sequence: AnimationEventSequence,
                            original_shop_state: "ShopStateSerializer" = None):

        friendly_recruits = battle_state.get_battle_info(battle_id=self.battle_id).friendly_recruits
        if friendly_recruits != battle_state.friendly_recruits:
            original_run_snapshot = None

        if stack_item.op == GameConstants.Opcodes.Stack.passive_battle_ability:
            self.passive_battle_ability(battle_state=battle_state,
                                        state_set=state_set,
                                        animation_event_sequence=animation_event_sequence,
                                        stack_item=stack_item, original_shop_state=original_shop_state)
        elif stack_item.op == GameConstants.Opcodes.Stack.start_of_battle:
            self.start_of_battle(battle_state=battle_state,
                                 state_set=state_set,
                                 animation_event_sequence=animation_event_sequence,
                                 stack_item=stack_item, original_run_snapshot=original_shop_state)
        elif stack_item.op == GameConstants.Opcodes.Stack.shop_friendly_recruit_faints:
            self.battle_friendly_recruit_faints(battle_state=battle_state,
                                                state_set=state_set,
                                                stack_item=stack_item,
                                                animation_event_sequence=animation_event_sequence,
                                                original_shop_state=original_shop_state)
        elif stack_item.op == GameConstants.Opcodes.Stack.shop_friendly_recruit_summoned:
            self.battle_friendly_recruit_summoned(battle_state=battle_state,
                                                  state_set=state_set,
                                                  stack_item=stack_item,
                                                  animation_event_sequence=animation_event_sequence,
                                                  original_shop_state=original_shop_state)

    def update_shop_state(self, shop_state: "ShopStateSerializer",
                          state_set: "StateSet",
                          stack_item: "StackItem",
                          animation_event_sequence: AnimationEventSequence,
                          shop_snapshot: "ShopSnapshotSerializer" = None):

        if stack_item.op == GameConstants.Opcodes.Shop.shop_level_up:
            self.shop_level_up(shop_state=shop_state,
                               state_set=state_set,
                               stack_item=stack_item,
                               animation_event_sequence=animation_event_sequence)
        elif stack_item.op == GameConstants.Opcodes.Shop.shop_end_of_turn:
            self.shop_end_of_turn(shop_state=shop_state,
                                  state_set=state_set,
                                  stack_item=stack_item,
                                  animation_event_sequence=animation_event_sequence)
        elif stack_item.op == GameConstants.Opcodes.Shop.shop_start_of_turn:
            self.shop_start_of_turn(shop_state=shop_state,
                                    state_set=state_set,
                                    stack_item=stack_item,
                                    animation_event_sequence=animation_event_sequence)
        elif stack_item.op == GameConstants.Opcodes.Shop.shop_gain_experience:
            self.shop_gain_experience(shop_state=shop_state,
                                      state_set=state_set,
                                      stack_item=stack_item,
                                      animation_event_sequence=animation_event_sequence)
        elif stack_item.op == GameConstants.Opcodes.Shop.shop_bought:
            self.shop_bought(shop_state=shop_state,
                             state_set=state_set,
                             stack_item=stack_item,
                             animation_event_sequence=animation_event_sequence,
                             shop_snapshot=shop_snapshot)
        elif stack_item.op == GameConstants.Opcodes.Shop.shop_sold:
            self.shop_sold(shop_state=shop_state,
                           state_set=state_set,
                           stack_item=stack_item,
                           animation_event_sequence=animation_event_sequence)
        elif stack_item.op == GameConstants.Opcodes.Shop.shop_roll:
            self.shop_rolled(shop_state=shop_state,
                             state_set=state_set,
                             stack_item=stack_item,
                             animation_event_sequence=animation_event_sequence)
        elif stack_item.op == GameConstants.Opcodes.Shop.shop_friendly_recruit_summoned:
            self.shop_friendly_recruit_summoned(shop_state=shop_state,
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
        return f"{self.sub_type_as_text.ljust(30)} {self.shop_id}"
