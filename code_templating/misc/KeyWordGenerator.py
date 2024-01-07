import json

from pyharbor_shared_library.Disk import Disk

from zb7_game_engine.runtime.core.GameConstants import GameConstants


class KeyWordGenerator:
    @staticmethod
    def run():
        key_words = Disk.Sync.load_file_json(filename="/zb7_game_engine/immutable_data/configs/key_words.json")
        sub_types = Disk.Sync.load_file_json(filename="/zb7_game_engine/immutable_data/configs/sub_types.json")
        opcodes = [x for x in GameConstants.Opcodes.Stack.__dict__.keys() if not x.startswith("__")]
        # opcodes_ui = [x.replace("_", " ") for x in opcodes]
        habitats = [x for x in GameConstants.Habitats.__dict__.keys() if not x.startswith("__")]
        scientific_names = [x for x in GameConstants.ScientificNames.__dict__.keys() if not x.startswith("__")]
        sub_types = [x["sub_type_as_text"] for x in sub_types]
        # key_words["opcodes_code"] = opcodes
        key_words["habitats"] = habitats
        key_words["scientific_names"] = scientific_names
        key_words["sub_types"] = sub_types
        Disk.Sync.write_file_text(data=json.dumps(key_words, indent=4), filename="/zb7_game_engine/immutable_data/configs/key_words.json")


if __name__ == "__main__":
    KeyWordGenerator.run()