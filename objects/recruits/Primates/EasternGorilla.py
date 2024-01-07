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


class EasternGorilla(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=88,
                         sub_type_as_text="EasternGorilla", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def shop_buff_stats(self, shop_state: "ShopStateSerializer",
                        stack_item: "StackItem",
                        state_set: "StateSet",
                        animation_event_sequence: AnimationEventSequence,
                        original_shop_state: "ShopStateSerializer" = None,
                        melee: int = 0,
                        ranged: int = 0,
                        health: int = 0,
                        max_health: int = 0,
                        armor: int = 0,
                        initiative: int = 0,
                        buffer: Union["RecruitSerializer", "RelicSerializer"] = None,
                        group: Group = None):

        number_of_primates = len([x for x in shop_state.friendly_recruits if
                                  GameConstants.ScientificNames.Primates in x.binomial_nomenclature])
        if self.experience < GameConstants.Levels.level_2:
            buff = 1.05 ** number_of_primates
        elif self.experience < GameConstants.Levels.level_3:
            buff = 1.1 ** number_of_primates
        else:
            buff = 1.15 ** number_of_primates
        melee = int(melee * buff)
        ranged = int(ranged * buff)
        health = int(health * buff)
        max_health = int(max_health * buff)
        armor = int(armor * buff)
        initiative = int(initiative * buff)

        super().shop_buff_stats(shop_state=shop_state, stack_item=stack_item, state_set=state_set,
                                animation_event_sequence=animation_event_sequence,
                                original_shop_state=original_shop_state,
                                melee=melee, ranged=ranged, health=health,
                                armor=armor,
                                max_health=max_health,
                                initiative=initiative,
                                buffer=buffer,
                                group=group)

    def battle_buff_stats(self, battle_state: "BattleStateSerializer",
                          stack_item: "StackItem",
                          state_set: "StateSet",
                          animation_event_sequence: AnimationEventSequence,
                          original_shop_state: "ShopStateSerializer" = None,
                          melee: int = 0,
                          ranged: int = 0,
                          health: int = 0,
                          max_health: int = 0,
                          armor: int = 0,
                          initiative: int = 0,
                          buffer: Union["RecruitSerializer", "RelicSerializer"] = None,
                          group: Group = None):
        info = battle_state.get_battle_info(battle_id=self.battle_id)
        number_of_primates = len([x for x in info.friendly_recruits if
                                  GameConstants.ScientificNames.Primates in x.binomial_nomenclature])
        if self.experience < GameConstants.Levels.level_2:
            buff = 1.05 ** number_of_primates
        elif self.experience < GameConstants.Levels.level_3:
            buff = 1.1 ** number_of_primates
        else:
            buff = 1.15 ** number_of_primates
        melee = int(melee * buff)
        ranged = int(ranged * buff)
        health = int(health * buff)
        max_health = int(max_health * buff)
        armor = int(armor * buff)
        initiative = int(initiative * buff)
        super().battle_buff_stats(battle_state=battle_state, stack_item=stack_item, state_set=state_set,
                                  animation_event_sequence=animation_event_sequence,
                                  original_shop_state=original_shop_state,
                                  melee=melee, ranged=ranged, health=health,
                                  armor=armor,
                                  max_health=max_health,
                                  initiative=initiative,
                                  buffer=buffer,
                                  group=group)

