import base64

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer


class AddStatus(AnimationEventSerializer):
    def __init__(self, state_id: int, battle_id: int, shop_id: int, status_sub_type_as_int: int, amount: int):
        super().__init__(animation_type_as_text=GameConstants.Animations.AddStatus,
                         state_id=state_id)
        self.battle_id = battle_id
        self.shop_id = shop_id
        self.status_sub_type_as_int = status_sub_type_as_int
        self.status_sub_type_as_text = ImmutableData.Subtype.from_int(status_sub_type_as_int)["sub_type_as_text"]
        self.amount = amount

    def to_bytes(self) -> bytearray:
        _bytes = bytearray()
        animation_type_bytes = self.animation_type_as_int.to_bytes(1, byteorder="big")
        state_id_bytes = self.state_id.to_bytes(2, byteorder="big")
        status_sub_type_as_int_bytes = self.status_sub_type_as_int.to_bytes(2, byteorder="big")
        shop_id_bytes = self.shop_id.to_bytes(1, byteorder="big")
        battle_id_bytes = self.battle_id.to_bytes(1, byteorder="big")
        amount_bytes = self.amount.to_bytes(2, byteorder="big")

        _bytes.extend(animation_type_bytes)
        _bytes.extend(state_id_bytes)
        _bytes.extend(status_sub_type_as_int_bytes)
        _bytes.extend(shop_id_bytes)
        _bytes.extend(battle_id_bytes)
        _bytes.extend(amount_bytes)

        return _bytes

    @classmethod
    def from_bytes(cls, _bytes: bytes) -> "AddStatus":
        current_index = 0
        animation_type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        state_id = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 2
        status_sub_type_as_int = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 2
        shop_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        battle_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        amount = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 2

        return cls(state_id=state_id,
                   battle_id=battle_id,
                   shop_id=shop_id,
                   status_sub_type_as_int=status_sub_type_as_int,
                   amount=amount)


if __name__ == "__main__":
    AddStatus(state_id=0)