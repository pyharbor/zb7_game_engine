class BattleId:
    @staticmethod
    def to_bytes(self) -> bytearray:
        _bytes = bytearray()
        animation_type_bytes = self.animation_type_as_int.to_bytes(1, byteorder="big")
        state_id_bytes = self.state_id.to_bytes(2, byteorder="big")
        battle_id_bytes = self.battle_id.to_bytes(1, byteorder="big")
        _bytes.extend(animation_type_bytes)
        _bytes.extend(state_id_bytes)
        _bytes.extend(battle_id_bytes)
        return _bytes

    @staticmethod
    def from_bytes(cls, _bytes: bytes):
        current_index = 0
        animation_type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        state_id = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 1
        battle_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        return cls(state_id=state_id, battle_id=battle_id)