
import base64
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer


class GenericAbilityNotification(AnimationEventSerializer):
    def __init__(self, state_id: int, shop_id: int, battle_id: int, description: str):
        super().__init__(animation_type_as_text=GameConstants.Animations.GenericAbilityNotification,
                         state_id=state_id)
        self.shop_id = shop_id
        self.battle_id = battle_id
        self.description = description
                            
    def to_bytes(self) -> bytearray:
        _bytes = bytearray()
        animation_type_bytes = self.animation_type_as_int.to_bytes(1, byteorder="big")
        state_id_bytes = self.state_id.to_bytes(2, byteorder="big")

        if self.battle_id is None:
            battle_id_bytes = int(0).to_bytes(1, byteorder="big")
        else:
            battle_id_bytes = self.battle_id.to_bytes(1, byteorder="big")
        shop_id_bytes = self.shop_id.to_bytes(1, byteorder="big")
        description_bytes = self.description.encode("utf-8")
        description_length_bytes = len(description_bytes).to_bytes(1, byteorder="big")

        _bytes.extend(animation_type_bytes)
        _bytes.extend(state_id_bytes)
        _bytes.extend(battle_id_bytes)
        _bytes.extend(shop_id_bytes)
        _bytes.extend(description_length_bytes)
        _bytes.extend(description_bytes)
        return _bytes

    @classmethod
    def from_bytes(cls, _bytes: bytes) -> "GenericAbilityNotification":
        current_index = 0
        animation_type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        state_id = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 1
        battle_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        shop_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        description_length = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        description = _bytes[current_index:current_index + description_length].decode("utf-8")
        current_index += description_length

        return cls(state_id=state_id, shop_id=shop_id, battle_id=battle_id, description=description)


if __name__ == "__main__":
    GenericAbilityNotification(state_id=0, shop_id=0, battle_id=0, description="test")