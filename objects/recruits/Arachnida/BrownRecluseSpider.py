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


class BrownRecluseSpider(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=14,
                         sub_type_as_text="BrownRecluseSpider", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def battle_attack_with_melee(self, battle_state: "BattleStateSerializer",
                                 state_set: StateSet,
                                 stack_item: "StackItem",
                                 animation_event_sequence: AnimationEventSequence,
                                 original_shop_state: "ShopStateSerializer" = None,
                                 damage_type: str = "default"):
        if self.team_index == 0:
            front_enemy = super().battle_attack_with_melee(battle_state, state_set, stack_item,
                                                           animation_event_sequence,
                                                           original_shop_state, damage_type)
            if front_enemy is None:
                return None
            if self.experience < GameConstants.Levels.level_2:
                status = Statuses.Cytotoxin(counter=2)
            elif self.experience < GameConstants.Levels.level_4:
                status = Statuses.Cytotoxin(counter=3)
            elif self.experience < GameConstants.Levels.level_6:
                status = Statuses.Cytotoxin(counter=6)
            else:
                status = Statuses.Cytotoxin(counter=9)
            front_enemy.add_status(status=status, battle_state=battle_state, state_set=state_set,
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
            random_enemy = super().battle_attack_with_range(battle_state, state_set, stack_item,
                                                            animation_event_sequence,
                                                            original_shop_state, damage_type, group)
            if random_enemy is None:
                return None
            if self.experience < GameConstants.Levels.level_2:
                status = Statuses.Cytotoxin(counter=4)
            elif self.experience < GameConstants.Levels.level_4:
                status = Statuses.Cytotoxin(counter=5)
            elif self.experience < GameConstants.Levels.level_6:
                status = Statuses.Cytotoxin(counter=9)
            else:
                status = Statuses.Cytotoxin(counter=11)
            if random_enemy is not None:
                random_enemy.add_status(status=status, battle_state=battle_state, state_set=state_set,
                                        animation_event_sequence=animation_event_sequence,
                                        enemy=self)
            return random_enemy

