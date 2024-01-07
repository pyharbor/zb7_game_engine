import importlib

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus


class StatusSerializer(BaseStatus):

    @classmethod
    def from_human_readable_json(cls, _json: dict):
        pass

    def to_human_readable_json(self) -> dict:
        pass

    @classmethod
    def from_config_json(cls, _json: dict):
        sub_type_as_int = _json["sub_type_as_int"]
        immutable_data = ImmutableData.Subtype.from_int(sub_type_as_int)
        sub_type_as_text = immutable_data["sub_type_as_text"]
        module = importlib.import_module(f"zb7_game_engine.runtime.objects.statuses.{sub_type_as_text[0]}.{sub_type_as_text}")
        klass = module.__getattribute__(f"{sub_type_as_text}")
        return klass()

    def to_base64(self):
        raise NotImplementedError

    @staticmethod
    def from_base64(_bytes: bytes):
        raise NotImplementedError

    def to_bytes(self):
        _bytes = bytearray()
        subtype_bytes = self.sub_type_as_int.to_bytes(length=2, byteorder="big")
        counter_bytes = self.counter.to_bytes(length=2, byteorder="big")
        _bytes.extend(subtype_bytes)
        _bytes.extend(counter_bytes)
        return _bytes

    @staticmethod
    def from_bytes(_bytes: bytes) -> "StatusSerializer":
        current_index = 0
        sub_type_as_int = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 2
        sub_type_as_text = ImmutableData.Subtype.from_int(sub_type_as_int)["sub_type_as_text"]
        counter = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 2

        module = importlib.import_module(
            f"zb7_game_engine.runtime.objects.statuses.{sub_type_as_text[0]}.{sub_type_as_text}")
        klass = module.__getattribute__(f"{sub_type_as_text}")
        return klass(
            sub_type_as_int=sub_type_as_int,
            sub_type_as_text=sub_type_as_text,
            counter=counter
        )

    def __str__(self):
        return f"{self.sub_type_as_text}(counter={self.counter})"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    pass
