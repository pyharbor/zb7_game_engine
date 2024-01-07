from collections import defaultdict
from pathlib import Path

from PIL import Image
import os
from pyharbor_shared_library.Disk import Disk

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
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
    objects = [x for x in Disk.Sync.rglob(
        "/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts")
              if x.is_file() and x.name != ".DS_Store" and x.suffix == ".png"]
    arts = Disk.Sync.load_file_json(filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/arts.json")
    info_by_item_id = {x['item_id']: x for x in arts}
    input_directory = "/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts"
    for i, x in enumerate(objects):
        try:
            sub_type, aaid, size = x.name.split("_")
            size = size.split(".")[0]
            item_id = sub_type + "_" + aaid
            info = info_by_item_id[item_id]
            parent_directory = x.parent.parent.name
            _type = x.parent.parent.parent.name
            if info['alias'] == "luongthetrug":
                print(item_id)
                resize(width=1024, height=1024,
                       input_filename=f"{input_directory}/{_type}/{parent_directory}/{sub_type}/{item_id}_large.png",
                       output_filename=f"{input_directory}/{_type}/{parent_directory}/{sub_type}/{item_id}_large.png")
                resize(width=350, height=350,
                       input_filename=f"{input_directory}/{_type}/{parent_directory}/{sub_type}/{item_id}_large.png",
                       output_filename=f"{input_directory}/{_type}/{parent_directory}/{sub_type}/{item_id}_medium.png")
                resize(width=200, height=200,
                       input_filename=f"{input_directory}/{_type}/{parent_directory}/{sub_type}/{item_id}_large.png",
                       output_filename=f"{input_directory}/{_type}/{parent_directory}/{sub_type}/{item_id}_small.png")
        except Exception as e:
            print(e)
