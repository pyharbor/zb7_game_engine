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


class VitaminWater(RelicSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=211,
                         sub_type_as_text="VitaminWater", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------
        if "target" not in self.custom_data:
            self.custom_data["target"] = None
            self.target = None
        else:
            self.target = self.custom_data["target"]

        
    def shop_end_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                         animation_event_sequence: AnimationEventSequence):
        self.generic_ability_notification(state=shop_state, state_set=state_set,
                                          animation_event_sequence=animation_event_sequence)
        if self.target is not None:
            target_match = shop_state.get_object_from_shop_id(shop_id=self.target)
            if target_match is not None:
                buff = self.get_logical_level()
                target_match.shop_buff_stats(health=buff,
                                             max_health=buff,
                                             shop_state=shop_state,
                                             state_set=state_set,
                                             stack_item=stack_item, buffer=self,
                                             animation_event_sequence=animation_event_sequence)

    @classmethod
    def bytes_to_custom_data(cls, _bytes: bytes, current_index: int) -> dict:
        return ShopIDTarget.bytes_to_custom_data(_bytes=_bytes, current_index=current_index)

    def custom_data_to_bytes(self) -> bytes:
        return ShopIDTarget.custom_data_to_bytes(self)

    def shop_set_object_data(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                             user_input: "ShopUserInput", animation_event_sequence: AnimationEventSequence,
                             original_shop_snapshot: "ShopSnapshotSerializer" = None):
        if user_input.set_shop_object_data_opcode == GameConstants.Opcodes.ObjectData.shop_set_custom:
            if self.target is not None:
                raise Exception("Target already set")
            if user_input.target_object is None:
                raise Exception("No target object provided")

            team_match = shop_state.get_object_from_shop_id(shop_id=int(user_input.target_object))
            if team_match is None:
                raise ValueError("Target entity does not exist")

            else:
                self.custom_data["target"] = team_match.shop_id
                self.target = team_match.shop_id
                e = Animations.ShopUpdatedRecruit(shop_id=self.shop_id,
                                                  state_id=state_set.add_state(shop_state),
                                                  battle_id=self.battle_id)
                animation_event_sequence.append(e)
        elif user_input.set_shop_object_data_opcode == GameConstants.Opcodes.ObjectData.shop_upgrade_object:
            logical_level = self.get_logical_level()
            if logical_level >= 3:
                raise Exception(f"{self.__class__.__name__} cannot be upgraded past level 3")

            if shop_state.money < 5:
                raise Exception(f"Not enough money to upgrade {self.__class__.__name__}")

            shop_state.money -= 5
            if self.experience == GameConstants.Levels.level_1:
                self.experience = GameConstants.Levels.level_2
            elif self.experience == GameConstants.Levels.level_2:
                self.experience = GameConstants.Levels.level_3
        else:
            super().shop_set_object_data(shop_state=shop_state, state_set=state_set,
                                         stack_item=stack_item, user_input=user_input,
                                         animation_event_sequence=animation_event_sequence)

    def shop_friendly_recruit_sold(self, shop_state: "ShopStateSerializer",
                                   state_set: "StateSet",
                                   stack_item: "StackItem",
                                   animation_event_sequence: AnimationEventSequence,
                                   original_run_snapshot: "ShopSnapshotSerializer" = None):
        target = stack_item.context["target"]
        if target.shop_id == self.custom_data["target"]:
            self.custom_data["target"] = None
            self.target = None

