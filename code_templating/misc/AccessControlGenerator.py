import json

from pyharbor_shared_library.Disk import Disk

from zb7_game_engine.runtime.core.GameConstants import GameConstants


class AccessControlGenerator:
    @staticmethod
    def run():
        example = {"AcridSlimeSkin_0": "unlocked"}

        sub_types = Disk.Sync.load_file_json(filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")
        _json = {
            "items":
                {}
        }
        for x in sub_types:
            for a in x['arts']:
                if a['item_id'].endswith("_0"):
                    _json["items"][a['item_id']] = "unlocked"
                else:
                    _json["items"][a['item_id']] = "locked"
                    # _json["items"][a['item_id']] = "unlocked"
        Disk.Sync.write_file_text(data=json.dumps(_json, indent=4), filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/game_access_control.json")


if __name__ == "__main__":
    AccessControlGenerator.run()