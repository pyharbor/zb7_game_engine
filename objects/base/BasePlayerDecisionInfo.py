import base64
import importlib
import json
from typing import Union

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.GameConstants import GameConstants


class BasePlayerDecisionInfo:

    def __init__(self,
                 info_type_as_text: str = None,
                 info_type_as_int: int = None,
                 shop_id: int = None
                 ):
        if info_type_as_text is None and info_type_as_int is None:
            raise ValueError("BasePlayerDecisionInfo must have a type")

        if info_type_as_text is None:
            info_type_as_text = ImmutableData.AnimationEvents.from_int(info_type_as_int)
        if info_type_as_int is None:
            info_type_as_int = ImmutableData.AnimationEvents.from_text(info_type_as_text)

        self.info_type_as_text = info_type_as_text
        self.info_type_as_int = info_type_as_int
        self.shop_id = shop_id


if __name__ == "__main__":
    pass
