import base64
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer
from zb7_game_engine.serialization.shared.animation_events.BasicIds import BasicIds


class ShopUpdatedRelic(AnimationEventSerializer):
    def __init__(self, state_id: int, shop_id: int, battle_id: int):
        super().__init__(animation_type_as_text=GameConstants.Animations.ShopUpdatedRelic,
                         state_id=state_id)
        self.shop_id = shop_id
        self.battle_id = battle_id                        
                            
    def to_bytes(self) -> bytearray:
        return BasicIds.to_bytes(self)

    @classmethod
    def from_bytes(cls, _bytes: bytes) -> "ShopUpdatedRelic":
        return BasicIds.from_bytes(cls, _bytes)


if __name__ == "__main__":
    ShopUpdatedRelic(state_id=0)