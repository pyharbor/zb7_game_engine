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


class Walrus(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=35,
                         sub_type_as_text="Walrus", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def battle_receive_damage(self, damage: int,
                              battle_state: "BattleStateSerializer",
                              enemy: "RecruitSerializer",
                              state_set: StateSet,
                              animation_event_sequence: AnimationEventSequence,
                              origin: str = "melee",
                              original_shop_state: "ShopStateSerializer" = None,
                              damage_reduction_stack: list[dict] = None
                              ) -> int:
        if damage_reduction_stack is None:
            damage_reduction_stack = [
                dict(amount=damage, sub_type_as_int=GameConstants.DamageReductionStack.UnModifiedDamage)]
        prevented_damage = 0
        info = battle_state.get_battle_info(battle_id=self.battle_id)
        count = len([x for x in info.friendly_recruits if GameConstants.ScientificNames.Pinnipedia in x.binomial_nomenclature])
        count += len([x for x in info.friendly_recruits if GameConstants.Habitats.Arctic in x.binomial_nomenclature])
        if self.experience < GameConstants.Levels.level_2:
            amount = count
        elif self.experience < GameConstants.Levels.level_3:
            amount = count * 2
        else:
            amount = count * 6
        original_damage = damage
        damage = max(0, damage - amount)
        prevented_damage = original_damage - damage
        damage_reduction_stack.append(
            dict(amount=prevented_damage, sub_type_as_int=GameConstants.DamageReductionStack.FattyTissue)
        )
        return super().battle_receive_damage(damage, battle_state, enemy, state_set, animation_event_sequence,
                                             origin, original_shop_state, damage_reduction_stack)

    def shop_end_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                         animation_event_sequence: AnimationEventSequence,
                         shop_snapshot: "ShopSnapshotSerializer" = None):
        buff = 4
        self.generic_ability_notification(
            state=shop_state,
            state_set=state_set,
            animation_event_sequence=animation_event_sequence)
        g = Group()
        for x in shop_state.friendly_recruits:
            if GameConstants.Habitats.Arctic in x.binomial_nomenclature:
                x.shop_buff_stats(
                    shop_state=shop_state,
                    state_set=state_set,
                    stack_item=stack_item,
                    animation_event_sequence=animation_event_sequence,
                    health=buff,
                    max_health=buff,
                    group=g
                )
        if len(g.animation_events) > 0:
            g.set_state_id(state_id=state_set.add_state(state=shop_state))
            animation_event_sequence.append(g)

    def battle_attack_with_melee(self, battle_state: "BattleStateSerializer",
                                 state_set: StateSet,
                                 stack_item: "StackItem",
                                 animation_event_sequence: AnimationEventSequence,
                                 original_shop_state: "ShopStateSerializer" = None,
                                 damage_type: str = "default"):
        if self.experience > GameConstants.Levels.level_4:
            damage = self.health
        else:
            damage = self.ranged_attack
        if self.team_index == 0 and damage > 0:
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

    def battle_attack_with_range(self, battle_state: "BattleStateSerializer",
                                 state_set: StateSet,
                                 stack_item: "StackItem",
                                 animation_event_sequence: AnimationEventSequence,
                                 original_shop_state: "ShopStateSerializer" = None,
                                 damage_type: str = "default",
                                 group=None) -> Union["RecruitSerializer", None]:
        if self.experience > GameConstants.Levels.level_4:
            damage = self.health
        else:
            damage = self.ranged_attack
        if self.team_index != 0 and damage > 0:
            random_enemy = self.get_random_enemy(battle_state=battle_state)
            if random_enemy is None:
                return
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

