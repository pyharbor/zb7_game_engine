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


class KomodoDragon(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=243,
                         sub_type_as_text="KomodoDragon", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def battle_attack_with_melee(self, battle_state: "BattleStateSerializer",
                                 state_set: StateSet,
                                 stack_item: "StackItem",
                                 animation_event_sequence: AnimationEventSequence,
                                 original_shop_state: "ShopStateSerializer" = None,
                                 damage_type: str = "default"):
        if self.team_index == 0:
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
            front_enemy.battle_receive_damage(damage=damage,
                                              enemy=self,
                                              state_set=state_set,
                                              battle_state=battle_state,
                                              animation_event_sequence=animation_event_sequence,
                                              origin="melee")
            amount = 10
            if self.experience < GameConstants.Levels.level_2:
                amount = 10
            elif self.experience < GameConstants.Levels.level_3:
                amount = 20
            elif self.experience < GameConstants.Levels.level_4:
                amount = 30
            elif self.experience < GameConstants.Levels.level_5:
                amount = 40
            else:
                amount = 50
            front_enemy.add_status(status=Statuses.Bacteria(counter=amount),
                                   state_set=state_set,
                                   battle_state=battle_state,
                                   animation_event_sequence=animation_event_sequence,
                                   enemy=self)
            return front_enemy

    def battle_attack_with_range(self, battle_state: "BattleStateSerializer",
                                 state_set: StateSet,
                                 stack_item: "StackItem",
                                 animation_event_sequence: AnimationEventSequence,
                                 original_shop_state: "ShopStateSerializer" = None,
                                 damage_type: str = "default",
                                 group=None) -> Union["RecruitSerializer", None]:
        if self.team_index != 0:
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

            amount = 10
            if self.experience < GameConstants.Levels.level_2:
                amount = 10
            elif self.experience < GameConstants.Levels.level_3:
                amount = 20
            elif self.experience < GameConstants.Levels.level_4:
                amount = 30
            elif self.experience < GameConstants.Levels.level_5:
                amount = 40
            else:
                amount = 50
            random_enemy.add_status(status=Statuses.Bacteria(counter=amount),
                                    state_set=state_set,
                                    battle_state=battle_state,
                                    animation_event_sequence=animation_event_sequence,
                                    enemy=self)
            return random_enemy

    def shop_end_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                         animation_event_sequence: AnimationEventSequence,
                         shop_snapshot: "ShopSnapshotSerializer" = None):
        self.generic_ability_notification(
            state=shop_state,
            state_set=state_set,
            animation_event_sequence=animation_event_sequence)
        g = Group()
        targets = []
        if self.experience >= GameConstants.Levels.level_2:
            for i in range(1, 3):
                try:
                    targets.append(shop_state.friendly_recruits[self.team_index - i])
                except IndexError as e:
                    pass
                try:
                    targets.append(shop_state.friendly_recruits[self.team_index + i])
                except IndexError as e:
                    pass
        else:
            try:
                targets.append(shop_state.friendly_recruits[self.team_index - 1])
            except IndexError as e:
                pass
            try:
                targets.append(shop_state.friendly_recruits[self.team_index + 1])
            except IndexError as e:
                pass
        for x in targets:
            if GameConstants.ScientificNames.Reptilia in x.binomial_nomenclature:
                    x.shop_buff_stats(melee=3,
                                      ranged=3,
                                      health=3,
                                      max_health=3,
                                      shop_state=shop_state,
                                      state_set=state_set,
                                      stack_item=stack_item, buffer=self,
                                      animation_event_sequence=animation_event_sequence,
                                      group=g)
        g.set_state_id(state_id=state_set.add_state(state=shop_state))
        animation_event_sequence.append(g)

