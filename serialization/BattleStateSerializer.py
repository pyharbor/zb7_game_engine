from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.ObjectParser import ObjectParser
from zb7_game_engine.runtime.core.states.BattleState import BattleState
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer


class BattleStateSerializer(BattleState):
    @classmethod
    def from_human_readable_json(cls, _json: dict):
        pass

    def to_human_readable_json(self) -> dict:
        pass

    def to_json(self):
        _json = {}
        if len(self.friendly_recruits) > 0:
            _json["a"] = []
            for recruit in self.friendly_recruits:
                _json["a"].append(recruit.to_base64())
        if len(self.friendly_relics) > 0:
            _json["b"] = []
            for relic in self.friendly_relics:
                _json["b"].append(relic.to_base64())
        if len(self.enemy_recruits) > 0:
            _json["c"] = []
            for recruit in self.enemy_recruits:
                _json["c"].append(recruit.to_base64())
        if len(self.enemy_relics) > 0:
            _json["d"] = []
            for relic in self.enemy_relics:
                _json["d"].append(relic.to_base64())
        _json["i"] = self.battle_turn
        return _json

    @staticmethod
    def from_json(_json):
        friendly_recruits = []
        friendly_relics = []
        enemy_recruits = []
        enemy_relics = []
        if "a" in _json:
            for recruit in _json["a"]:
                friendly_recruits.append(ObjectParser.from_base64_text(recruit))
        if "b" in _json:
            for relic in _json["b"]:
                friendly_relics.append(ObjectParser.from_base64_text(relic))
        if "c" in _json:
            for recruit in _json["c"]:
                enemy_recruits.append(ObjectParser.from_base64_text(recruit))
        if "d" in _json:
            for relic in _json["d"]:
                enemy_relics.append(RelicSerializer.from_base64(relic))
        battle_turn = _json["i"]
        return BattleStateSerializer(friendly_recruits=friendly_recruits,
                                     friendly_relics=friendly_relics,
                                     enemy_recruits=enemy_recruits,
                                     enemy_relics=enemy_relics,
                                     battle_turn=battle_turn)

    def copy(self):
        return BattleStateSerializer.from_json(self.to_json())


if __name__ == "__main__":
    pass
