import base64
import importlib
import json
from typing import Union
from zb7_game_engine.immutable_data.ImmutableData import ImmutableData


class AnimationEvent:

    def __init__(self,
                 animation_type_as_text: str = None,
                 animation_type_as_int: int = None,
                 state_id: int = None,
                 custom_data: dict = None,
                 ):
        if animation_type_as_text is None and animation_type_as_int is None:
            raise ValueError("AnimationEvent must have a type")

        if state_id is None:
            raise ValueError("AnimationEvent must have a state_id")

        if animation_type_as_text is None:
            animation_type_as_text = ImmutableData.AnimationEvents.from_int(animation_type_as_int)
        if animation_type_as_int is None:
            animation_type_as_int = ImmutableData.AnimationEvents.from_text(animation_type_as_text)

        self.animation_type_as_text = animation_type_as_text
        self.animation_type_as_int = animation_type_as_int
        self.state_id = state_id
        self.custom_data = custom_data or {}

    def __str__(self):
        return json.dumps(self.__dict__)

