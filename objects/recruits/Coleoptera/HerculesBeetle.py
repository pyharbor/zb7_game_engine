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


class HerculesBeetle(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=119,
                         sub_type_as_text="HerculesBeetle", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------
        if 'kill_counter' not in self.custom_data:
            self.custom_data['kill_counter'] = 0

        
    def start_of_battle(self,
                        battle_state: "BattleStateSerializer",
                        state_set: "StateSet",
                        stack_item: "StackItem",
                        animation_event_sequence: AnimationEventSequence,
                        original_shop_state: "ShopStateSerializer" = None):
        self.generic_ability_notification(
            state_set=state_set,
            animation_event_sequence=animation_event_sequence,
            state=battle_state
        )
        carapace_counters = 0
        info = battle_state.get_battle_info(battle_id=self.battle_id)
        for x in info.friendly_recruits:
            s = x.get_status(sub_type_as_text="Carapace")
            if s is not None:
                carapace_counters += s.counter
        boost = 0.0
        if self.experience < GameConstants.Levels.level_2:
            boost = 1.02 ** carapace_counters
        elif self.experience < GameConstants.Levels.level_3:
            boost = 1.04 ** carapace_counters
        else:
            boost = 1.06 ** carapace_counters

        increased = self.melee_attack * boost
        melee_diff = increased - self.melee_attack
        increased = self.ranged_attack * boost
        ranged_diff = increased - self.ranged_attack
        self.battle_buff_stats(
            battle_state=battle_state,
            animation_event_sequence=animation_event_sequence,
            state_set=state_set,
            stack_item=stack_item,
            melee=int(melee_diff),
            ranged=int(ranged_diff)
        )

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
            if self.custom_data['kill_counter'] >= 15:
                self.generic_ability_notification(
                    state=battle_state,
                    description="rally",
                    state_set=state_set,
                    animation_event_sequence=animation_event_sequence)
                front_enemies = enemy_recruits[0:2]
            else:
                front_enemies = enemy_recruits[0:1]

            for x in front_enemies:
                for x2 in self.listeners.get_listeners(hook=Listeners.Hooks.battle_attack_with_melee):
                    # basically we allow arbitrary other objects to affect the 'fainting' of a unit
                    # if that unit is revived it doesn't actually need to faint and thus returns immediately
                    damage, should_return = x2.lt_battle_attack_with_melee(
                        battle_state=battle_state,
                        damage=damage,
                        enemy=x2,
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
                target_battle_id=front_enemies[0].battle_id,
                target_shop_id=front_enemies[0].shop_id,
                amount=damage,
            )
            animation_event_sequence.append(e)
            if damage_type == "default":
                for x in front_enemies:
                    x.battle_receive_damage(damage=damage,
                                            enemy=self,
                                            state_set=state_set,
                                            battle_state=battle_state,
                                            animation_event_sequence=animation_event_sequence,
                                            origin="melee")
            elif damage_type == "unblockable":
                for x in front_enemies:
                    x.battle_receive_unblockable_damage(damage=damage,
                                                        enemy=self,
                                                        state_set=state_set,
                                                        battle_state=battle_state,
                                                        animation_event_sequence=animation_event_sequence,
                                                        origin="melee")
            friendly_shop_ids = [x.shop_id for x in battle_state.get_battle_info(battle_id=self.battle_id).friendly_recruits]
            for x in front_enemies:
                if x.health <= 0:
                    self.custom_data['kill_counter'] = min(255, self.custom_data['kill_counter'] + 1)
                    if original_shop_state is not None:
                        # for x in original_shop_state.friendly_recruits:
                        #     if x.shop_id in friendly_shop_ids:
                        #         x.melee_attack += 1
                        #         x.ranged_attack += 1
                        #         if x.battle_id in battle_state.info_by_battle_id:
                        #             x.battle_buff_stats(
                        #                 battle_state=battle_state,
                        #                 state_set=state_set,
                        #                 stack_item=stack_item,
                        #                 animation_event_sequence=animation_event_sequence,
                        #                 original_shop_state=original_shop_state,
                        #                 melee=1,
                        #                 ranged=1
                        #             )
                        original = original_shop_state.get_object_from_shop_id(shop_id=self.shop_id)
                        self.custom_data['kill_counter'] = min(255, self.custom_data['kill_counter'] + 1)
                        if self.custom_data['kill_counter'] == 15:
                            melee_attack = original.melee_attack
                            ranged_attack = original.ranged_attack
                            health = original.health
                            max_health = original.max_health
                            initiative = original.initiative
                            armor = original.armor
                            original.melee_attack += melee_attack
                            original.ranged_attack += ranged_attack
                            original.health += health
                            original.max_health += max_health
                            original.initiative += int(initiative)
                            original.initiative = round(original.initiative, 3)
                            original.armor += armor
                            self.battle_buff_stats(
                                battle_state=battle_state,
                                state_set=state_set,
                                stack_item=stack_item,
                                animation_event_sequence=animation_event_sequence,
                                original_shop_state=original_shop_state,
                                melee=melee_attack,
                                ranged=ranged_attack,
                                health=health,
                                max_health=max_health,
                                initiative=int(initiative),
                                armor=armor
                            )

            return front_enemies[0]

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
            if random_enemy.health <= 0:
                self.custom_data['kill_counter'] = min(255, self.custom_data['kill_counter'] + 1)
                if original_shop_state is not None:
                    original = original_shop_state.get_object_from_shop_id(shop_id=self.shop_id)
                    self.custom_data['kill_counter'] = min(255, self.custom_data['kill_counter'] + 1)
                    if self.custom_data['kill_counter'] == 15:
                        melee_attack = original.melee_attack
                        ranged_attack = original.ranged_attack
                        health = original.health
                        max_health = original.max_health
                        initiative = original.initiative
                        armor = original.armor
                        original.melee_attack += melee_attack
                        original.ranged_attack += ranged_attack
                        original.health += health
                        original.max_health += max_health
                        original.armor += armor
                        original.initiative = round(original.initiative, 3)
                        self.battle_buff_stats(
                            battle_state=battle_state,
                            state_set=state_set,
                            stack_item=stack_item,
                            animation_event_sequence=animation_event_sequence,
                            original_shop_state=original_shop_state,
                            melee=melee_attack,
                            ranged=ranged_attack,
                            health=health,
                            max_health=max_health,
                            initiative=int(initiative),
                            armor=armor
                        )

            return random_enemy

    @classmethod
    def bytes_to_custom_data(cls, _bytes: bytes, current_index: int) -> dict:
        return Uint8Counter.bytes_to_custom_data(_bytes=_bytes, current_index=current_index, key="kill_counter")

    def custom_data_to_bytes(self) -> bytes:
        return Uint8Counter.custom_data_to_bytes(self, key="kill_counter")

