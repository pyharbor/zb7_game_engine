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


class ElectricEel(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=226,
                         sub_type_as_text="ElectricEel", 
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
        logical_level = self.get_logical_level()
        if logical_level < 3:
            target_count = 1
            turn_trigger = 3
        elif 3 <= logical_level < 5:
            target_count = 2
            turn_trigger = 2
        else:
            target_count = 3
            turn_trigger = 2
        if self.counter % turn_trigger == 0:
            self.generic_ability_notification(
                state_set=state_set,
                animation_event_sequence=animation_event_sequence,
                state=battle_state
            )
            info = battle_state.get_battle_info(battle_id=self.battle_id)
            e = Group()

            for i in range(target_count):
                x: RecruitSerializer = random_engine.choice(_list=info.enemy_recruits, seed=battle_state.seed,
                                                            snapshot=original_shop_state)
                x.battle_receive_unblockable_damage(
                    damage=self.experience,
                    battle_state=battle_state,
                    enemy=self,
                    animation_event_sequence=animation_event_sequence,
                    state_set=state_set,
                    origin="lightning",
                    original_shop_state=original_shop_state,
                    group=e
                )
            e.set_state_id(state_set.add_state(battle_state))
            animation_event_sequence.append(e)

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

        logical_level = self.get_logical_level()
        if logical_level < 3:
            target_count = 1
        elif 3 <= logical_level < 5:
            target_count = 2
        else:
            target_count = 3

        self.generic_ability_notification(
            state_set=state_set,
            animation_event_sequence=animation_event_sequence,
            state=battle_state
        )
        info = battle_state.get_battle_info(battle_id=self.battle_id)
        e = Group()

        for i in range(target_count):
            x: RecruitSerializer = random_engine.choice(_list=info.enemy_recruits, seed=battle_state.seed,
                                                        snapshot=original_shop_state)
            x.battle_receive_unblockable_damage(
                damage=self.experience,
                battle_state=battle_state,
                enemy=self,
                animation_event_sequence=animation_event_sequence,
                state_set=state_set,
                origin="lightning",
                original_shop_state=original_shop_state,
                group=e
            )
        e.set_state_id(state_set.add_state(battle_state))
        animation_event_sequence.append(e)

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

