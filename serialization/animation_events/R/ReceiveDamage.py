import base64

from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer
from zb7_game_engine.serialization.shared.animation_events.DamageReductionStack import DamageReductionStack


class ReceiveDamage(AnimationEventSerializer):
    def __init__(self, state_id: int, shop_id: int, battle_id: int,
                 damage_reduction_stack: list, damage_after_modifications: int,
                 damage_before_modifications: int):
        super().__init__(animation_type_as_text=GameConstants.Animations.ReceiveDamage,
                         state_id=state_id)
        self.damage_reduction_stack = damage_reduction_stack
        self.damage_after_modifications = damage_after_modifications
        self.damage_before_modifications = damage_before_modifications
        self.battle_id = battle_id
        self.shop_id = shop_id

    def to_bytes(self) -> bytearray:
        return DamageReductionStack.to_bytes(self)

    @classmethod
    def from_bytes(cls, _bytes: bytes) -> "ReceiveDamage":
        return DamageReductionStack.from_bytes(cls, _bytes)

    def __str__(self):
        return f"ReceiveDamage(state_id={self.state_id}, damage_reduction_stack={self.damage_reduction_stack}, damage_after_modifications={self.damage_after_modifications}, damage_before_modifications={self.damage_before_modifications}, battle_id={self.battle_id}, shop_id={self.shop_id})"


if __name__ == "__main__":
    damage_reduction_stack = [
        dict(amount=4, sub_type_as_int=1),
    ]
    r = ReceiveDamage(damage_reduction_stack=damage_reduction_stack,
                      damage_after_modifications=12,
                      damage_before_modifications=16,
                      battle_id=3,
                      shop_id=2,
                      state_id=1,
                      )
    print(r.to_base64())
    r2 = ReceiveDamage.from_base64(r.to_base64())
    print(r2.to_base64())
    print(r2)
    print(r)
