import json
from collections import defaultdict

from pyharbor_shared_library.Disk import Disk
import re

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.objects.statuses.Statuses import Statuses


if __name__ == "__main__":
    sub_types = Disk.Sync.load_file_json(filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")
    key_words = defaultdict(int)
    single_quote_regex = re.compile(r"(?<!\w)'(?!')(.*?)(?<!')'(?!')")
    for x in sub_types:
        if x["type"] == "Recruit":
            matches = re.findall(pattern=single_quote_regex, string=x['ability'][0]['description'])
            if len(matches) > 0:
                for match in matches:
                    if match == "start of battle":
                        pass
                    key_words[match] += 1

    for k,v in key_words.items():
        print(f"{k}: {v}")

    _json: dict[str, dict] = {}
    for k, v in key_words.items():
        key_word_data = {}
        if k in GameConstants.ScientificNames.__dict__:
            key_word_data["type"] = "scientific_name"
            key_word_data["value"] = GameConstants.ScientificNames.__dict__[k]
        elif k in GameConstants.Habitats.__dict__:
            if isinstance(GameConstants.Habitats.__dict__[k], list):
                key_word_data["type"] = "habitat-multi"
                key_word_data["value"] = GameConstants.Habitats.__dict__[k]
            elif isinstance(GameConstants.Habitats.__dict__[k], str):
                key_word_data["type"] = "habitat"
                key_word_data["value"] = GameConstants.Habitats.__dict__[k]
        elif k in ImmutableData._subtype_text_to_int:
            immutable_data = ImmutableData.Subtype.from_text(k)
            key_word_data["type"] = immutable_data["type"]
            key_word_data["value"] = k
        else:
            key_word_data["type"] = "op"
            key_word_data["value"] = k
        _json[k] = key_word_data

    for k, v in GameConstants.Habitats.__dict__.items():
        if isinstance(v, list):
            _json[k] = {
                "type": "habitat-multi",
                "value": v
            }
        elif isinstance(v, str):
            _json[k] = {
                "type": "habitat",
                "value": v
            }

    for k, v in GameConstants.ScientificNames.__dict__.items():
        _json[k] = {
            "type": "scientific_name",
            "value": k
        }

    key_word_color_map = {
        "op": "light_yellow",
        "habitat": "GOLD",
        "habitat-multi": "GOLD",
        "scientific_name": "DEEP_SKY_BLUE",
        "Recruit": "coral",
        "Relic": "coral",
        "Status": "coral",
    }

    godot_bbcode = ""
    visited_types = {}
    for k, v in _json.items():
        color = key_word_color_map[v["type"]]
        if v["type"] not in visited_types:
            visited_types[v["type"]] = True
            godot_bbcode += f"[url={k}][color={color}]'{k}'[/color][/url]\n"
    print(godot_bbcode)

    Disk.Sync.write_file_text(data=json.dumps(_json, indent=4), filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/key_words.json")


