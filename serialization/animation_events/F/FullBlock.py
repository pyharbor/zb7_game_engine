import base64
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer
from zb7_game_engine.serialization.shared.animation_events.DamageReductionStack import DamageReductionStack


class FullBlock(AnimationEventSerializer):
    def __init__(self, state_id: int, shop_id: int, battle_id: int,
                 damage_reduction_stack: list, damage_after_modifications: int,
                 damage_before_modifications: int):
        super().__init__(animation_type_as_text=GameConstants.Animations.FullBlock,
                         state_id=state_id)
        self.battle_id = battle_id
        self.shop_id = shop_id
        self.damage_reduction_stack = damage_reduction_stack
        self.damage_after_modifications = damage_after_modifications
        self.damage_before_modifications = damage_before_modifications

    def to_bytes(self) -> bytearray:
        return DamageReductionStack.to_bytes(self)

    @classmethod
    def from_bytes(cls, _bytes: bytes) -> "FullBlock":
        return DamageReductionStack.from_bytes(cls, _bytes)



if __name__ == "__main__":
    FullBlock(state_id=0)
