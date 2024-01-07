from pyharbor_shared_library.Disk import Disk

from zb7_game_engine.code_templating.animation_events.AnimationEventFuncBodies import AnimationEventFuncBodies


class AnimationEventGenerator:
    def __init__(self):
        self.objects = Disk.Sync.load_file_yaml(
            filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/animation_events.json")

    def generate_modules(self):
        for x in self.objects.keys():
            sub_type = x
            module_output_path = f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/" \
                                 f"zb7_game_engine/zb7_game_engine/serialization/animation_events/{sub_type[0]}/{sub_type}.py"
            text = AnimationEventTemplate(x)
            print(text)
            compile(source=text, filename=module_output_path, mode="exec")
            if Disk.Sync.check_path_exists(filename=module_output_path):
                pass
            else:
                Disk.Sync.write_file_text(filename=module_output_path, data=text)

    def generate_animations(self):
        recruits_text = ""
        for x in self.objects.keys():
            sub_type = x
            recruits_text += f"from zb7_game_engine.serialization.animation_events.{sub_type[0]}.{sub_type} import {sub_type}\n"
        recruits_text += f"""

class Animations:

"""
        for x in self.objects.keys():
            sub_type = x
            recruits_text += f"    {sub_type} = {sub_type}\n"

        module_output_path = f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/serialization/animation_events/Animations.py"
        compile(source=recruits_text, filename=module_output_path, mode="exec")
        Disk.Sync.write_file_text(filename=module_output_path, data=recruits_text)


class AnimationEventTemplate:
    def __new__(cls, x):
        text = f"""import base64
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer


class {x}(AnimationEventSerializer):
    def __init__(self, state_id: int, shop_id: int, battle_id: int):
        super().__init__(animation_type_as_text=GameConstants.Animations.{x},
                         state_id=state_id)
        self.shop_id = shop_id
        self.battle_id = battle_id                        
                            
    def to_bytes(self) -> bytearray:
        _bytes = bytearray()
        animation_type_bytes = self.animation_type_as_int.to_bytes(1, byteorder="big")
        state_id_bytes = self.state_id.to_bytes(2, byteorder="big")
        shop_id_bytes = self.shop_id.to_bytes(1, byteorder="big")
        battle_id_bytes = self.battle_id.to_bytes(1, byteorder="big")
        _bytes.extend(animation_type_bytes)
        _bytes.extend(state_id_bytes)
        _bytes.extend(shop_id_bytes)
        _bytes.extend(battle_id_bytes)
        return _bytes

    @classmethod
    def from_bytes(cls, _bytes: bytes) -> "{x}":
        current_index = 0
        animation_type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        state_id = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 1
        shop_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        battle_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        return cls(state_id=state_id, shop_id=shop_id, battle_id=battle_id)


if __name__ == "__main__":
    {x}(state_id=0)"""
        return text


if __name__ == "__main__":
    r = AnimationEventGenerator()
    r.generate_animations()
    r.generate_modules()
