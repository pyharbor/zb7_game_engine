from pyharbor_shared_library.Disk import Disk

if __name__ == "__main__":
    sub_types = Disk.Sync.load_file_json(filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")
    for x in sub_types:
        if x['type'] == "Relic":
            for art in x['arts']:
                artist = art['alias']
                item_id = art['item_id']
                sub_type_as_text = x['sub_type_as_text']
                print(f"{artist.ljust(20)} {item_id}")
                input_path = f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/relics/{sub_type_as_text[0]}/{sub_type_as_text}/{item_id}_large.png"
                output_path = f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_alternate_arts/assets/arts/python/new/relics/static_files/{artist}/{item_id}_large.png"
                Disk.Sync.create_directories(filename=output_path)
                _bytes = Disk.Sync.load_file_bytes(filename=input_path)
                Disk.Sync.write_file_bytes(filename=output_path, data=_bytes)
    statuses_files = [x for x in Disk.Sync.rglob(directory="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/statuses") if x.is_file() and x.suffix == ".png"]
    for x in statuses_files:
        artist = "admurin"
        sub_type_as_text, aaid, *_ = x.stem.split("_")
        item_id = sub_type_as_text + "_" + aaid
        _bytes = Disk.Sync.load_file_bytes(filename=str(x))
        output_path = f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_alternate_arts/assets/arts/python/new/statuses/static_files/admurin/{item_id}_large.png"
        Disk.Sync.write_file_bytes(filename=output_path, data=_bytes)