import json

from pyharbor_shared_library.Disk import Disk

if __name__ == "__main__":
    arts = Disk.Sync.load_file_json(
        filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/arts.json")
    for i, x in enumerate(arts):
        print(x)
        if "dealustre" == x["alias"]:
            x["scale"] = 1.0
            print(x)

    Disk.Sync.write_file_text(data=json.dumps(arts, indent=4), filename=f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/arts.json")