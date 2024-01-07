from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from collections import defaultdict
from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature
from zb7_game_engine.runtime.objects.base.BaseRecruit import BaseRecruit
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus
from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.StateSet import StateSet
from typing import List, TYPE_CHECKING, Union
from zb7_game_engine.runtime.core.StackItem import StackItem
from zb7_game_engine.serialization.animation_events.Animations import Animations
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer
from zb7_game_engine.runtime.core.Listeners import Listeners
from zb7_game_engine.serialization.animation_events.Animations import Animations
from zb7_game_engine.runtime.core.RandomEngine import random_engine
from zb7_game_engine.serialization.animation_events.G.Group import Group
from zb7_game_engine.runtime.objects.statuses.Statuses import Statuses
from zb7_game_engine.serialization.shared.custom_data.ShopIDTarget import ShopIDTarget
from zb7_game_engine.runtime.core.ObjectParser import ObjectParser
from zb7_game_engine.serialization.shared.custom_data.SuperNestCD import SuperNestCD
from zb7_game_engine.serialization.shared.custom_data.Rewards import Rewards


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


class SuperNest(RelicSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=217,
                         sub_type_as_text="SuperNest", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------
        if "construction_counter" not in self.custom_data:
            self.custom_data["construction_counter"] = 5
        if "start_of_battle" not in self.custom_data:
            self.custom_data["start_of_battle"] = {}
        if "battle_friendly_recruit_summoned" not in self.custom_data:
            self.custom_data["battle_friendly_recruit_summoned"] = {}

        
    def start_of_battle(self,
                        battle_state: "BattleStateSerializer",
                        state_set: StateSet,
                        stack_item: "StackItem",
                        animation_event_sequence: AnimationEventSequence,
                        original_run_snapshot: "BattleSnapshotSerializer" = None):
        for k,v in self.custom_data["start_of_battle"].items():
            print(f"{k} {v}")

    def battle_friendly_recruit_summoned(self, battle_state: "BattleStateSerializer",
                                         state_set: StateSet,
                                         stack_item: StackItem,
                                         animation_event_sequence: AnimationEventSequence,
                                         original_run_snapshot: "BattleSnapshotSerializer" = None):
        for k,v in self.custom_data["battle_friendly_recruit_summoned"].items():
            print(f"{k} {v}")

    @classmethod
    def bytes_to_custom_data(cls, _bytes: bytes, current_index: int) -> dict:
        return SuperNestCD.bytes_to_custom_data(_bytes, current_index)

    def custom_data_to_bytes(self) -> bytes:
        return SuperNestCD.custom_data_to_bytes(self)

    def shop_set_object_data(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                             user_input: "ShopUserInput", animation_event_sequence: AnimationEventSequence):
        if user_input.set_shop_object_data_opcode == GameConstants.Opcodes.ObjectData.shop_set_custom:
            raise Exception("Not Implemented yet")
            info = user_input.player_decision_choice
            sub_type_as_text = info["sub_type_as_text"]
            immutable_data = ImmutableData.Subtype.from_text(sub_type_as_text)
            if immutable_data["main_species"] != GameConstants.ScientificNames.Hymenoptera:
                raise Exception("Invalid species")
            trigger = info["trigger"]
            melee = info["melee_buff"]
            ranged = info["ranged_buff"]
            armor = info["armor_buff"]
            health = info["health_buff"]
            initiative = info["initiative_buff"]

            cost = 5
            if self.custom_data["construction_counter"] < cost:
                raise Exception("Not enough construction counter")

            if sub_type_as_text not in self.custom_data[trigger]:
                self.custom_data[trigger][sub_type_as_text] = defaultdict(int)
            self.custom_data[trigger][sub_type_as_text]["melee_buff"] += melee
            self.custom_data[trigger][sub_type_as_text]["ranged_buff"] += ranged
            self.custom_data[trigger][sub_type_as_text]["armor_buff"] += armor
            self.custom_data[trigger][sub_type_as_text]["health_buff"] += health
            self.custom_data[trigger][sub_type_as_text]["initiative_buff"] += initiative


        else:
            super().shop_set_object_data(shop_state=shop_state, state_set=state_set,
                                         stack_item=stack_item, user_input=user_input,
                                         animation_event_sequence=animation_event_sequence)

