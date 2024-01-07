import base64
import importlib

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.objects.base.BaseAnimationEvent import BaseAnimationEvent
from zb7_game_engine.runtime.objects.base.BasePlayerDecisionInfo import BasePlayerDecisionInfo


class PlayerDecisionInfoSerializer(BasePlayerDecisionInfo):

    def to_bytes(self) -> bytearray:
        _bytes = bytearray()
        info_type_bytes = self.info_type_as_int.to_bytes(1, byteorder="big")
        shop_id_bytes = self.shop_id.to_bytes(1, byteorder="big")
        _bytes.extend(info_type_bytes)
        _bytes.extend(shop_id_bytes)
        return _bytes

    def to_base64(self):
        return base64.b64encode(self.to_bytes()).decode("utf-8")

    @classmethod
    def from_base64(cls, _base64: str):
        _bytes = base64.b64decode(_base64)
        return cls.from_bytes(_bytes)

    @staticmethod
    def from_bytes(_bytes: bytes):
        current_index = 0
        info_type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        info_type_as_text = ImmutableData.AnimationEvents.from_int(info_type_as_int)
        module = importlib.import_module(f"zb7_game_engine.serialization.player_decision_info.{info_type_as_text}")
        klass = module.__getattribute__(f"{info_type_as_text}")
        return klass.from_bytes(_bytes)


if __name__ == "__main__":
    # 14 = TreasureChest
    p = PlayerDecisionInfoSerializer(info_type_as_int=14,
                                     shop_id=1)
    p2 = PlayerDecisionInfoSerializer.from_base64(p.to_base64())
