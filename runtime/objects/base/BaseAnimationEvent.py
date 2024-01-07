import base64
import importlib
import json
from typing import Union

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.GameConstants import GameConstants


class BaseAnimationEvent:

    def __init__(self,
                 animation_type_as_text: str = None,
                 animation_type_as_int: int = None,
                 state_id: int = None,
                 custom_data: Union[dict, list] = None
                 ):
        if animation_type_as_text is None and animation_type_as_int is None:
            raise ValueError("AnimationEvent must have a type")

        if animation_type_as_text is None:
            animation_type_as_text = ImmutableData.AnimationEvents.from_int(animation_type_as_int)
        if animation_type_as_int is None:
            animation_type_as_int = ImmutableData.AnimationEvents.from_text(animation_type_as_text)

        self.animation_type_as_text = animation_type_as_text
        self.animation_type_as_int = animation_type_as_int
        self.state_id = state_id
        self.custom_data = custom_data

    def to_bytes(self) -> bytearray:
        raise NotImplementedError()

    @staticmethod
    def from_bytes(_bytes: bytes):
        raise NotImplementedError()


if __name__ == "__main__":
    a = BaseAnimationEvent(animation_type_as_text="shark_bite", animation_type_as_int=12, state_id=1)
    print(a)
    b = a.to_bytes()
    a2 = BaseAnimationEvent.from_bytes(b)
    print(a2)
