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


class CarpenterAnt(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=21,
                         sub_type_as_text="CarpenterAnt", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------
        self.valid_subtypes_as_text = [
            "BombusPolaris",
            "BullAnt",
            "CarpenterAnt",
            "EasternBumblebee",
            "FireAnt",
            "GhostAnt",
            "HoneyPotAnt",
            "PaperWasp",
            "QueenAnt",
            "VelvetAnt",
            "YellowJacket",
        ]
        if "trigger" not in self.custom_data:
            self.custom_data["trigger"] = 1

        
    def shop_end_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                         animation_event_sequence: AnimationEventSequence,
                         shop_snapshot: "ShopSnapshotSerializer" = None):
        self.generic_ability_notification(
            state=shop_state,
            state_set=state_set,
            animation_event_sequence=animation_event_sequence)
        g = Group()
        for sub_type_as_text, stats in self.custom_data.items():
            if sub_type_as_text == "trigger":
                continue
            for x in shop_state.friendly_recruits:
                if x.sub_type_as_text == sub_type_as_text:
                    health_buff = stats["health"]
                    melee_attack_buff = stats["melee_attack"]
                    ranged_attack_buff = stats["ranged_attack"]
                    armor_buff = stats["armor"]
                    initiative_buff = stats["initiative"]
                    x.shop_buff_stats(
                        shop_state=shop_state,
                        state_set=state_set,
                        stack_item=stack_item,
                        animation_event_sequence=animation_event_sequence,
                        health=health_buff,
                        max_health=health_buff,
                        melee=melee_attack_buff,
                        ranged=ranged_attack_buff,
                        armor=armor_buff,
                        initiative=initiative_buff,
                        group=g
                    )
        if len(g.animation_events) > 0:
            g.set_state_id(state_id=state_set.add_state(shop_state))
            animation_event_sequence.append(g)

    @classmethod
    def bytes_to_custom_data(cls, _bytes: bytes, current_index: int) -> dict:
        return CarpenterAntCD.bytes_to_custom_data(_bytes, current_index)

    def custom_data_to_bytes(self) -> bytes:
        return CarpenterAntCD.custom_data_to_bytes(self)

    def shop_set_object_data(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                             user_input: "ShopUserInput", animation_event_sequence: AnimationEventSequence,
                             original_shop_snapshot: "ShopSnapshotSerializer" = None):
        if user_input.set_shop_object_data_opcode == GameConstants.Opcodes.ObjectData.shop_set_custom:
            if self.custom_data["trigger"] == 0:
                raise Exception("This recruit cannot be interacted with right now")
            sub_type_as_text = user_input.player_decision_choice['sub_type_as_text']
            target_stat = user_input.player_decision_choice['stat']
            if self.experience < GameConstants.Levels.level_2:
                buff = 2
            else:
                buff = 3

            if sub_type_as_text is None:
                raise Exception("Must supply a sub_type_as_text")
            if target_stat is None:
                raise Exception("Must supply a target_stat")

            if sub_type_as_text not in self.valid_subtypes_as_text:
                raise ValueError("Invalid sub_type_as_text must be a valid 'Hymenoptera' sub-species")

            target_stat = target_stat.replace(" ", "_")

            if target_stat not in ["melee_attack", "ranged_attack", "armor", "health", "initiative"]:
                raise ValueError(
                    "Invalid target_stat must be one of 'melee_attack', 'ranged_attack', 'armor', 'health', 'initiative'")

            if sub_type_as_text not in self.custom_data:
                self.custom_data[sub_type_as_text] = {
                    "melee_attack": 0,
                    "ranged_attack": 0,
                    "armor": 0,
                    "health": 0,
                    "initiative": 0
                }
            self.custom_data[sub_type_as_text][target_stat] += buff
            self.custom_data["trigger"] = 0
            e = Animations.ShopUpdatedRecruit(
                state_id=state_set.add_state(shop_state),
                shop_id=self.shop_id,
                battle_id=self.battle_id
            )
            animation_event_sequence.append(e)

        else:
            super().shop_set_object_data(shop_state=shop_state, state_set=state_set,
                                         stack_item=stack_item, user_input=user_input,
                                         animation_event_sequence=animation_event_sequence)

    def shop_start_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                           animation_event_sequence: AnimationEventSequence,
                           shop_snapshot: "ShopSnapshotSerializer" = None):
        pass

    def shop_level_up(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                      animation_event_sequence: AnimationEventSequence):
        self.custom_data["trigger"] = 1
        e = Animations.ShopUpdatedRecruit(
            state_id=state_set.add_state(shop_state),
            shop_id=self.shop_id,
            battle_id=self.battle_id
        )
        animation_event_sequence.append(e)

