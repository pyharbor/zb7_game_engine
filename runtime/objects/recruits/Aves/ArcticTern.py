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


class ArcticTern(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=107,
                         sub_type_as_text="ArcticTern", 
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
        random_num = battle_state.random.random()
        evasive_probability = 0.0
        if self.experience < GameConstants.Levels.level_2:
            evasive_probability = 0.07
        elif self.experience < GameConstants.Levels.level_3:
            evasive_probability = 0.14
        elif self.experience < GameConstants.Levels.level_4:
            evasive_probability = 0.21
        elif self.experience < GameConstants.Levels.level_5:
            evasive_probability = 0.28
        elif self.experience < GameConstants.Levels.level_6:
            evasive_probability = 0.35
        elif self.experience < GameConstants.Levels.level_7:
            evasive_probability = 0.42
        elif self.experience < GameConstants.Levels.level_8:
            evasive_probability = 0.49
        elif self.experience < GameConstants.Levels.level_9:
            evasive_probability = 0.56
        elif self.experience < GameConstants.Levels.level_10:
            evasive_probability = 0.63
        else:
            evasive_probability = 0.70

        if evasive_probability > random_num:
            damage_reduction_stack.append(
                dict(amount=damage, sub_type_as_int=GameConstants.DamageReductionStack.Evasion))
            e = Animations.Dodge(state_id=state_set.add_state(state=battle_state),
                                 shop_id=self.shop_id,
                                 battle_id=self.battle_id,
                                 amount=damage)
            animation_event_sequence.append(e)
        else:
            return super().battle_receive_damage(damage, battle_state, enemy, state_set, animation_event_sequence,
                                             origin, original_shop_state, damage_reduction_stack)

