import base64
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer


class SeaOtter(AnimationEventSerializer):
    def __init__(self, state_id: int, shop_id: int, battle_id: int, result_as_int: int):
        super().__init__(animation_type_as_text=GameConstants.Animations.SeaOtter,
                         state_id=state_id)
        self.shop_id = shop_id
        self.battle_id = battle_id
        self.result_as_int = result_as_int
        self.int_to_map = {
            1: "seaweed",
            2: "nothing",
            3: "clam",
            4: "gold",
        }
        self.text_to_int_map = {v: k for k, v in self.int_to_map.items()}
        self.result_as_int = result_as_int
        self.result_as_text = self.int_to_map[result_as_int]
                            
    def to_bytes(self) -> bytearray:
        _bytes = bytearray()
        animation_type_bytes = self.animation_type_as_int.to_bytes(1, byteorder="big")
        state_id_bytes = self.state_id.to_bytes(2, byteorder="big")
        shop_id_bytes = self.shop_id.to_bytes(1, byteorder="big")
        battle_id_bytes = self.battle_id.to_bytes(1, byteorder="big")
        result_bytes = self.result_as_int.to_bytes(1, byteorder="big")
        _bytes.extend(animation_type_bytes)
        _bytes.extend(state_id_bytes)
        _bytes.extend(shop_id_bytes)
        _bytes.extend(battle_id_bytes)
        _bytes.extend(result_bytes)
        return _bytes

    @classmethod
    def from_bytes(cls, _bytes: bytes) -> "SeaOtter":
        current_index = 0
        animation_type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        state_id = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 1
        shop_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        battle_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        result_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        return cls(state_id=state_id, shop_id=shop_id, battle_id=battle_id, result_as_int=result_as_int)


if __name__ == "__main__":
    SeaOtter(state_id=0)