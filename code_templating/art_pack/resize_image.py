import json
from pathlib import Path
import subprocess
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
                im = im.resize(size=(width, height), resample=Image.NEAREST)
                im.save(output_filename)


if __name__ == "__main__":
    video_file = Path(
        "/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/animated_recruits/PaperWasp_3_large.mov")
    sub_type, aaid, size = video_file.stem.split("_")
    Disk.Sync.create_directories(filename=f"{sub_type}_{aaid}/{sub_type}_{aaid}_large/1.png")
    Disk.Sync.create_directories(filename=f"{sub_type}_{aaid}/{sub_type}_{aaid}_medium/1.png")
    Disk.Sync.create_directories(filename=f"{sub_type}_{aaid}/{sub_type}_{aaid}_small/2.png")
    command = f"""ffmpeg -i "{video_file}" -vf fps=24 {sub_type}_{aaid}/{sub_type}_{aaid}_{size}/{sub_type}_{aaid}_{size}_%04d.png"""
    subprocess.check_output(command, shell=True)
    files = [x for x in Disk.Sync.rglob(
        directory=f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/code_templating/art_pack/"
                  f"{sub_type}_{aaid}/{sub_type}_{aaid}_large")
             if x.is_file()]
    for x in files:
        for size_name, size_int in zip(["medium", "small"], [350, 156]):
            Resizer.resize(width=size_int, height=size_int,
                           input_filename=str(x),
                           output_filename=f"{sub_type}_{aaid}/{sub_type}_{aaid}_{size_name}/{x.name}.png")
