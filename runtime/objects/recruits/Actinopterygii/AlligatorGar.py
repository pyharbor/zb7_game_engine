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


class AlligatorGar(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=83,
                         sub_type_as_text="AlligatorGar", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
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
        info = battle_state.get_battle_info(battle_id=self.battle_id)
        group = Group()
        for x in info.friendly_recruits:
            for habitat in GameConstants.Habitats.Freshwater:
                if habitat in x.binomial_nomenclature:
                    if self.experience < GameConstants.Levels.level_3:
                        x.battle_buff_stats(
                            battle_state=battle_state,
                            state_set=state_set,
                            stack_item=stack_item,
                            animation_event_sequence=animation_event_sequence,
                            original_shop_state=original_shop_state,
                            ranged=20,
                            group=group
                        )
                    elif GameConstants.Levels.level_3 <= self.experience < GameConstants.Levels.level_5:
                        x.battle_buff_stats(
                            battle_state=battle_state,
                            state_set=state_set,
                            stack_item=stack_item,
                            animation_event_sequence=animation_event_sequence,
                            original_shop_state=original_shop_state,
                            ranged=20,
                            health=20,
                            max_health=20,
                            group=group
                        )
                    elif GameConstants.Levels.level_5 <= self.experience:
                        x.battle_buff_stats(
                            battle_state=battle_state,
                            state_set=state_set,
                            stack_item=stack_item,
                            animation_event_sequence=animation_event_sequence,
                            original_shop_state=original_shop_state,
                            ranged=25,
                            health=25,
                            max_health=25,
                            armor=10,
                            group=group
                        )
                    break
        group.set_state_id(state_set.add_state(battle_state))
        animation_event_sequence.append(group)

