from zb7_game_engine.immutable_data.ImmutableData import ImmutableData


class Uint8ArrayOfScientificNomenclature:

    @staticmethod
    def bytes_to_custom_data(_bytes: bytes, current_index: int) -> dict:
            len_encountered_types = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
            current_index += 1
            encountered_types = []
            if len_encountered_types > 0:
                for x in range(len_encountered_types):
                    type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
                    current_index += 1
                    type_as_text = ImmutableData.ScientificNomenclature.from_int(type_as_int)
                    encountered_types.append(type_as_text)
            else:
                encountered_types = []
            return {"encountered_types": encountered_types}

    @staticmethod
    def custom_data_to_bytes(self) -> bytes:

        _bytes = bytearray()
        len_encountered_types = int(0).to_bytes(1, byteorder="big")
        encountered_types_bytes = bytearray()
        if len(self.custom_data["encountered_types"]) > 0:
            for x in self.custom_data["encountered_types"]:
                type_as_int = ImmutableData.ScientificNomenclature.to_int(x)
                encountered_types_bytes.extend(type_as_int.to_bytes(1, byteorder="big"))
            len_encountered_types = len(encountered_types_bytes).to_bytes(1, byteorder="big")
        _bytes.extend(len_encountered_types)
        _bytes.extend(encountered_types_bytes)
        return _bytes