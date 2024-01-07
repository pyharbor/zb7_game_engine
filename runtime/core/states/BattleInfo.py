from typing import List

from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer


class BattleInfo:
    def __init__(self, friendly_recruits: List[RecruitSerializer], friendly_relics: List[RelicSerializer],
                 friendly_uuid: str,
                 enemy_recruits: List[RecruitSerializer], enemy_relics: List[RelicSerializer],
                 enemy_uuid: str):
        self.friendly_recruits = friendly_recruits
        self.friendly_relics = friendly_relics
        self.friendly_uuid = friendly_uuid
        self.enemy_recruits = enemy_recruits
        self.enemy_relics = enemy_relics
        self.enemy_uuid = enemy_uuid