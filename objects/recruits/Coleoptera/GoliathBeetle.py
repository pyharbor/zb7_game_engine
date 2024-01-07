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


class GoliathBeetle(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=124,
                         sub_type_as_text="GoliathBeetle", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------
        if "previous_max_carapace_counter" not in self.custom_data:
            self.custom_data["previous_max_carapace_counter"] = 0

        
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
        info = battle_state.get_battle_info(self.battle_id)
        for x in info.friendly_recruits:
            x.listeners.add_listener(hook=Listeners.Hooks.add_status, listener=self)
        counter = 0
        status = self.get_status(sub_type_as_text="Carapace")
        if status is not None:
            counter += status.counter
        counter += 1
        counter = max(1, int(counter * 1.5))
        self.add_status(Statuses.Carapace(counter=counter), battle_state=battle_state, state_set=state_set,
                        animation_event_sequence=animation_event_sequence,
                        enemy=None,
                        original_shop_state=original_shop_state)

    def shop_start_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                           animation_event_sequence: AnimationEventSequence,
                           shop_snapshot: "ShopSnapshotSerializer" = None):
        self.generic_ability_notification(
            state=shop_state,
            state_set=state_set,
            animation_event_sequence=animation_event_sequence)
        buff = self.custom_data["previous_max_carapace_counter"]
        targets = [x for x in shop_state.friendly_recruits if x.sub_type_as_text != "EmptySlot"]
        # probabbilities decreasing from left to right for n slots
        # 0.5, 0.25, 0.125, 0.0625, 0.03125
        random_num = random_engine.random_float(seed=shop_snapshot.uuid, snapshot=shop_snapshot)
        probablities = [0.5, 0.25, 0.125, 0.0625, 0.03125, 0.1]
        current_prob = 0
        buffed_unit = False
        for x in targets:
            current_prob += probablities.pop(0)
            if random_num < current_prob:
                x.shop_buff_stats(
                    shop_state=shop_state,
                    state_set=state_set,
                    stack_item=stack_item,
                    animation_event_sequence=animation_event_sequence,
                    ranged=int(buff / 3),
                    health=int(buff/1.1),
                    max_health=int(buff/1.1),
                    melee=int(buff / 3),
                    armor=int(buff / 6)
                )
                buffed_unit = True
                break
        if not buffed_unit:
            targets[-1].shop_buff_stats(
                shop_state=shop_state,
                state_set=state_set,
                stack_item=stack_item,
                animation_event_sequence=animation_event_sequence,
                ranged=int(buff / 3),
                health=buff,
                max_health=buff,
                melee=int(buff / 3),
                armor=int(buff / 5)
            )

    def lt_add_status(self, status: BaseStatus,
                      battle_state: "BattleStateSerializer",
                      state_set: "StateSet",
                      enemy: "RecruitSerializer",
                      animation_event_sequence: AnimationEventSequence,
                      origin: str = "melee",
                      original_shop_state: "ShopStateSerializer" = None
                      ):
        should_return = False
        carapace_count = 0
        if status.sub_type_as_text == "Carapace":
            carapace_count = status.counter
        info = battle_state.get_battle_info(battle_id=self.battle_id)
        for x in info.friendly_recruits:
            s = x.get_status(sub_type_as_text="Carapace")
            if s is not None:
                carapace_count += s.counter
        if original_shop_state is not None:
            obj = original_shop_state.get_object_from_shop_id(self.shop_id)
            if obj is not None:
                obj.custom_data["previous_max_carapace_counter"] = max(carapace_count, obj.custom_data["previous_max_carapace_counter"])
        self.custom_data["previous_max_carapace_counter"] = max(carapace_count, self.custom_data["previous_max_carapace_counter"])
        return status, should_return

    @classmethod
    def bytes_to_custom_data(cls, _bytes: bytes, current_index: int) -> dict:
        return Uint8Counter.bytes_to_custom_data(_bytes=_bytes, current_index=current_index, key="previous_max_carapace_counter")

    def custom_data_to_bytes(self) -> bytes:
        return Uint8Counter.custom_data_to_bytes(self, key="previous_max_carapace_counter")

