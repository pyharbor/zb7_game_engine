from zb7_game_engine.immutable_data.ImmutableData import ImmutableData


class SeaOtterCD:

    @staticmethod
    def custom_data_to_bytes(self) -> bytes:
        _bytes = bytearray()
        trigger_as_bytes = self.custom_data["trigger"].to_bytes(length=1, byteorder="big")
        _bytes.extend(trigger_as_bytes)
        for sub_type_as_text, stats in self.custom_data.items():
            if sub_type_as_text == "trigger":
                continue
            sub_type_as_int = ImmutableData.Subtype.from_text(sub_type_as_text)["sub_type_as_int"]
            subtype_bytes = sub_type_as_int.to_bytes(length=2, byteorder="big")
            experience = stats["experience"].to_bytes(length=1, byteorder="big")
            _bytes.extend(subtype_bytes)
            _bytes.extend(experience)

        return _bytes

    @staticmethod
    def bytes_to_custom_data(_bytes: bytes, current_index: int) -> dict:
        custom_data = {}
        trigger = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        custom_data["trigger"] = trigger
        while current_index < len(_bytes):
            sub_type_as_int = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
            sub_type_as_text = ImmutableData.Subtype.from_int(sub_type_as_int)["sub_type_as_text"]
            current_index += 2
            experience = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
            current_index += 1
            custom_data[sub_type_as_text] = {
                "experience": experience
            }
        return custom_data