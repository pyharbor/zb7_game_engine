import base64
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer
from zb7_game_engine.serialization.shared.animation_events.StateId import StateId


class BattleWon(AnimationEventSerializer):
    def __init__(self, state_id: int):
        super().__init__(animation_type_as_text=GameConstants.Animations.BattleWon,
                         state_id=state_id)
                            
    def to_bytes(self) -> bytearray:
        return StateId.to_bytes(self)

    @classmethod
    def from_bytes(cls, _bytes: bytes) -> "BattleWon":
        return StateId.from_bytes(cls, _bytes)


if __name__ == "__main__":
    BattleWon(state_id=0)