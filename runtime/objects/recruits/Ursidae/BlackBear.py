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


class BlackBear(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=131,
                         sub_type_as_text="BlackBear", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def start_of_battle(self,
                        battle_state: "BattleStateSerializer",
                        state_set: "StateSet",
                        stack_item: "StackItem",
                        animation_event_sequence: AnimationEventSequence,
                        original_shop_state: "ShopStateSerializer" = None):
        self.generic_ability_notification(
            state=battle_state,
            state_set=state_set,
            animation_event_sequence=animation_event_sequence)
        melee_buff = 0
        health_buff = 0
        armor_buff = 0
        initiative_buff = 0
        ranged_buff = 0
        if self.experience < GameConstants.Levels.level_2:
            melee_buff = 10
            health_buff = 10
            armor_buff = 4
            initiative_buff = 10
            ranged_buff = 10
        elif self.experience < GameConstants.Levels.level_3:
            melee_buff = 20
            health_buff = 20
            armor_buff = 8
            initiative_buff = 20
            ranged_buff = 20
        elif self.experience < GameConstants.Levels.level_4:
            melee_buff = 30
            health_buff = 30
            armor_buff = 12
            initiative_buff = 30
            ranged_buff = 30
        else:
            melee_buff = 40
            health_buff = 40
            armor_buff = 16
            initiative_buff = 40
            ranged_buff = 40
        self.battle_buff_stats(
            battle_state=battle_state,
            state_set=state_set,
            stack_item=stack_item,
            animation_event_sequence=animation_event_sequence,
            ranged=ranged_buff,
            health=health_buff,
            max_health=health_buff,
            melee=melee_buff,
            initiative=initiative_buff,
            armor=armor_buff
        )
        info = battle_state.get_battle_info(battle_id=self.battle_id)
        for x in info.friendly_recruits:
            if GameConstants.ScientificNames.Canidae in x.binomial_nomenclature:
                x.listeners.add_listener(hook=Listeners.Hooks.battle_receive_damage, listener=self)

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
        percentage = 0.97
        if self.experience < GameConstants.Levels.level_4:
            percentage = 0.97
        else:
            percentage = 0.94
        original_damage = damage
        damage = max(0, int(damage * percentage))
        prevented_damage = original_damage - damage
        damage_reduction_stack.append(
            dict(amount=prevented_damage, sub_type_as_int=GameConstants.DamageReductionStack.BearHide)
        )
        return super().battle_receive_damage(damage, battle_state, enemy, state_set, animation_event_sequence,
                                             origin, original_shop_state, damage_reduction_stack)

    def lt_battle_receive_damage(self, damage: int,
                                 battle_state: "BattleStateSerializer",
                                 enemy: "BaseRecruit",
                                 state_set: "StateSet",
                                 animation_event_sequence: AnimationEventSequence,
                                 recruit: "RecruitSerializer",
                                 origin: str = "melee",
                                 original_shop_state: "ShopStateSerializer" = None,
                                 damage_reduction_stack: list[dict] = None,
                                 ) -> list[int, bool]:
        if damage_reduction_stack is None:
            damage_reduction_stack = [
                dict(amount=damage, sub_type_as_int=GameConstants.DamageReductionStack.UnModifiedDamage)]
        prevented_damage = 0
        percentage = 0.97
        if self.experience < GameConstants.Levels.level_4:
            percentage = 0.97
        else:
            percentage = 0.94
        original_damage = damage
        damage = max(0, int(damage * percentage))
        prevented_damage = original_damage - damage
        damage_reduction_stack.append(
            dict(amount=prevented_damage, sub_type_as_int=GameConstants.DamageReductionStack.BearHide)
        )
        return [damage, False]

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

        info = battle_state.get_battle_info(battle_id=self.battle_id)
        objects = info.friendly_recruits + info.friendly_relics
        objects = [x for x in objects if x.battle_id != self.battle_id]
        battle_state.queue_ability_for(trigger=GameConstants.Opcodes.Stack.battle_friendly_recruit_faints,
                                       objects=objects,
                                       context={"target": self})

        battle_state.remove_recruit_from_battle(self)
        battle_state.stack = deque([x for x in battle_state.stack if x.object.battle_id != self.battle_id])

        for x in info.friendly_recruits:
            if GameConstants.ScientificNames.Canidae in x.binomial_nomenclature:
                x.listeners.remove_listener(hook=Listeners.Hooks.battle_receive_damage, listener=self)

