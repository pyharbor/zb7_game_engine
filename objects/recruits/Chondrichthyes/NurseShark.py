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


class NurseShark(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=62,
                         sub_type_as_text="NurseShark", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------
        self.graveyard = []

        
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
        heal_amount = 0
        if self.experience < GameConstants.Levels.level_2:
            heal_amount = 10
        elif self.experience < GameConstants.Levels.level_3:
            heal_amount = 15
        elif self.experience < GameConstants.Levels.level_4:
            heal_amount = 20
        elif self.experience < GameConstants.Levels.level_5:
            heal_amount = 25
        elif self.experience < GameConstants.Levels.level_6:
            heal_amount = 30
        elif self.experience < GameConstants.Levels.level_7:
            heal_amount = 35
        elif self.experience < GameConstants.Levels.level_8:
            heal_amount = 40
        elif self.experience < GameConstants.Levels.level_9:
            heal_amount = 45
        else:
            heal_amount = 50

        info = battle_state.get_battle_info(battle_id=self.battle_id)
        sharks = [recruit for recruit in info.friendly_recruits if
                  GameConstants.ScientificNames.Chondrichthyes in recruit.binomial_nomenclature]
        damaged_sharks = [recruit for recruit in sharks if recruit.health < recruit.max_health]
        if len(damaged_sharks) > 0:
            highest_attack_damaged_shark = max(damaged_sharks,
                                               key=lambda recruit: recruit.melee_attack + recruit.ranged_attack)
            self.generic_ability_notification(
                state=battle_state,
                state_set=state_set,
                animation_event_sequence=animation_event_sequence)
            highest_attack_damaged_shark.battle_heal(
                healer=self,
                heal=heal_amount,
                battle_state=battle_state,
                state_set=state_set,
                animation_event_sequence=animation_event_sequence
            )
        else:
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
        valid_targets = []
        for x in self.graveyard:
            for h in GameConstants.Habitats.Oceanic:
                if h in x.binomial_nomenclature and "NurseShark" != x.sub_type_as_text:
                    valid_targets.append(x)


        battle_info = battle_state.get_battle_info(battle_id=self.battle_id)
        objects = battle_info.friendly_recruits + battle_info.friendly_relics
        objects = [x for x in objects if x.battle_id != self.battle_id]
        battle_state.queue_ability_for(trigger=GameConstants.Opcodes.Stack.battle_friendly_recruit_faints,
                                       objects=objects,
                                       context={"target": self})

        battle_state.remove_recruit_from_battle(self)
        battle_state.stack = deque([x for x in battle_state.stack if x.object.battle_id != self.battle_id])
        if len(valid_targets) > 0:
            random_choice = random_engine.choice(_list=valid_targets, seed=battle_state.seed,
                                                 snapshot=original_shop_state)
            # we have to pull it again because it has diverged
            current_info = battle_state.get_battle_info(battle_id=self.battle_id)
            current_info.friendly_recruits.append(random_choice)
            battle_state.update_objects_sorted()
            for i, x in enumerate(current_info.friendly_recruits):
                x.team_index = i
            e = Animations.Revive(state_id=state_set.add_state(state=battle_state),
                                  shop_id=random_choice.shop_id,
                                  battle_id=random_choice.battle_id)
            animation_event_sequence.append(e)

    def battle_friendly_recruit_faints(self, battle_state: "BattleStateSerializer",
                                       state_set: StateSet,
                                       stack_item: StackItem,
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

        target = stack_item.context["target"]
        shop_ids = [x.shop_id for x in self.graveyard]
        if target.shop_id not in shop_ids:
            self.graveyard.append(target)
        super().battle_friendly_recruit_faints(battle_state, state_set, stack_item, animation_event_sequence,
                                               original_shop_state)

