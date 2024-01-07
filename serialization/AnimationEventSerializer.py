import base64
import importlib

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.objects.base.BaseAnimationEvent import BaseAnimationEvent


class AnimationEventSerializer(BaseAnimationEvent):

    @classmethod
    def from_human_readable_json(cls, _json: dict):
        pass

    def to_human_readable_json(self) -> dict:
        pass

    def to_bytes(self) -> bytearray:
        _bytes = bytearray()
        animation_type_bytes = self.animation_type_as_int.to_bytes(1, byteorder="big")
        if self.state_id is None:
            state_id_bytes = bytearray([255, 255])
        else:
            state_id_bytes = self.state_id.to_bytes(2, byteorder="big")
        _bytes.extend(animation_type_bytes)
        _bytes.extend(state_id_bytes)
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
        animation_type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        animation_type_as_text = ImmutableData.AnimationEvents.from_int(animation_type_as_int)
        module = importlib.import_module(f"zb7_game_engine.serialization.animation_events.{animation_type_as_text[0]}.{animation_type_as_text}")
        klass = module.__getattribute__(f"{animation_type_as_text}")
        return klass.from_bytes(_bytes)


if __name__ == "__main__":
    pass
