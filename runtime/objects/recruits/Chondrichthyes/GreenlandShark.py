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


class GreenlandShark(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=228,
                         sub_type_as_text="GreenlandShark", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
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
        recruit: RecruitSerializer = stack_item.context["target"]
        for h in GameConstants.Habitats.Oceanic:
            if h in recruit.binomial_nomenclature:
                health_boost = 0
                melee_boost = 0
                ranged_boost = 0
                armor_boost = 0
                if self.experience < GameConstants.Levels.level_2:
                    health_boost += 1
                elif self.experience < GameConstants.Levels.level_3:
                    health_boost += 1
                    melee_boost += 1
                    ranged_boost += 1
                elif self.experience < GameConstants.Levels.level_4:
                    health_boost += 2
                    melee_boost += 1
                    ranged_boost += 1
                else:
                    health_boost += 2
                    melee_boost += 2
                    ranged_boost += 2
                    armor_boost += 1

                self.battle_buff_stats(battle_state=battle_state,
                                       state_set=state_set,
                                       stack_item=stack_item,
                                       animation_event_sequence=animation_event_sequence,
                                       original_shop_state=original_shop_state,
                                       health=health_boost,
                                       max_health=health_boost,
                                       melee=melee_boost,
                                       ranged=ranged_boost,
                                       armor=armor_boost)
                if original_shop_state is not None:
                    obj = original_shop_state.get_object_from_shop_id(self.shop_id)
                    if obj is not None:
                        obj.melee_attack += melee_boost
                        obj.ranged_attack += ranged_boost
                        obj.armor += armor_boost
                        obj.health += health_boost
                        obj.max_health += health_boost

