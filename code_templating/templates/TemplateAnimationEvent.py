import base64
from typing import Union

import importlib
import inspect

from zb7_game_engine.code_templating.FunctionSourceCode import FunctionSourceCode
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer


class TemplateAnimationEvent(AnimationEventSerializer):

    def to_bytes(self) -> bytearray:
        _bytes = bytearray()
        animation_type_bytes = self.animation_type_as_int.to_bytes(1, byteorder="big")
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

    @classmethod
    def from_bytes(cls, _bytes: bytes):
        current_index = 0
        animation_type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        state_id = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 2
        return cls(animation_type_as_int=animation_type_as_int)