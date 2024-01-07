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


class MacaroniPenguin(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=237,
                         sub_type_as_text="MacaroniPenguin", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------
        self.counter = 0

        
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
        self.counter += 1
        if self.experience < GameConstants.Levels.level_2:
            if self.counter % 4 == 0:
                self.add_status(Statuses.Diving(counter=1), battle_state=battle_state, state_set=state_set,
                                animation_event_sequence=animation_event_sequence,
                                enemy=None)
        elif self.experience < GameConstants.Levels.level_3:
            if self.counter % 3 == 0:
                self.add_status(Statuses.Diving(counter=1), battle_state=battle_state, state_set=state_set,
                                animation_event_sequence=animation_event_sequence,
                                enemy=None)
        else:
            if self.counter % 2 == 0:
                self.add_status(Statuses.Diving(counter=1), battle_state=battle_state, state_set=state_set,
                                animation_event_sequence=animation_event_sequence,
                                enemy=None)

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
        self.add_status(Statuses.Diving(counter=1), battle_state=battle_state, state_set=state_set,
                        animation_event_sequence=animation_event_sequence,
                        enemy=None)

    def battle_receive_damage(self, damage: int,
                              battle_state: "BattleStateSerializer",
                              enemy: "RecruitSerializer",
                              state_set: StateSet,
                              animation_event_sequence: AnimationEventSequence,
                              origin: str = "melee",
                              original_shop_state: "ShopStateSerializer" = None,
                              damage_reduction_stack: list[dict] = None
                              ) -> int:
        overkill = super().battle_receive_damage(damage, battle_state, enemy, state_set, animation_event_sequence,
                                                 origin, original_shop_state, damage_reduction_stack)
        if self.health <= 0:
            info = battle_state.get_battle_info(battle_id=self.battle_id)
            emperor_penguin = len([x for x in info.friendly_recruits if x.sub_type_as_text == "EmperorPenguin"]) >= 1
            if emperor_penguin:
                self.generic_ability_notification(
                    state_set=state_set,
                    description="for the the emperor!",
                    animation_event_sequence=animation_event_sequence,
                    state=battle_state
                )
                self.health = 1
                # pop the faint stack item
                battle_state.stack.popleft()
        return overkill

    def shop_receive_damage(self, damage: int,
                            shop_state: "ShopStateSerializer",
                            enemy: "RecruitSerializer",
                            state_set: StateSet,
                            animation_event_sequence: AnimationEventSequence,
                            origin: str = "melee",
                            original_shop_state: "ShopSnapshotSerializer" = None,
                            damage_reduction_stack: list[dict] = None
                            ) -> int:
        overkill = super().shop_receive_damage(damage, shop_state, enemy, state_set, animation_event_sequence,
                                                 origin, original_shop_state, damage_reduction_stack)
        if self.health <= 0:
            emperor_penguin = len([x for x in shop_state.friendly_recruits if x.sub_type_as_text == "EmperorPenguin"]) >= 1
            if emperor_penguin:
                self.generic_ability_notification(
                    state_set=state_set,
                    description="for the the emperor!",
                    animation_event_sequence=animation_event_sequence,
                    state=shop_state
                )
                self.health = 1
                # pop the faint stack item
                shop_state.stack.popleft()
        return overkill

