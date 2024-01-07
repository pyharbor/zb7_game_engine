
import base64
from typing import List

from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer


class Group(AnimationEventSerializer):
    def __init__(self, state_id: int = None):
        super().__init__(animation_type_as_text=GameConstants.Animations.Group)
        self.animation_events: List[AnimationEventSerializer] = []
        self.state_id = state_id
                            
    def to_bytes(self) -> bytearray:
        _bytes = bytearray()
        animation_type_bytes = self.animation_type_as_int.to_bytes(1, byteorder="big")
        state_id_bytes = self.state_id.to_bytes(2, byteorder="big")
        _bytes.extend(animation_type_bytes)
        _bytes.extend(state_id_bytes)
        for event in self.animation_events:
            event_bytes = event.to_bytes()
            event_bytes_length = len(event_bytes).to_bytes(2, byteorder="big")
            _bytes.extend(event_bytes_length)
            _bytes.extend(event_bytes)

        return _bytes

    @classmethod
    def from_bytes(cls, _bytes: bytes) -> "Group":
        current_index = 0
        animation_type_as_int = int.from_bytes(_bytes[current_index: current_index + 1], byteorder="big")
        current_index += 1
        state_id = int.from_bytes(_bytes[current_index: current_index + 2], byteorder="big")
        current_index += 2
        group = cls(state_id=state_id)
        while current_index < len(_bytes):
            event_length = int.from_bytes(_bytes[current_index: current_index + 2], byteorder="big")
            current_index += 2
            event_bytes = _bytes[current_index: current_index + event_length]
            current_index += event_length
            event = AnimationEventSerializer.from_bytes(event_bytes)
            group.add_animation_event(event)
        return group

    def add_animation_event(self, animation_event: AnimationEventSerializer):
        self.animation_events.append(animation_event)

    def set_state_id(self, state_id: int):
        self.state_id = state_id
        for event in self.animation_events:
            event.state_id = state_id


if __name__ == "__main__":
    g = Group(state_id=0)