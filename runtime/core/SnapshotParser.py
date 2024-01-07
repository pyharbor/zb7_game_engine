import base64

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.serialization.BattleSnapshotSerializer import BattleSnapshotSerializer
from zb7_game_engine.serialization.ShopSnapshotSerializer import ShopSnapshotSerializer


class SnapshotParser:
    @staticmethod
    def snapshot_from_json(json_dict):
        snapshot_base64_text = json_dict["i"]
        current_index = 0
        _bytes = base64.b64decode(snapshot_base64_text)
        snapshot_type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        snapshot_type_as_text = ImmutableData.Misc.from_int(snapshot_type_as_int)
        if snapshot_type_as_text == "BattleSnapshot":
            return BattleSnapshotSerializer.from_json(json_dict)
        elif snapshot_type_as_text == "ShopSnapshot":
            return ShopSnapshotSerializer.from_json(json_dict)