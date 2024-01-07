import json

from pyharbor_shared_library.Disk import Disk


class Info:
    def __init__(self, animation_type_as_int, animation_type_as_text, custom_data):
        self.animation_type_as_int = animation_type_as_int
        self.animation_type_as_text = animation_type_as_text
        self.custom_data = custom_data


if __name__ == "__main__":
    _json = Disk.Sync.load_file_json(filename="animation_events.json")
    for i, (k, v) in enumerate(_json.items()):
        _json[k] = Info(animation_type_as_int=i, animation_type_as_text=k, custom_data=None).__dict__
    Disk.Sync.write_file_text(data=json.dumps(_json, indent=4), filename="animation_events.json")
    text = ["class Animations:"]
    for k, v in _json.items():
        text.append(f'    {k} = "{k}"')
    print("\n".join(text))