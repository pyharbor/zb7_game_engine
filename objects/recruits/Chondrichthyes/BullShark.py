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


class BullShark(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=61,
                         sub_type_as_text="BullShark", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
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
            temporary_armor_reduction = 0
            if self.experience < GameConstants.Levels.level_2:
                temporary_armor_reduction = 25
            elif self.experience < GameConstants.Levels.level_3:
                temporary_armor_reduction = 50
            elif self.experience < GameConstants.Levels.level_4:
                temporary_armor_reduction = 75
            else:
                temporary_armor_reduction = 100

            original_armor_value = front_enemy.armor
            e = Animations.MeleeAttack(
                state_id=state_set.add_state(state=battle_state),
                shop_id=self.shop_id,
                battle_id=self.battle_id,
                target_battle_id=front_enemy.battle_id,
                target_shop_id=front_enemy.shop_id,
                amount=damage,
            )
            animation_event_sequence.append(e)
            front_enemy.armor = max(0, front_enemy.armor - temporary_armor_reduction)
            front_enemy.battle_receive_damage(damage=damage,
                                              enemy=self,
                                              state_set=state_set,
                                              battle_state=battle_state,
                                              animation_event_sequence=animation_event_sequence,
                                              origin="melee")

            front_enemy.armor = original_armor_value
            return front_enemy

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

            temporary_armor_reduction = 0
            if self.experience < GameConstants.Levels.level_2:
                temporary_armor_reduction = 25
            elif self.experience < GameConstants.Levels.level_3:
                temporary_armor_reduction = 50
            elif self.experience < GameConstants.Levels.level_4:
                temporary_armor_reduction = 75
            else:
                temporary_armor_reduction = 100

            original_armor_value = random_enemy.armor
            e = Animations.RangedAttack(
                state_id=None,
                shop_id=self.shop_id,
                battle_id=self.battle_id,
                target_battle_id=random_enemy.battle_id,
                target_shop_id=random_enemy.shop_id,
                amount=damage,
            )
            animation_event_sequence.append(e)
            random_enemy.armor = max(0, random_enemy.armor - temporary_armor_reduction)
            random_enemy.battle_receive_damage(damage=damage,
                                               enemy=self,
                                               state_set=state_set,
                                               battle_state=battle_state,
                                               animation_event_sequence=animation_event_sequence,
                                               origin="ranged")
            random_enemy.armor = original_armor_value
            return random_enemy

