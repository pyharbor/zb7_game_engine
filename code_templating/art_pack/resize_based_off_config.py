import json
from pathlib import Path

from PIL import Image
from pyharbor_shared_library.Disk import Disk

from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature


class Info:
    def __init__(self, path, alias, item_id, social_info, scale, y_offset, flip_h, large_size, medium_size, small_size,
                 local_path):
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


class Resizer:
    @staticmethod
    def resize(width: int, height: int, input_filename: str, output_filename: str):
        # Loop through each image in the directory and resize it
        with Image.open(input_filename) as im:
            if (width, height) != im.size:
                im.thumbnail(size=(width, height))
                im.save(output_filename)

    @staticmethod
    def run():
        sub_types = Disk.Sync.load_file_json(
            filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")
        arts = Disk.Sync.load_file_json(
            filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/arts.json")
        arts = [Info(**x) for x in arts]
        for x in arts:
            if "statuses" in str(x.local_path):
                continue
            try:
                local_path = Path(x.local_path)
                Resizer.resize(width=x.large_size, height=x.large_size,
                               input_filename=f"{local_path.parent}/{x.item_id}_large.png",
                               output_filename=f"{local_path.parent}/{x.item_id}_large.png")
                print(f"{local_path.parent}/{x.item_id}_large.png")
                Resizer.resize(width=x.medium_size, height=x.medium_size,
                               input_filename=f"{local_path.parent}/{x.item_id}_large.png",
                               output_filename=f"{local_path.parent}/{x.item_id}_medium.png")
                print(f"{local_path.parent}/{x.item_id}_medium.png")
                Resizer.resize(width=x.small_size, height=x.small_size,
                               input_filename=f"{local_path.parent}/{x.item_id}_large.png",
                               output_filename=f"{local_path.parent}/{x.item_id}_small.png")
                print(f"{local_path.parent}/{x.item_id}_small.png")
            except FileNotFoundError:
                print(f"File not found: {x.item_id}")
                continue


if __name__ == "__main__":
    Resizer.run()
