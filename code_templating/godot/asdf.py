from pyharbor_shared_library.Disk import Disk

if __name__ == "__main__":
    animations = Disk.Sync.load_file_json(
        filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/animation_events.json")
    sub_types = Disk.Sync.load_file_json("/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")
    unique_custom_data = []
    for i, x in enumerate(sub_types):
        if "custom_data" in x:
            unique_custom_data.append((x["custom_data"], "custom_data"))

    for k, v in animations.items():
        if "custom_data" in v:
            unique_custom_data.append((v["custom_data"], "animation_event"))

    unique_custom_data = [x for x in unique_custom_data if x[0] is not None]
    unique_custom_data = set(unique_custom_data)
    unique_custom_data = list(unique_custom_data)
    unique_custom_data.sort(key=lambda x: x[1] + x[0])

    for i, (name, type) in enumerate(unique_custom_data):
        print(f"{str(i).ljust(3)} {str(type).ljust(15)} {str(name)}")

    t = []
    for i, (name, type) in enumerate(unique_custom_data):
        t.append(f"class_name {name}")

    print("\n".join(t))

