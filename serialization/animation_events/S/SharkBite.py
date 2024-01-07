import base64
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer
from zb7_game_engine.serialization.shared.animation_events.TargetSubjectAmount import TargetSubjectAmount


class SharkBite(AnimationEventSerializer):
    def __init__(self, state_id: int, shop_id: int, battle_id: int, target_shop_id: int, target_battle_id: int, amount: int):
        super().__init__(animation_type_as_text=GameConstants.Animations.SharkBite,
                         state_id=state_id)
        self.battle_id = battle_id
        self.shop_id = shop_id
        self.target_battle_id = target_battle_id
        self.target_shop_id = target_shop_id
        self.amount = amount

    def to_bytes(self) -> bytearray:
        return TargetSubjectAmount.to_bytes(self)

    @classmethod
    def from_bytes(cls, _bytes: bytes) -> "SharkBite":
        return TargetSubjectAmount.from_bytes(cls, _bytes)


if __name__ == "__main__":
    SharkBite(state_id=0)