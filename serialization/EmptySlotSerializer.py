import base64
import importlib

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature
from zb7_game_engine.runtime.objects.base.BaseRecruit import BaseRecruit
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus
from zb7_game_engine.serialization.StatusSerializer import StatusSerializer
from zb7_game_engine.serialization.misc.BitFlags import BitFlags


class EmptySlotSerializer(BaseRecruit):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=225,
                         sub_type_as_text="EmptySlot",
                         **kwargs)

    @classmethod
    def from_human_readable_json(cls, _json: dict):
        pass

    def to_human_readable_json(self) -> dict:
        pass

    def to_base64(self):
        return base64.b64encode(self.to_bytes()).decode("utf-8")

    def to_bytes(self):
        _bytes = bytearray()
        subtype_bytes = self.sub_type_as_int.to_bytes(length=2, byteorder="big")
        team_index_bytes = self.team_index.to_bytes(length=1, byteorder="big")
        shop_id_bytes = self.shop_id.to_bytes(length=1, byteorder="big")

        _bytes.extend(subtype_bytes)
        _bytes.extend(team_index_bytes)
        _bytes.extend(shop_id_bytes)
        return _bytes

    @classmethod
    def from_base64(cls, base64_string: str) -> "EmptySlotSerlializer":
        _bytes = base64.b64decode(base64_string)
        return cls.from_bytes(_bytes)

    @classmethod
    def bytes_to_custom_data(cls, _bytes: bytes, current_index: int) -> dict:
        return {}

    @classmethod
    def custom_data_to_bytes(cls) -> bytes:
        return b""

    @classmethod
    def from_bytes(cls, _bytes: bytes) -> "EmptySlotSerlializer":
        current_index = 0
        sub_type_as_int = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        sub_type_as_text = ImmutableData.Subtype.from_int(sub_type_as_int)["sub_type_as_text"]
        current_index += 2
        team_index = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        shop_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1

        return EmptySlotSerializer(
            sub_type_as_int=sub_type_as_int,
            sub_type_as_text=sub_type_as_text,
            team_index=team_index,
            shop_id=shop_id
        )

    def to_base64_minimal(self):
        _bytes = bytearray()
        subtype_bytes = self.sub_type_as_int.to_bytes(length=2, byteorder="big")
        shop_id_bytes = self.shop_id.to_bytes(length=1, byteorder="big")
        _bytes.extend(subtype_bytes)
        _bytes.extend(shop_id_bytes)
        base64_bytes = base64.b64encode(_bytes)
        return base64_bytes.decode("utf-8")

    @staticmethod
    def from_base64_minimal(base64_string: str):
        _bytes = base64.b64decode(base64_string)
        current_index = 0
        sub_type_as_int = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        immutable_data = ImmutableData.Subtype.from_int(sub_type_as_int)
        binomial_nomenclature = BinomialNomenclature.from_json(immutable_data["binomial_nomenclature"])
        species = binomial_nomenclature.get_main_species()
        sub_type_as_text = immutable_data["sub_type_as_text"]
        module = importlib.import_module(f"zb7_game_engine.runtime.objects.recruits.{species}.{sub_type_as_text}")
        klass = module.__getattribute__(f"{sub_type_as_text}")

        current_index += 2
        shop_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1

        return klass(
            sub_type_as_int=sub_type_as_int,
            sub_type_as_text=sub_type_as_text,
            shop_id=shop_id,
            type="EmptySlot"
        )

    def copy(self):
        self.to_bytes()
        return self.from_bytes(self.to_bytes())


if __name__ == "__main__":
    e = EmptySlotSerializer(shop_id=1)
    print(e.to_base64())
    print(e.to_base64_minimal())