import json
from collections import defaultdict

from pyharbor_shared_library.Disk import Disk

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.misc.debugging.Debug import Debug
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer
from zb7_game_engine.serialization.StatusSerializer import StatusSerializer

if __name__ == "__main__":
    import re
    sub_types = Disk.Sync.load_file_json(filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")
    # sub_types = [x for x in sub_types if x["type"] == "Recruit"]
    statuses_as_objects = []
    for i, x in enumerate(sub_types):
        if x["type"] != "Status":
            continue
        statuses_as_objects.append(StatusSerializer.from_config_json(x))
    abilities_text = []
    for i, x in enumerate(statuses_as_objects):
        abilities_text.append(f"{str(i).ljust(3)} {Debug.StatusSerializer.study_info_abilities(x)}")
    Disk.Sync.write_file_text(data="\n".join(abilities_text),
                              filename=f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/scripts/study_statuses_abilites.txt")
    # Disk.Sync.write_file_text(data=json.dumps(sub_types, indent=2), filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")