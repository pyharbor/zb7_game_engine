from collections import defaultdict
from pathlib import Path

from PIL import Image
import os
from pyharbor_shared_library.Disk import Disk

from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature


class Info:
    def __init__(self, sub_type: str, aaid: str, main_species: str, path: Path, sizes: list[str] = None):
        self.sub_type = sub_type
        self.aaid = aaid
        if sizes is None:
            sizes = []
        self.sizes = sizes
        self.main_species = main_species
        self.item_id = sub_type + "_" + aaid
        self.path: Path = path


def resize(width: int, height: int, input_filename: str, output_filename: str):
    # Loop through each image in the directory and resize it
    with Image.open(input_filename) as im:
        im.thumbnail(size=(width, height))
        im.save(output_filename)


if __name__ == "__main__":
    files = [x for x in Disk.Sync.rglob(
        directory="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/recruits")
             if x.is_file() and x.name != ".DS_Store"]
    sub_types = Disk.Sync.load_file_json(
        filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")
    file_set: dict[str, Info] = defaultdict(Info)

    for f in files:
        sub_type, aaid, size = f.name.split("_")
        size = size.split(".")[0]
        item_id = sub_type + "_" + aaid

        for x in sub_types:
            if x['sub_type_as_text'] == sub_type:
                b = BinomialNomenclature.from_json(x['binomial_nomenclature'])
                main_species = b.get_main_species()
                obj = Info(sub_type=sub_type, aaid=aaid, main_species=main_species, path=f)
                if item_id not in file_set:
                    file_set[item_id] = obj
                break
        file_set[item_id].sizes.append(size)
    missing_arts: list[Info] = []
    required_sizes = ["small", "medium", "large"]
    for i, (item_id, obj) in enumerate(file_set.items()):
        # print(f"{str(i).ljust(3)} {item_id.ljust(30)} {sizes}")
        missing_arts.append(obj)
        # for s in required_sizes:
        #     if s not in obj.sizes:
        #         missing_arts.append(obj)

    missing_arts = sorted(missing_arts, key=lambda x: x.main_species + x.item_id)
    input_directory = "/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/recruits"
    output_directory = "/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/recruits"
    for i, x in enumerate(missing_arts):
        for s in required_sizes:
            if s not in x.sizes:
                print(f"{str(i).ljust(3)} {x.item_id.ljust(40)} {x.main_species.ljust(20)} {x.sizes}")
                break
        print(f"{str(i).ljust(3)} {x.item_id.ljust(40)} {x.main_species.ljust(20)} {x.sizes}")

        resize(width=1024, height=1024, input_filename=f"{input_directory}/{x.main_species}/{x.sub_type}/{x.item_id}_large.png",
               output_filename=f"{output_directory}/{x.main_species}/{x.sub_type}/{x.item_id}_large.png")
        resize(width=256, height=256, input_filename=f"{input_directory}/{x.main_species}/{x.sub_type}/{x.item_id}_large.png",
               output_filename=f"{output_directory}/{x.main_species}/{x.sub_type}/{x.item_id}_medium.png")
        resize(width=128, height=128, input_filename=f"{input_directory}/{x.main_species}/{x.sub_type}/{x.item_id}_large.png",
               output_filename=f"{output_directory}/{x.main_species}/{x.sub_type}/{x.item_id}_small.png")

    input_directory = "/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/relics"
    output_directory = "/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/relics"
    relics = [x for x in Disk.Sync.rglob("/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/relics") if x.is_file() and x.name != ".DS_Store"]

    for i, x in enumerate(relics):
        sub_type, aaid, size = x.name.split("_")
        size = size.split(".")[0]
        item_id = sub_type + "_" + aaid
        resize(width=1024, height=1024,
               input_filename=f"{input_directory}/{sub_type[0]}/{sub_type}/{item_id}_large.png",
               output_filename=f"{output_directory}/{sub_type[0]}/{sub_type}/{item_id}_large.png")
        resize(width=256, height=256,
               input_filename=f"{input_directory}/{sub_type[0]}/{sub_type}/{item_id}_large.png",
               output_filename=f"{output_directory}/{sub_type[0]}/{sub_type}/{item_id}_medium.png")
        resize(width=128, height=128,
               input_filename=f"{input_directory}/{sub_type[0]}/{sub_type}/{item_id}_large.png",
               output_filename=f"{output_directory}/{sub_type[0]}/{sub_type}/{item_id}_small.png")
