import base64
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer
from zb7_game_engine.serialization.shared.animation_events.BasicIds import BasicIds


class HymenopteraReinforcements(AnimationEventSerializer):
    def __init__(self, state_id: int, battle_id: int, shop_id: int):
        super().__init__(animation_type_as_text=GameConstants.Animations.HymenopteraReinforcements,
                         state_id=state_id)
        self.battle_id = battle_id
        self.shop_id = shop_id

    def to_bytes(self) -> bytearray:
        return BasicIds.to_bytes(self)

    @classmethod
    def from_bytes(cls, _bytes: bytes) -> "HymenopteraReinforcements":
        return BasicIds.from_bytes(cls, _bytes)


if __name__ == "__main__":
    HymenopteraReinforcements(state_id=0)