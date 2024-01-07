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


class HoneyPotAnt(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=230,
                         sub_type_as_text="HoneyPotAnt", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------
        if "honey_counter" not in self.custom_data:
            self.custom_data["honey_counter"] = 5
        self.honey_counter = self.custom_data["honey_counter"]

        
    def shop_end_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                         animation_event_sequence: AnimationEventSequence,
                         shop_snapshot: "ShopSnapshotSerializer" = None):
        if self.experience < GameConstants.Levels.level_2:
            buff = 2
        elif self.experience < GameConstants.Levels.level_3:
            buff = 4
        elif self.experience < GameConstants.Levels.level_4:
            buff = 8
        elif self.experience < GameConstants.Levels.level_5:
            buff = 12
        else:
            buff = 16
        self.honey_counter += buff
        self.custom_data["honey_counter"] += buff
        e = Animations.ShopUpdatedRecruit(
            state_id=state_set.add_state(shop_state),
            shop_id=self.shop_id,
            battle_id=self.battle_id,
        )
        animation_event_sequence.append(e)

    def shop_start_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                           animation_event_sequence: AnimationEventSequence,
                           shop_snapshot: "ShopSnapshotSerializer" = None):
        recruits = sorted(shop_state.friendly_recruits, key=lambda x: x.initiative)
        g = Group()
        for x in recruits:
            if GameConstants.ScientificNames.Ursidae in x.binomial_nomenclature and self.honey_counter >= 7 and x.sub_type_as_text != "HoneyPotAnt":
                self.honey_counter -= 7
                self.custom_data["honey_counter"] -= 7
                x.shop_buff_stats(
                    shop_state=shop_state,
                    state_set=state_set,
                    stack_item=stack_item,
                    animation_event_sequence=animation_event_sequence,
                    ranged=7,
                    health=7,
                    max_health=7,
                    melee=7,
                    armor=3,
                    group=g
                )
            elif GameConstants.ScientificNames.Hymenoptera in x.binomial_nomenclature and self.honey_counter > 2 and x.sub_type_as_text != "HoneyPotAnt":
                self.honey_counter -= 2
                self.custom_data["honey_counter"] -= 2
                x.shop_buff_stats(
                    shop_state=shop_state,
                    state_set=state_set,
                    stack_item=stack_item,
                    animation_event_sequence=animation_event_sequence,
                    ranged=2,
                    health=2,
                    max_health=2,
                    melee=2,
                    armor=1,
                    group=g
                )

        if len(g.animation_events) > 0:
            g.set_state_id(state_id=state_set.add_state(state=shop_state))
            animation_event_sequence.append(g)

    @classmethod
    def bytes_to_custom_data(cls, _bytes: bytes, current_index: int) -> dict:
        return Uint16Counter.bytes_to_custom_data(_bytes=_bytes, current_index=current_index, key="honey_counter")

    def custom_data_to_bytes(self) -> bytes:
        return Uint16Counter.custom_data_to_bytes(self, key="honey_counter")

