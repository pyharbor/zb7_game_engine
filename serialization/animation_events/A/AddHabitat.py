import base64

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer


class AddHabitat(AnimationEventSerializer):
    def __init__(self, state_id: int, shop_id: int = None, battle_id: int = None, habitat_as_int: int = None):
        super().__init__(animation_type_as_text=GameConstants.Animations.AddHabitat,
                         state_id=state_id)
        self.shop_id = shop_id
        self.battle_id = battle_id
        self.habitat_as_int = habitat_as_int
        self.habitat_as_text = ImmutableData.Habitats.from_int(self.habitat_as_int)

    def to_bytes(self) -> bytearray:
        _bytes = bytearray()
        animation_type_bytes = self.animation_type_as_int.to_bytes(1, byteorder="big")
        state_id_bytes = self.state_id.to_bytes(2, byteorder="big")
        shop_id_bytes = self.shop_id.to_bytes(1, byteorder="big")
        if self.battle_id is None:
            battle_id_bytes = (0).to_bytes(1, byteorder="big")
        else:
            battle_id_bytes = self.battle_id.to_bytes(1, byteorder="big")
        species_as_int_bytes = self.habitat_as_int.to_bytes(1, byteorder="big")
        _bytes.extend(animation_type_bytes)
        _bytes.extend(state_id_bytes)
        _bytes.extend(shop_id_bytes)
        _bytes.extend(battle_id_bytes)
        _bytes.extend(species_as_int_bytes)
        return _bytes

    @classmethod
    def from_bytes(cls, _bytes: bytes) -> "AddHabitat":
        current_index = 0
        animation_type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        state_id = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 1
        shop_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        battle_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        habitat_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        return cls(state_id=state_id, shop_id=shop_id, battle_id=battle_id, habitat_as_int=habitat_as_int)


if __name__ == "__main__":
    AddHabitat(state_id=0)