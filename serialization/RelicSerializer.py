import base64
import importlib
import json

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.objects.base.BaseRelic import BaseRelic


class RelicSerializer(BaseRelic):

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
        module = importlib.import_module(f"zb7_game_engine.runtime.objects.relics.{sub_type_as_text[0]}.{sub_type_as_text}")
        klass = module.__getattribute__(f"{sub_type_as_text}")
        rarity = _json["rarity"]
        return klass(
            sub_type_as_int=_json["sub_type_as_int"],
            sub_type_as_text=sub_type_as_text,
            initiative=_json["initiative"],
            experience=1,
            rarity=rarity
        )

    @classmethod
    def bytes_to_custom_data(cls, _bytes: bytes, current_index: int) -> dict:
        return {}

    @classmethod
    def custom_data_to_bytes(cls) -> bytes:
        return b""

    def to_bytes_minimal(self):
        _bytes = bytearray()
        subtype_bytes = self.sub_type_as_int.to_bytes(length=2, byteorder="big")
        shop_id_bytes = self.shop_id.to_bytes(length=1, byteorder="big")
        aaid_bytes = self.aaid.to_bytes(length=1, byteorder="big")
        _bytes.extend(subtype_bytes)
        _bytes.extend(shop_id_bytes)
        _bytes.extend(aaid_bytes)
        return _bytes

    def to_base64_minimal(self):
        _bytes = self.to_bytes_minimal()
        base64_bytes = base64.b64encode(_bytes)
        return base64_bytes.decode("utf-8")

    @staticmethod
    def from_bytes_minimal(_bytes: bytes):
        current_index = 0
        sub_type_as_int = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        sub_type_as_text = ImmutableData.Subtype.from_int(sub_type_as_int)["sub_type_as_text"]
        current_index += 2
        shop_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        aaid = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1

        module = importlib.import_module(
            f"zb7_game_engine.runtime.objects.relics.{sub_type_as_text[0]}.{sub_type_as_text}")
        klass = module.__getattribute__(f"{sub_type_as_text}")
        return klass(
            sub_type_as_int=sub_type_as_int,
            sub_type_as_text=sub_type_as_text,
            shop_id=shop_id,
            aaid=aaid,
            type="Relic"
        )

    @staticmethod
    def from_base64_minimal(base64_string: str):
        _bytes = base64.b64decode(base64_string)
        return RelicSerializer.from_bytes_minimal(_bytes)

    def to_base64(self):
        _bytes = self.to_bytes()
        base64_bytes = base64.b64encode(_bytes)
        return base64_bytes.decode("utf-8")

    @staticmethod
    def from_base64(base64_string: str):
        _bytes = base64.b64decode(base64_string)
        return RelicSerializer.from_bytes(_bytes)

    def to_bytes(self):
        _bytes = bytearray()
        subtype_bytes = self.sub_type_as_int.to_bytes(length=2, byteorder="big")
        experience_bytes = self._experience.to_bytes(length=2, byteorder="big")
        initiative_as_int = ImmutableData.Initiative.to_int(self._initiative)
        initiative_bytes = initiative_as_int.to_bytes(length=2, byteorder="big")
        cost_bytes = self._cost.to_bytes(length=1, byteorder="big")
        shop_id_bytes = self.shop_id.to_bytes(length=1, byteorder="big")
        if self.battle_id is None:
            battle_id_bytes = int(0).to_bytes(length=1, byteorder="big")
        else:
            battle_id_bytes = self.battle_id.to_bytes(length=1, byteorder="big")
        aaid_bytes = self._aaid.to_bytes(length=1, byteorder="big")
        # convert a variable length string into bytes
        custom_data_bytes = self.custom_data_to_bytes()

        _bytes.extend(subtype_bytes)
        _bytes.extend(experience_bytes)
        _bytes.extend(initiative_bytes)
        _bytes.extend(cost_bytes)
        _bytes.extend(shop_id_bytes)
        _bytes.extend(battle_id_bytes)
        _bytes.extend(aaid_bytes)
        _bytes.extend(custom_data_bytes)
        return _bytes

    @staticmethod
    def from_bytes(_bytes):
        current_index = 0
        sub_type_as_int = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        sub_type_as_text = ImmutableData.Subtype.from_int(sub_type_as_int)["sub_type_as_text"]
        if sub_type_as_text == "GraduationCap":
            pass
        module = importlib.import_module(
            f"zb7_game_engine.runtime.objects.relics.{sub_type_as_text[0]}.{sub_type_as_text}")
        klass = module.__getattribute__(f"{sub_type_as_text}")

        current_index += 2
        experience = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 2
        initiative_as_int = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        initiative_as_float = ImmutableData.Initiative.from_int(initiative_as_int)
        current_index += 2

        cost = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1

        shop_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1

        battle_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1

        aaid = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        custom_data = klass.bytes_to_custom_data(_bytes, current_index)

        return klass(
            sub_type_as_int=sub_type_as_int,
            sub_type_as_text=sub_type_as_text,
            triggers=[],
            initiative=initiative_as_float,
            experience=experience,
            cost=cost,
            shop_id=shop_id,
            battle_id=battle_id,
            random_seed=1,
            custom_data=custom_data,
            options={},
            aaid=aaid
        )

    def copy(self):
        self.to_bytes()
        return self.from_bytes(self.to_bytes())