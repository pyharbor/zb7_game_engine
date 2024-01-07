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


class BlackClawedCrab(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=18,
                         sub_type_as_text="BlackClawedCrab", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def battle_attack_with_melee(self, battle_state: "BattleStateSerializer",
                                 state_set: StateSet,
                                 stack_item: "StackItem",
                                 animation_event_sequence: AnimationEventSequence,
                                 original_shop_state: "ShopStateSerializer" = None,
                                 damage_type: str = "default"):
        if self.team_index == 0 and self.melee_attack > 0:
            front_enemy = super().battle_attack_with_melee(battle_state=battle_state,
                                                           state_set=state_set,
                                                           stack_item=stack_item,
                                                           animation_event_sequence=animation_event_sequence,
                                                           original_shop_state=original_shop_state,
                                                           damage_type=damage_type)

            armor_reduction = 0
            if self.experience < GameConstants.Levels.level_2:
                armor_reduction = int(self.melee_attack / 4)
            elif self.experience < GameConstants.Levels.level_3:
                armor_reduction = int(self.melee_attack / 3)
            elif self.experience < GameConstants.Levels.level_4:
                armor_reduction = int(self.melee_attack / 2)
            else:
                armor_reduction = int(self.melee_attack)
            if front_enemy is not None:
                front_enemy.battle_debuff_stats(
                    battle_state=battle_state,
                    stack_item=stack_item,
                    state_set=state_set,
                    animation_event_sequence=animation_event_sequence,
                    original_shop_state=original_shop_state,
                    armor=armor_reduction
                )

            return front_enemy

    def battle_attack_with_range(self, battle_state: "BattleStateSerializer",
                                 state_set: StateSet,
                                 stack_item: "StackItem",
                                 animation_event_sequence: AnimationEventSequence,
                                 original_shop_state: "ShopStateSerializer" = None,
                                 damage_type: str = "default",
                                 group=None) -> Union["RecruitSerializer", None]:
        if self.team_index != 0 and self.ranged_attack > 0:
            random_enemy = super().battle_attack_with_range(battle_state=battle_state,
                                                            state_set=state_set,
                                                            stack_item=stack_item,
                                                            animation_event_sequence=animation_event_sequence,
                                                            original_shop_state=original_shop_state,
                                                            damage_type=damage_type)

            armor_reduction = 0
            if self.experience < GameConstants.Levels.level_2:
                armor_reduction = int(self.melee_attack / 4)
            elif self.experience < GameConstants.Levels.level_3:
                armor_reduction = int(self.melee_attack / 3)
            elif self.experience < GameConstants.Levels.level_4:
                armor_reduction = int(self.melee_attack / 2)
            else:
                armor_reduction = int(self.melee_attack)
            if random_enemy is not None:
                random_enemy.battle_debuff_stats(
                    battle_state=battle_state,
                    stack_item=stack_item,
                    state_set=state_set,
                    animation_event_sequence=animation_event_sequence,
                    original_shop_state=original_shop_state,
                    armor=armor_reduction
                )

            return random_enemy

    def battle_receive_damage(self, damage: int,
                              battle_state: "BattleStateSerializer",
                              enemy: "RecruitSerializer",
                              state_set: StateSet,
                              animation_event_sequence: AnimationEventSequence,
                              origin: str = "melee",
                              original_shop_state: "ShopStateSerializer" = None,
                              damage_reduction_stack: list[dict] = None
                              ) -> int:
        health_before = self.health
        overkill = super().battle_receive_damage(damage, battle_state, enemy, state_set, animation_event_sequence,
                                                 origin, original_shop_state, damage_reduction_stack)

        health_after = self.health
        if health_before == health_after:
            info = battle_state.get_battle_info(self.battle_id)
            if info.friendly_recruits == battle_state.friendly_recruits:
                buff = 1 if self.experience < GameConstants.Levels.level_4 else 2
                g = Group()
                info = battle_state.get_battle_info(battle_id=self.battle_id)
                for x in info.friendly_recruits:
                    x.battle_buff_stats(battle_state=battle_state,
                                        stack_item=None,
                                        state_set=state_set,
                                        animation_event_sequence=animation_event_sequence,
                                        original_shop_state=original_shop_state,
                                        health=buff,
                                        max_health=buff,
                                        group=g)
                g.set_state_id(state_id=state_set.add_state(battle_state))
                animation_event_sequence.append(g)
                if battle_state.original_shop_state is not None:
                    for x in battle_state.original_shop_state.friendly_recruits:
                        x.health += buff
                        x.max_health += buff

        return overkill

