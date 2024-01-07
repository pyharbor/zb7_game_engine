import json

from pyharbor_shared_library.Disk import Disk

from zb7_game_engine.runtime.core.GameConstants import GameConstants


class UserSettingsGenerator:
    @staticmethod
    def run():
        example = {
            "sub_type": "AcridSlimeSkin",
            "options": [
                "0"
            ],
            "selected": "0"
        }
        user_settings = Disk.Sync.load_file_json(
            filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/game_user_settings.json")
        sub_types = Disk.Sync.load_file_json(filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")
        user_settings["object_cosmetic_info"] = []
        for x in sub_types:
            if x['sub_type_as_text'] == "EmptySlot":
                continue
            options = [a['item_id'] for a in x['arts']]
            option_zero = [x for x in options if x.endswith("_0")][0]
            user_settings["object_cosmetic_info"].append(
                {
                    "sub_type": x['sub_type_as_text'],
                    "options": options,
                    "selected": option_zero
                }
            )
        Disk.Sync.write_file_text(data=json.dumps(user_settings, indent=4), filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/game_user_settings.json")


if __name__ == "__main__":
    UserSettingsGenerator.run()