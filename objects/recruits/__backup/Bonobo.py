from typing import List
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


class Bonobo(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=86,
                         sub_type_as_text="Bonobo",
                         **kwargs)

        # ------ Protect Below from Code Templating ------
        self.target = self.custom_data.get("target", None)

    @classmethod
    def bytes_to_custom_data(cls, _bytes: bytes, current_index: int) -> dict:
        len_target = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        if len_target > 0:
            target = int.from_bytes(_bytes[current_index:current_index + len_target], byteorder="big")
        else:
            target = None
        return {"target": target}

    def custom_data_to_bytes(self) -> bytes:
        _bytes = bytearray()
        len_target_bytes = int(0).to_bytes(1, byteorder="big")
        target_bytes = b""
        if self.target is not None:
            target_bytes = self.target.to_bytes(1, byteorder="big")
            len_target_bytes = len(target_bytes).to_bytes(1, byteorder="big")
        _bytes.extend(len_target_bytes)
        _bytes.extend(target_bytes)
        return _bytes

    def shop_set_object_data(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                             user_input: "ShopUserInput", animation_event_sequence: AnimationEventSequence):
        if user_input.set_shop_object_data_opcode == GameConstants.Opcodes.ObjectData.shop_set_name:
            super().shop_set_object_data(shop_state=shop_state, state_set=state_set,
                                         stack_item=stack_item, user_input=user_input,
                                         animation_event_sequence=animation_event_sequence)
        elif user_input.set_shop_object_data_opcode == GameConstants.Opcodes.ObjectData.shop_set_custom:
            if user_input.target_object is None:
                raise Exception("No target object provided")

            team_match = shop_state.get_object_from_shop_id(shop_id=user_input.target_object.shop_id)
            if team_match is None:
                raise ValueError("Target entity does not exist")

            if GameConstants.ScientificNames.Primates not in team_match.binomial_nomenclature:
                raise ValueError("Target entity is not a primate")

            else:
                self.custom_data["target"] = team_match.shop_id
                self.target = team_match.shop_id
                e = Animations.ShopUpdatedRecruit(shop_id=self.shop_id, state_id=state_set.add_state(shop_state))
                animation_event_sequence.append(e)
        else:
            raise ValueError("Invalid set_object_data opcode")

    def shop_end_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                         animation_event_sequence: AnimationEventSequence):
        self.generic_ability_notification(state=shop_state, state_set=state_set,
                                          description=self.ability[0].name,
                                          animation_event_sequence=animation_event_sequence)
        if self.target is not None:
            target_match = shop_state.get_object_from_shop_id(shop_id=self.target)
            if target_match is not None:
                target_match.shop_buff_stats(health=4,
                                             max_health=4,
                                             shop_state=shop_state,
                                             state_set=state_set,
                                             stack_item=stack_item, buffer=self,
                                             animation_event_sequence=animation_event_sequence)
