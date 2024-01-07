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


class GhostAnt(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=55,
                         sub_type_as_text="GhostAnt", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------
        self.exiled = False
        self.team_uuid = None

        
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
        if self.exiled:
            if battle_state.friendly_uuid == self.team_uuid:
                recruits = battle_state.friendly_recruits
            else:
                recruits = battle_state.enemy_recruits
            if len(recruits) < 7:
                self.exiled = False
                recruits.insert(0, self)
                battle_state.update_objects_sorted()
                for i, x in enumerate(recruits):
                    x.team_index = i
                self.health = 1
                e = Animations.Revive(
                    state_id=state_set.add_state(state=battle_state),
                    shop_id=self.shop_id,
                    battle_id=self.battle_id,
                )
                animation_event_sequence.append(e)
                battle_state.queue_ability_for(trigger=GameConstants.Opcodes.Stack.battle_friendly_recruit_summoned,
                                               objects=recruits,
                                               context={"target": self})
                return

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
        e = Animations.Faint(
            state_id=state_set.add_state(state=battle_state),
            shop_id=self.shop_id,
            battle_id=self.battle_id,
        )
        animation_event_sequence.append(e)

        battle_info = battle_state.get_battle_info(battle_id=self.battle_id)
        objects = battle_info.friendly_recruits + battle_info.friendly_relics
        battle_state.queue_ability_for(trigger=GameConstants.Opcodes.Stack.battle_friendly_recruit_faints,
                                       objects=objects,
                                       context={"target": self})
        self.team_uuid = battle_info.friendly_uuid

        battle_info.friendly_recruits.pop(self.team_index)
        for i, x in enumerate(battle_info.friendly_recruits):
            x.team_index = i
        battle_state.stack = deque([x for x in battle_state.stack if x.object.battle_id != self.battle_id])
        self.exiled = True

    def battle_attack_with_melee(self, battle_state: "BattleStateSerializer",
                                 state_set: StateSet,
                                 stack_item: "StackItem",
                                 animation_event_sequence: AnimationEventSequence,
                                 original_shop_state: "ShopStateSerializer" = None,
                                 damage_type: str = "default"):
        if self.exiled:
            return
        else:
            super().battle_attack_with_melee(battle_state=battle_state,
                                             state_set=state_set,
                                             stack_item=stack_item,
                                             animation_event_sequence=animation_event_sequence,
                                             original_shop_state=original_shop_state,
                                             damage_type=damage_type)

    def battle_attack_with_range(self, battle_state: "BattleStateSerializer",
                                 state_set: StateSet,
                                 stack_item: "StackItem",
                                 animation_event_sequence: AnimationEventSequence,
                                 original_shop_state: "ShopStateSerializer" = None,
                                 damage_type: str = "default",
                                 group=None) -> Union["RecruitSerializer", None]:
        if self.exiled:
            return
        else:
            super().battle_attack_with_range(battle_state=battle_state,
                                             state_set=state_set,
                                             stack_item=stack_item,
                                             animation_event_sequence=animation_event_sequence,
                                             original_shop_state=original_shop_state,
                                             damage_type=damage_type,
                                             group=group)

    def battle_level_up(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                        animation_event_sequence: AnimationEventSequence):
        if self.exiled:
            return
        else:
            super().battle_level_up(shop_state, state_set, stack_item, animation_event_sequence)

    def battle_gain_experience(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                               animation_event_sequence: AnimationEventSequence):
        if self.exiled:
            return
        else:
            super().battle_gain_experience(shop_state, state_set, stack_item, animation_event_sequence)

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

