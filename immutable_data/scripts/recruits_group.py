import json
from collections import defaultdict
from pyharbor_shared_library.Disk import Disk

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.ObjectParser import ObjectParser
from zb7_game_engine.runtime.misc.debugging.Debug import Debug
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer

if __name__ == "__main__":
    import re
    sub_types = Disk.Sync.load_file_json(filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")
    recruits: list[RecruitSerializer] = [RecruitSerializer.from_config_json(x) for x in sub_types if x["type"] == "Recruit"]
    grouping_dict: dict[str, list[RecruitSerializer]] = defaultdict(list)
    habitat_groups = [
        (GameConstants.Habitats.Arid, "Arid"),
        (GameConstants.Habitats.TemperateForest, "Temperate Forest"),
        (GameConstants.Habitats.TropicalForests, "Tropical Forest"),
        (GameConstants.Habitats.Arctic, "Arctic"),
        (GameConstants.Habitats.Meadow, "Meadow"),
        (GameConstants.Habitats.DeepSea, "Deep Sea"),
        (GameConstants.Habitats.OpenOcean, "OpenOcean"),
        (GameConstants.Habitats.Freshwater, "FreshWater"),
        (GameConstants.Habitats.Swampy, "Swampy"),
        (GameConstants.Habitats.GrasslandLike, "GrasslandLike"),
        (GameConstants.Habitats.Oceanic, "Oceanic"),
        (GameConstants.Habitats.Coastal, "Coastal"),
        ([GameConstants.Habitats.Beach], "Beach"),
    ]

    for recruit in recruits:
        habitats = recruit.habitats
        for x in habitats:
            for y in habitat_groups:
                if x in y[0]:
                    if recruit not in grouping_dict[y[1]]:
                        grouping_dict[y[1]].append(recruit)

    for recruit in recruits:
        grouping_dict[recruit.main_species].append(recruit)

    for k, v in grouping_dict.items():
        print(f"{k} {len(v)}")
        for x in v:
            print(f"    {x.sub_type_as_text}")


