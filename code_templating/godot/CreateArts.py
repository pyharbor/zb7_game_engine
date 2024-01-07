import json

from pyharbor_shared_library.Disk import Disk

from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature


class Info:
    def __init__(self, path, alias, item_id, social_info, scale, y_offset, flip_h, large_size, medium_size, small_size, local_path):
        self.path = path
        self.alias = alias
        self.item_id = item_id
        self.social_info = social_info
        self.scale = scale
        self.y_offset = y_offset
        self.flip_h = flip_h
        self.large_size = large_size
        self.medium_size = medium_size
        self.small_size = small_size
        self.local_path = local_path


class CreateArts:
    @staticmethod
    def create():
        sub_types = Disk.Sync.load_file_json(filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")
        arts = Disk.Sync.load_file_json(filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/arts.json")
        # for x in arts:
        #     if "large_size" not in x:
        #         x["large_size"] = 1024
        #     if "medium_size" not in x:
        #         x["medium_size"] = 256
        #     if "small_size" not in x:
        #         x["small_size"] = 128
        arts = [x for x in arts if "/statuses/" not in x["path"]]
        new_items = []
        existing_items = [x["item_id"] for x in arts]
        for x in sub_types:
            for a in x["arts"]:
                if x['type'] == "Recruit":
                    binomial_nomenclature = BinomialNomenclature.from_json(x["binomial_nomenclature"])
                    main_species = binomial_nomenclature.get_main_species()
                    sub_type_as_text = x["sub_type_as_text"]
                    item_id = a["item_id"]
                    if item_id in existing_items:
                        continue
                    path = f"res://assets/arts/recruits/{main_species}/{sub_type_as_text}/{item_id}"
                    i = Info(
                        path=path,
                        alias=a["alias"],
                        item_id=a["item_id"],
                        social_info=a["social_info"],
                        scale=1.0,
                        y_offset=0.0,
                        flip_h=False,
                        large_size=1024,
                        medium_size=256,
                        small_size=128,
                        local_path=f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/recruits/{main_species}/{sub_type_as_text}/{item_id}_large.png"
                    )
                    new_items.append(i.__dict__)
                elif x['type'] == "Relic":
                    sub_type_as_text = x["sub_type_as_text"]
                    item_id = a["item_id"]
                    if item_id in existing_items:
                        continue
                    path = f"res://assets/arts/relics/{sub_type_as_text[0]}/{sub_type_as_text}/{item_id}"
                    i = Info(
                        path=path,
                        alias=a["alias"],
                        item_id=a["item_id"],
                        social_info=a["social_info"],
                        scale=1.0,
                        y_offset=0.0,
                        flip_h=False,
                        large_size=1024,
                        medium_size=256,
                        small_size=128,
                        local_path=f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/relics/{sub_type_as_text[0]}/{sub_type_as_text}/{item_id}_large.png"
                    )
                    new_items.append(i.__dict__)
                elif x['type'] == "Status":
                    sub_type_as_text = x["sub_type_as_text"]
                    item_id = a["item_id"]
                    # if item_id in existing_items:
                    #     continue
                    path = f"res://assets/arts/statuses/{sub_type_as_text[0]}/{sub_type_as_text}/{item_id}_small.png"
                    i = Info(
                        path=path,
                        alias=a["alias"],
                        item_id=a["item_id"],
                        social_info=a["social_info"],
                        scale=1.0,
                        y_offset=0.0,
                        flip_h=False,
                        large_size=1024,
                        medium_size=256,
                        small_size=128,
                        local_path=f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/statuses/{sub_type_as_text[0]}/{sub_type_as_text}/{item_id}_small.png"
                    )
                    new_items.append(i.__dict__)

        arts.extend(new_items)
        arts.sort(key=lambda x: x["item_id"])
        Disk.Sync.write_file_text(filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/arts.json",
                                  data=json.dumps(arts, indent=4))



if __name__ == "__main__":
    CreateArts.create()