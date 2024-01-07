import base64
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer
from zb7_game_engine.serialization.misc.BitFlags import BitFlags
from zb7_game_engine.serialization.shared.animation_events.StatsModification import StatsModification


class DebuffStats(AnimationEventSerializer):
    def __init__(self, state_id: int, shop_id: int, battle_id: int, health: int, melee: int, ranged: int, armor: int,
                 initiative: int, max_health: int):
        super().__init__(animation_type_as_text=GameConstants.Animations.DebuffStats,
                         state_id=state_id)
        self.health = health
        self.melee = melee
        self.ranged = ranged
        self.armor = armor
        self.initiative = initiative
        self.max_health = max_health
        self.shop_id = shop_id
        self.battle_id = battle_id

    def to_bytes(self) -> bytearray:
        return StatsModification.to_bytes(self)

    @classmethod
    def from_bytes(cls, _bytes: bytes) -> "DebuffStats":
        return StatsModification.from_bytes(cls, _bytes)


if __name__ == "__main__":
    DebuffStats(state_id=0)
