import base64
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer
from zb7_game_engine.serialization.shared.animation_events.BattleId import BattleId


class EntangledWebEffect(AnimationEventSerializer):
    def __init__(self, state_id: int, battle_id: int):
        super().__init__(animation_type_as_text=GameConstants.Animations.EntangledWebEffect,
                         state_id=state_id)
        self.battle_id = battle_id

    def to_bytes(self) -> bytearray:
        return BattleId.to_bytes(self)

    @classmethod
    def from_bytes(cls, _bytes: bytes) -> "EntangledWebEffect":
        return BattleId.from_bytes(cls, _bytes)


if __name__ == "__main__":
    EntangledWebEffect(state_id=0)