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


class EmperorPenguin(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=236,
                         sub_type_as_text="EmperorPenguin", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def shop_end_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                         animation_event_sequence: AnimationEventSequence,
                         shop_snapshot: "ShopSnapshotSerializer" = None):
        number_of_unique_arctic_recruits = []
        number_of_emperor_penguins = 0
        visited_arctic_species = set()
        for x in shop_state.friendly_recruits:
            if x.sub_type_as_text == "EmperorPenguin":
                number_of_emperor_penguins += 1
            if GameConstants.Habitats.Arctic in x.binomial_nomenclature and x.sub_type_as_text not in visited_arctic_species:
                number_of_unique_arctic_recruits.append(x)
                visited_arctic_species.add(x.sub_type_as_text)
        buff = (3 * len(visited_arctic_species)) - (number_of_emperor_penguins * 5)
        if buff < 0:
            return
        self.generic_ability_notification(
            state=shop_state,
            state_set=state_set,
            animation_event_sequence=animation_event_sequence)
        g = Group()
        for x in shop_state.friendly_recruits:
            if GameConstants.Habitats.Arctic in x.binomial_nomenclature:
                x.shop_buff_stats(
                    shop_state=shop_state,
                    state_set=state_set,
                    stack_item=stack_item,
                    animation_event_sequence=animation_event_sequence,
                    ranged=buff,
                    health=buff,
                    max_health=buff,
                    melee=buff,
                    group=g
                )
        if len(g.animation_events) > 0:
            g.set_state_id(state_id=state_set.add_state(state=shop_state))
            animation_event_sequence.append(g)

    def start_of_battle(self,
                        battle_state: "BattleStateSerializer",
                        state_set: "StateSet",
                        stack_item: "StackItem",
                        animation_event_sequence: AnimationEventSequence,
                        original_shop_state: "ShopStateSerializer" = None):
        if self.experience < GameConstants.Levels.level_3:
            return
        info = battle_state.get_battle_info(battle_id=self.battle_id)
        arctic_aves = [x for x in info.friendly_recruits if GameConstants.Habitats.Arctic in x.binomial_nomenclature and GameConstants.ScientificNames.Aves in x.binomial_nomenclature]
        arctic_only_recruits = [x for x in info.friendly_recruits if GameConstants.Habitats.Arctic in x.binomial_nomenclature and GameConstants.ScientificNames.Aves not in x.binomial_nomenclature]
        health_buff = 0
        for x in arctic_aves:
            health_buff += int(x.max_health * 0.5)
        for x in arctic_only_recruits:
            health_buff += int(x.max_health * 0.1)
        self.battle_buff_stats(health=health_buff,
                               max_health=health_buff,
                               battle_state=battle_state,
                               state_set=state_set,
                               stack_item=stack_item, buffer=self,
                               animation_event_sequence=animation_event_sequence)

