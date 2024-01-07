from pyharbor_shared_library.Disk import Disk

from zb7_game_engine.code_templating.statuses.StatusDefaultFuncs import StatusDefaultFuncs
from zb7_game_engine.code_templating.statuses.StatusFuncBodies import StatusFuncBodies
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus


class StatusGenerator:
    def __init__(self):
        objects = Disk.Sync.load_file_yaml(filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")
        statuses = [BaseStatus(**x) for x in objects if x["type"] == "Status"]
        self.statuses = statuses

    def generate_modules(self):
        for x in self.statuses:
            module_output_path = f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/" \
                                 f"zb7_game_engine/runtime/objects/statuses/{x.sub_type_as_text[0]}/{x.sub_type_as_text}.py"
            text = StatusTemplate(x)
            print(text)
            compile(source=text, filename=module_output_path, mode="exec")
            Disk.Sync.write_file_text(filename=module_output_path, data=text)

    def generate_statuses(self):
        statuses_text = ""
        for x in self.statuses:
            sub_type = x.sub_type_as_text
            statuses_text += f"from zb7_game_engine.runtime.objects.statuses.{sub_type[0]}.{sub_type} import {sub_type}\n"
        statuses_text += f"""
        
        
class Statuses:"""
        for x in self.statuses:
            sub_type = x.sub_type_as_text
            statuses_text += f"""
    {sub_type} = {sub_type}"""
        statuses_text += "\n"
        module_output_path = f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/runtime/objects/statuses/Statuses.py"
        compile(source=statuses_text, filename=module_output_path, mode="exec")
        Disk.Sync.write_file_text(filename=module_output_path, data=statuses_text)


class StatusTemplate:
    def __new__(cls, x: BaseStatus):
        func_bodies = StatusFuncBodies(
            module_path=f"zb7_game_engine.runtime.objects.statuses.{x.sub_type_as_text[0]}.{x.sub_type_as_text}",
            sub_type_as_text=x.sub_type_as_text)
        code_by_function_name = func_bodies.code_by_function_name


        text = f"""from typing import List
from zb7_game_engine.serialization.animation_events.G.Group import Group
from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature
from zb7_game_engine.runtime.core.StackItem import StackItem
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus
from zb7_game_engine.serialization.StatusSerializer import StatusSerializer
from typing import List, TYPE_CHECKING, Union
from zb7_game_engine.runtime.core.Listeners import Listeners
from zb7_game_engine.serialization.animation_events.Animations import Animations
from zb7_game_engine.runtime.core.GameConstants import GameConstants

if TYPE_CHECKING:
    from zb7_game_engine.serialization.ShopStateSerializer import ShopStateSerializer
    from zb7_game_engine.serialization.BattleStateSerializer import BattleStateSerializer
    from zb7_game_engine.runtime.core.StackItem import StackItem
    from zb7_game_engine.runtime.core.StateSet import StateSet
    from zb7_game_engine.runtime.core.shop_opcodes.ShopUserInput import ShopUserInput
    from zb7_game_engine.serialization.BattleSnapshotSerializer import BattleSnapshotSerializer
    from zb7_game_engine.serialization.ShopSnapshotSerializer import ShopSnapshotSerializer
    from zb7_game_engine.serialization.RelicSerializer import RelicSerializer
    from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
    from zb7_game_engine.serialization.StatusSerializer import StatusSerializer


class {x.sub_type_as_text}(StatusSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int={x.sub_type_as_int},
                         sub_type_as_text="{x.sub_type_as_text}", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------
{code_by_function_name.get('__init__', "")}
        
"""
        for trigger in x.triggers:
            if trigger in code_by_function_name and code_by_function_name[trigger]:
                text += StatusDefaultFuncs.code_by_func_name[trigger].function_header
                text += code_by_function_name[trigger] + "\n"

            else:
                text += StatusDefaultFuncs.code_by_func_name[trigger].function_header
                text += StatusDefaultFuncs.code_by_func_name[trigger].function_body + "\n"
        return text


if __name__ == "__main__":
    r = StatusGenerator()
    r.generate_statuses()
    r.generate_modules()
