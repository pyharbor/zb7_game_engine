import json
from collections import defaultdict
from pyharbor_shared_library.Disk import Disk

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.ObjectParser import ObjectParser
from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature
from zb7_game_engine.runtime.misc.debugging.Debug import Debug
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer

if __name__ == "__main__":
    import re
    sub_types = Disk.Sync.load_file_json(filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")
    # for x in sub_types:
    #     if x["type"] == "Recruit":
    #         binomial_nomenclature = BinomialNomenclature.from_json(x["binomial_nomenclature"])
    #         main_species = binomial_nomenclature.get_main_species()
    #         x["main_species"] = main_species
    # for x in sub_types:
    #     if x["type"] == "Status":
    #         continue
    #     for info in x["ability"]:
    #         if x["type"] == "Recruit":
    #             info["matched_logical_level"] = [1]
    #         elif x["type"] == "Relic":
    #             del info["matched_logical_level"]
    for x in sub_types:
        if x["type"] == "Relic":
            if "custom_data" not in x:
                x["custom_data"] = None
    Disk.Sync.write_file_text(data=json.dumps(sub_types, indent=4), filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")


