import base64
from typing import List, Union

from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.PlayerDecisionInfoSerializer import PlayerDecisionInfoSerializer
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer


class TreasureChestPDInfo(PlayerDecisionInfoSerializer):
    def __init__(self, shop_id: int, items: List[Union[RecruitSerializer, RelicSerializer]] = None):
        super().__init__(info_type_as_text=GameConstants.PDInfoType.TreasureChest,
                         shop_id=shop_id)
        self.items: List[RecruitSerializer, RelicSerializer] = items or []
                            
    def to_bytes(self) -> bytearray:
        _bytes = bytearray()
        info_type_bytes = self.info_type_as_int.to_bytes(1, byteorder="big")
        shop_id_bytes = self.shop_id.to_bytes(1, byteorder="big")
        items_bytes = bytearray()
        for item in self.items:
            item_bytes = item.to_bytes_minimal()
            items_bytes.extend(item_bytes)
        items_len_bytes = len(items_bytes).to_bytes(1, byteorder="big")
        _bytes.extend(info_type_bytes)
        _bytes.extend(shop_id_bytes)
        _bytes.extend(items_len_bytes)
        _bytes.extend(items_bytes)
        return _bytes

    @classmethod
    def from_bytes(cls, _bytes: bytes) -> "TreasureChestPDInfo":
        current_index = 0
        info_type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        shop_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        items_len = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        items = []
        for i in range(items_len):
            item = RecruitSerializer.from_bytes_minimal(_bytes[current_index:])
            items.append(item)
            current_index += 4
        return cls(shop_id=shop_id, items=items)


if __name__ == "__main__":
    TreasureChestPDInfo(shop_id=0)