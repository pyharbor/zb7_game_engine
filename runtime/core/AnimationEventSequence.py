from typing import List

from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer


class AnimationEventSequence:
    def __init__(self):
        self.events: List[AnimationEventSerializer] = []

    def to_json(self):
        _json = []
        for event in self.events:
            _json.append(event.to_base64())

        return _json

    @staticmethod
    def from_json(_json):
        sequence = AnimationEventSequence()
        for event in _json:
            sequence.append(AnimationEventSerializer.from_base64(event))
        return sequence

    def append(self, animation: AnimationEventSerializer):
        if animation is None:
            raise ValueError("animation should not be None")
        self.events.append(animation)

    def __iter__(self):
        return iter(self.events)

    def __len__(self):
        return len(self.events)
