import base64

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer


class AdaptToNewSpecies(AnimationEventSerializer):
    def __init__(self, state_id: int, shop_id: int, battle_id: int, type_as_int: int):
        super().__init__(animation_type_as_text=GameConstants.Animations.AdaptToNewSpecies,
                         state_id=state_id)
        self.shop_id = shop_id
        self.battle_id = battle_id
        self.type_as_int = type_as_int
        self.type_as_text = ImmutableData.ScientificNomenclature.from_int(self.type_as_int)
                            
    def to_bytes(self) -> bytearray:
        _bytes = bytearray()
        animation_type_bytes = self.animation_type_as_int.to_bytes(1, byteorder="big")
        state_id_bytes = self.state_id.to_bytes(2, byteorder="big")
        shop_id_bytes = self.shop_id.to_bytes(1, byteorder="big")
        battle_id_bytes = self.battle_id.to_bytes(1, byteorder="big")
        type_as_int_bytes = self.type_as_int.to_bytes(1, byteorder="big")
        _bytes.extend(animation_type_bytes)
        _bytes.extend(state_id_bytes)
        _bytes.extend(shop_id_bytes)
        _bytes.extend(battle_id_bytes)
        _bytes.extend(type_as_int_bytes)
        return _bytes

    @classmethod
    def from_bytes(cls, _bytes: bytes) -> "AdaptToNewSpecies":
        current_index = 0
        animation_type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        state_id = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 1
        shop_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        battle_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        return cls(state_id=state_id, shop_id=shop_id, battle_id=battle_id, type_as_int=type_as_int)


if __name__ == "__main__":
    AdaptToNewSpecies(state_id=0)