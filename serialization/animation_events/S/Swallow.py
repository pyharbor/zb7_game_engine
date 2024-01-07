import base64
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer
from zb7_game_engine.serialization.shared.animation_events.TargetSubject import TargetSubject


class Swallow(AnimationEventSerializer):
    def __init__(self, state_id: int, shop_id: int, battle_id: int, target_shop_id: int, target_battle_id: int):
        super().__init__(animation_type_as_text=GameConstants.Animations.Swallow,
                         state_id=state_id)
        self.shop_id = shop_id
        self.battle_id = battle_id
        self.target_shop_id = target_shop_id
        self.target_battle_id = target_battle_id

    def to_bytes(self) -> bytearray:
        return TargetSubject.to_bytes(self)

    @classmethod
    def from_bytes(cls, _bytes: bytes) -> "Consume":
        return TargetSubject.from_bytes(cls, _bytes)

