import json

from pyharbor_shared_library.Disk import Disk

from zb7_game_engine.runtime.core.GameConstants import GameConstants


class ShopGenerator:
    @staticmethod
    def run():
        example = {
            "item_id": "Dolphin_1",
            "price_in_token": 5,
            "sub_type": "Dolphin",
            "type": "ShopAlternativeArtItem"
        }
        sub_types = Disk.Sync.load_file_json(filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")
        _json = {
            "items":
                []
        }
        for x in sub_types:
            for a in x['arts']:
                if a['item_id'].endswith("_0"):
                    pass
                else:
                    _json["items"].append(
                        {
                            "item_id": a['item_id'],
                            "price_in_token": 5,
                            "sub_type": x['sub_type_as_text'],
                            "type": "ShopAlternativeArtItem"
                        }
                    )
        Disk.Sync.write_file_text(data=json.dumps(_json, indent=4), filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/game_shop.json")


if __name__ == "__main__":
    ShopGenerator.run()