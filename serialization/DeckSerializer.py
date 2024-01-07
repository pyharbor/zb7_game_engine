import base64
import importlib

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.Deck import Deck
from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature
from zb7_game_engine.runtime.objects.recruits.Recruits import Recruits


class DeckSerializer(Deck):

    def __init__(self, objects: list):
        super().__init__(objects=objects)
        self.base64_text = self.to_base64_text()

    @classmethod
    def from_human_readable_json(cls, _json: dict):
        pass

    def to_human_readable_json(self) -> dict:
        pass

    def to_base64_text(self) -> str:
        _bytes = self.to_bytes()
        return base64.b64encode(_bytes).decode("utf-8")

    def to_bytes(self) -> bytes:
        _bytes = bytearray()
        for obj in sorted(self.objects, key=lambda x: x.sub_type_as_text):
            sub_type_as_bytes = obj.sub_type_as_int.to_bytes(2, byteorder="big")
            aaid_bytes = obj.aaid.to_bytes(1, byteorder="big")
            _bytes.extend(sub_type_as_bytes + aaid_bytes)

        return _bytes

    @staticmethod
    def from_bytes(_bytes: bytes) -> "DeckSerializer":
        objects = []
        for x in range(0, len(_bytes), 3):
            sub_type_as_int = int.from_bytes(_bytes[x: x + 2], byteorder="big")
            aaid = int.from_bytes(_bytes[x+2: x + 3], byteorder="big")
            immutable_data = ImmutableData.Subtype.from_int(sub_type_as_int)
            sub_type_as_text = immutable_data["sub_type_as_text"]
            if immutable_data["type"] == "Recruit":
                binomial_nomenclature = BinomialNomenclature.from_json(immutable_data["binomial_nomenclature"])
                species = binomial_nomenclature.get_main_species()
                module = importlib.import_module(f"zb7_game_engine.runtime.objects.recruits.{species}.{sub_type_as_text}")
                klass = module.__getattribute__(f"{sub_type_as_text}")
            elif immutable_data["type"] == "Relic":
                module = importlib.import_module(f"zb7_game_engine.runtime.objects.relics.{sub_type_as_text[0]}.{sub_type_as_text}")
                klass = module.__getattribute__(f"{sub_type_as_text}")
            else:
                raise ValueError(f"Unknown type: {immutable_data['type']}")
            obj = klass(aaid=aaid)
            objects.append(obj)
        return DeckSerializer(objects=objects)

    @staticmethod
    def from_base64_text(base64_str: str) -> "DeckSerializer":
        _bytes = base64.b64decode(base64_str)
        return DeckSerializer.from_bytes(_bytes)


if __name__ == "__main__":
    d = DeckSerializer(objects=[Recruits.Reptilia.RainbowAgama()])
    d2 = DeckSerializer.from_bytes(d.to_bytes())
    d3 = DeckSerializer.from_base64_text(d.to_base64_text())
    for x in d2.objects:
        print(x.sub_type_as_text)

    for x in d3.objects:
        print(x.sub_type_as_text)

    print(d.to_base64_text(), len(d.to_base64_text()))