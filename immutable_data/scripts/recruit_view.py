import json
from collections import defaultdict

from pyharbor_shared_library.Disk import Disk

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.misc.debugging.Debug import Debug
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer

if __name__ == "__main__":
    import re
    sub_types = Disk.Sync.load_file_json(filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")
    # sub_types = [x for x in sub_types if x["type"] == "Recruit"]
    lines = Disk.Sync.load_file_text(filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/scripts/study_data.txt").split("\n")
    for i, line in enumerate(lines):
        lines[i] = re.sub(' +', ' ', line)

    recruit_as_objects = []
    for line in lines:
        index, sub_type_as_text, main_species, rarity, cost, stats, initiative, *habitats = line.split(" ")
        melee, ranged, armor, health, max_health = stats.split("/")
        habitats = "".join(habitats).replace("'", '"')
        habitats = json.loads(habitats)
        immutable_data = ImmutableData.Subtype.from_text(subtype_as_text=sub_type_as_text)
        _json = {
            "sub_type_as_text": sub_type_as_text,
            "sub_type_as_int": immutable_data["sub_type_as_int"],
            "main_species": main_species,
            "rarity": rarity,
            "cost": int(cost),
            "melee_attack": int(melee),
            "ranged_attack": int(ranged),
            "armor": int(armor),
            "health": int(health),
            "max_health": int(max_health),
            "initiative": float(initiative),
            "binomial_nomenclature": immutable_data["binomial_nomenclature"],
        }
        r = RecruitSerializer.from_config_json(_json)
        r.rarity = rarity
        r.cost = int(cost)
        recruit_as_objects.append(r)
    for i, x in enumerate(sub_types):
        if x["type"] != "Recruit":
            continue
        found = False
        for obj in recruit_as_objects:
            if obj.sub_type_as_text == x["sub_type_as_text"]:
                obj.index = i
                print(f"{obj.index} {obj.sub_type_as_text}")
                found = True
        if not found:
            recruit_as_objects.append(RecruitSerializer.from_config_json(x))
    sorted_by_main_species = sorted(recruit_as_objects, key=lambda x: x.main_species)
    abilities_text = []
    text = []
    for i, x in enumerate(sorted_by_main_species):
        text.append(f"{str(i).ljust(3)} {Debug.RecruitSerializer.study_info(x)}")
        abilities_text.append(f"{str(i).ljust(3)} {Debug.RecruitSerializer.study_info_abilities(x)}")
        print(f"{str(i).ljust(3)} {Debug.RecruitSerializer.study_info(x)}")
    Disk.Sync.write_file_text(data="\n".join(text), filename=f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/scripts/study_data.txt")
    Disk.Sync.write_file_text(data="\n".join(abilities_text),
                              filename=f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/scripts/study_data_abilites.txt")
    # habitats_counter = defaultdict(int)
    # for x in recruit_as_objects:
    #     for habitat in x.habitats:
    #         habitats_counter[habitat] += 1
    # main_species_counter = defaultdict(int)
    # for x in recruit_as_objects:
    #     main_species_counter[x.main_species] += 1

    # for habitat, count in habitats_counter.items():
    #     print(f"{habitat.ljust(20)} {count}")
    # print(f"{'main_species'.ljust(20)} {'count'}")
    # for main_species, count in main_species_counter.items():
    #     print(f"{main_species.ljust(20)} {count}")
    # for x in sub_types:
    #     for j in recruit_as_objects:
    #         if x["sub_type_as_text"] == j.sub_type_as_text:
    #             x["cost"] = j.cost
    #             x["melee_attack"] = j.melee_attack
    #             x["ranged_attack"] = j.ranged_attack
    #             x["armor"] = j.armor
    #             x["health"] = j.health
    #             x["max_health"] = j.max_health
    #             x["initiative"] = j.initiative
    #             x["rarity"] = j.rarity
    # Disk.Sync.write_file_text(data=json.dumps(sub_types, indent=4), filename=f"/zb7_game_engine/immutable_data/configs/sub_types.json")
    #
    # rarity_counter = defaultdict(int)
    # for x in recruit_as_objects:
    #     rarity_counter[x.rarity] += 1
    # for rarity, count in rarity_counter.items():
    #     print(f"{rarity.ljust(20)} {count}")