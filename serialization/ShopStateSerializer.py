import base64

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.ObjectParser import ObjectParser
from zb7_game_engine.runtime.core.states.ShopState import ShopState
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer


class ShopStateSerializer(ShopState):
    @classmethod
    def from_human_readable_json(cls, _json: dict):
        pass

    def to_human_readable_json(self) -> dict:
        pass

    def convert_state_data_to_bytes(self):
        _bytes = bytearray()
        wins_bytes = self.wins.to_bytes(1, byteorder='big', signed=True)
        health_bytes = self.health.to_bytes(1, byteorder='big', signed=True)
        money_bytes = self.money.to_bytes(2, byteorder='big', signed=True)
        turn_bytes = self.turn.to_bytes(1, byteorder='big', signed=True)
        operation_count_bytes = self.operation_count.to_bytes(2, byteorder='big', signed=True)
        _bytes.extend(wins_bytes)
        _bytes.extend(health_bytes)
        _bytes.extend(money_bytes)
        _bytes.extend(turn_bytes)
        _bytes.extend(operation_count_bytes)
        return _bytes

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

        if len(self.shop) > 0:
            _json["c"] = []
            for shop_item in self.shop:
                _json["c"].append(shop_item.to_base64_minimal())
        _json["d"] = base64.b64encode(self.convert_state_data_to_bytes()).decode("utf-8")
        return _json

    @staticmethod
    def from_json(_json):
        friendly_recruits = []
        friendly_relics = []
        shop = []
        if "a" in _json:
            for recruit in _json["a"]:
                friendly_recruits.append(ObjectParser.from_base64_text(recruit))
        if "b" in _json:
            for relic in _json["b"]:
                friendly_relics.append(ObjectParser.from_base64_text(relic))
        if "c" in _json:
            for shop_item in _json["c"]:
                shop.append(ObjectParser.from_base64_text_minimal(base64_str=shop_item))
        state_data_bytes = base64.b64decode(_json["d"])
        wins = int.from_bytes(state_data_bytes[0:1], byteorder='big', signed=True)
        health = int.from_bytes(state_data_bytes[1:2], byteorder='big', signed=True)
        money = int.from_bytes(state_data_bytes[2:4], byteorder='big', signed=True)
        turn = int.from_bytes(state_data_bytes[4:5], byteorder='big', signed=True)
        operation_count = int.from_bytes(state_data_bytes[5:7], byteorder='big', signed=True)
        return ShopStateSerializer(wins=wins, health=health, money=money, turn=turn,
                                   friendly_recruits=friendly_recruits,
                                   operation_count=operation_count,
                                   friendly_relics=friendly_relics, shop=shop)


if __name__ == "__main__":
    pass
