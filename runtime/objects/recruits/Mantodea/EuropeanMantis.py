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


class EuropeanMantis(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=114,
                         sub_type_as_text="EuropeanMantis", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def shop_end_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                         animation_event_sequence: AnimationEventSequence,
                         shop_snapshot: "ShopSnapshotSerializer" = None):
        try:
            target = shop_state.friendly_recruits[self.team_index - 1]
        except IndexError:
            return
        if isinstance(target, EmptySlotSerializer):
            return
        self.generic_ability_notification(
            state=shop_state,
            state_set=state_set,
            animation_event_sequence=animation_event_sequence)
        e = Animations.MeleeAttack(state_id=state_set.add_state(shop_state),
                                   battle_id=self.battle_id,
                                   amount=self.melee_attack,
                                   shop_id=self.shop_id,
                                   target_shop_id=target.shop_id,
                                   target_battle_id=target.battle_id)
        animation_event_sequence.append(e)
        target_original_health = target.health
        damage = self.melee_attack
        target.health = max(target.health - damage, 0)
        damage_reduction_stack = [
            dict(amount=damage, sub_type_as_int=GameConstants.DamageReductionStack.UnModifiedDamage)]
        initial_damage = damage_reduction_stack[0]["amount"]
        state_id = state_set.add_state(state=shop_state)
        if damage > 0:
            e = Animations.ReceiveDamage(
                state_id=state_id,
                damage_reduction_stack=damage_reduction_stack,
                damage_after_modifications=damage,
                damage_before_modifications=initial_damage,
                battle_id=target.battle_id,
                shop_id=target.shop_id,
            )
            animation_event_sequence.append(e)
        elif damage <= 0:
            e = Animations.FullBlock(
                state_id=state_id,
                damage_reduction_stack=damage_reduction_stack,
                damage_after_modifications=damage,
                damage_before_modifications=initial_damage,
                battle_id=self.battle_id,
                shop_id=self.shop_id,
            )
            animation_event_sequence.append(e)
        if target.health <= 0:
            target.shop_faint(shop_state=shop_state,
                              state_set=state_set,
                              stack_item=stack_item,
                              animation_event_sequence=animation_event_sequence,
                              original_shop_state=shop_snapshot)
        else:
            target.max_health = max(target.max_health - damage, 0)

        buff = 0.75
        if self.experience >= GameConstants.Levels.level_2:
            buff = 1.0
        buff = int(buff * (target_original_health - target.health))
        self.shop_buff_stats(
            shop_state=shop_state,
            state_set=state_set,
            stack_item=stack_item,
            animation_event_sequence=animation_event_sequence,
            ranged=buff,
            health=buff,
            max_health=buff,
            melee=buff
        )

