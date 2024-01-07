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


class SaltwaterCrocodile(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=73,
                         sub_type_as_text="SaltwaterCrocodile", 
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
        swampy_count = 0
        freshwater_count = 0
        info = battle_state.get_battle_info(battle_id=self.battle_id)
        for x in info.friendly_recruits:
            for h in GameConstants.Habitats.Swampy:
                if h in x.binomial_nomenclature:
                    swampy_count += 1
                    break
            for h in GameConstants.Habitats.Freshwater:
                if h in x.binomial_nomenclature:
                    freshwater_count += 1
                    break
        total = swampy_count + freshwater_count
        buff = 5 * total
        self.battle_buff_stats(melee=buff,
                               ranged=buff,
                               health=buff,
                               max_health=buff,
                               armor=total,
                               battle_state=battle_state,
                               state_set=state_set,
                               stack_item=stack_item, buffer=self,
                               animation_event_sequence=animation_event_sequence)

    def shop_end_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                         animation_event_sequence: AnimationEventSequence,
                         shop_snapshot: "ShopSnapshotSerializer" = None):
        self.generic_ability_notification(
            state=shop_state,
            state_set=state_set,
            animation_event_sequence=animation_event_sequence)
        g = Group()
        if self.experience >= GameConstants.Levels.level_3:
            for x in shop_state.friendly_recruits:
                buff = 0
                for h in GameConstants.Habitats.Swampy:
                    if h in x.binomial_nomenclature:
                        buff += 1
                        break
                for h in GameConstants.Habitats.Freshwater:
                    if h in x.binomial_nomenclature:
                        buff += 1
                        break
                if buff > 0:
                    x.shop_buff_stats(melee=buff,
                                      ranged=buff,
                                      health=buff,
                                      max_health=buff,
                                      shop_state=shop_state,
                                      state_set=state_set,
                                      stack_item=stack_item, buffer=self,
                                      animation_event_sequence=animation_event_sequence,
                                      group=g)
        g.set_state_id(state_id=state_set.add_state(state=shop_state))
        animation_event_sequence.append(g)
