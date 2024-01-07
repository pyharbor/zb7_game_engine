import base64
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer
from zb7_game_engine.serialization.shared.animation_events.BasicIdsAmount import BasicIdsAmount


class Heal(AnimationEventSerializer):
    def __init__(self, state_id: int, battle_id: int, shop_id: int, amount: int):
        super().__init__(animation_type_as_text=GameConstants.Animations.Heal,
                         state_id=state_id)
        self.battle_id = battle_id
        self.shop_id = shop_id
        self.amount = amount

    def to_bytes(self) -> bytearray:
        return BasicIdsAmount.to_bytes(self)

    @classmethod
    def from_bytes(cls, _bytes: bytes) -> "Heal":
        return BasicIdsAmount.from_bytes(cls, _bytes)

if __name__ == "__main__":
    Heal(state_id=0)