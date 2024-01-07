import base64

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.serialization.EmptySlotSerializer import EmptySlotSerializer
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer


class ObjectParser:
    @staticmethod
    def from_base64_text(base64_str):
        _bytes = base64.b64decode(base64_str)
        current_index = 0
        subtype_as_int = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        type = ImmutableData.Subtype.from_int(subtype_as_int)["type"]
        if type == "Relic":
            return RelicSerializer.from_base64(base64_str)
        elif type == "Recruit":
            return RecruitSerializer.from_base64(base64_str)
        elif type == "EmptySlot":
            return EmptySlotSerializer.from_base64(base64_str)

    @staticmethod
    def from_base64_text_minimal(base64_str):
        _bytes = base64.b64decode(base64_str)
        current_index = 0
        subtype_as_int = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        type = ImmutableData.Subtype.from_int(subtype_as_int)["type"]
        if type == "Relic":
            return RelicSerializer.from_base64_minimal(base64_str)
        elif type == "Recruit":
            return RecruitSerializer.from_base64_minimal(base64_str)
        elif type == "EmptySlot":
            return EmptySlotSerializer.from_base64_minimal(base64_str)

    @staticmethod
    def from_bytes_minimal(_bytes):
        current_index = 0
        subtype_as_int = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        type = ImmutableData.Subtype.from_int(subtype_as_int)["type"]
        if type == "Relic":
            return RelicSerializer.from_bytes_minimal(_bytes)
        elif type == "Recruit":
            return RecruitSerializer.from_bytes_minimal(_bytes)


