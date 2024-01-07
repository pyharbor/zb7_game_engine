from pyharbor_shared_library.Disk import Disk

from zb7_game_engine.code_templating.relics.RelicDefaultFuncs import RelicDefaultFuncs
from zb7_game_engine.code_templating.relics.RelicFuncBodies import RelicFuncBodies
from zb7_game_engine.runtime.objects.base.BaseRelic import BaseRelic


class RelicGenerator:
    def __init__(self):
        objects = Disk.Sync.load_file_yaml(filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")
        relics = [BaseRelic(**x) for x in objects if x["type"] == "Relic"]
        self.relics = relics

    def generate_modules(self):
        for x in self.relics:
            module_output_path = f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/" \
                                 f"zb7_game_engine/runtime/objects/relics/{x.sub_type_as_text[0]}/{x.sub_type_as_text}.py"
            text = RelicTemplate(x)
            print(text)
            compile(source=text, filename=module_output_path, mode="exec")
            Disk.Sync.write_file_text(filename=module_output_path, data=text)

    def generate_relics(self):
        relics_text = ""
        for x in self.relics:
            sub_type = x.sub_type_as_text
            relics_text += f"from zb7_game_engine.runtime.objects.relics.{sub_type[0]}.{sub_type} import {sub_type}\n"
        relics_text += f"""
        
        
class Relics:"""
        for x in self.relics:
            sub_type = x.sub_type_as_text
            relics_text += f"""
    {sub_type} = {sub_type}"""
        relics_text += "\n"
        module_output_path = f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/runtime/objects/relics/Relics.py"
        compile(source=relics_text, filename=module_output_path, mode="exec")
        Disk.Sync.write_file_text(filename=module_output_path, data=relics_text)


class RelicTemplate:
    def __new__(cls, x: BaseRelic):
        func_bodies = RelicFuncBodies(
            module_path=f"zb7_game_engine.runtime.objects.relics.{x.sub_type_as_text[0]}.{x.sub_type_as_text}",
            sub_type_as_text=x.sub_type_as_text)
        code_by_function_name = func_bodies.code_by_function_name


        text = f"""from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from collections import defaultdict
from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature
from zb7_game_engine.runtime.objects.base.BaseRecruit import BaseRecruit
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus
from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.StateSet import StateSet
from typing import List, TYPE_CHECKING, Union
from zb7_game_engine.runtime.core.StackItem import StackItem
from zb7_game_engine.serialization.animation_events.Animations import Animations
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer
from zb7_game_engine.runtime.core.Listeners import Listeners
from zb7_game_engine.serialization.animation_events.Animations import Animations
from zb7_game_engine.runtime.core.RandomEngine import random_engine
from zb7_game_engine.serialization.animation_events.G.Group import Group
from zb7_game_engine.runtime.objects.statuses.Statuses import Statuses
from zb7_game_engine.serialization.shared.custom_data.ShopIDTarget import ShopIDTarget
from zb7_game_engine.runtime.core.ObjectParser import ObjectParser
from zb7_game_engine.serialization.shared.custom_data.SuperNestCD import SuperNestCD
from zb7_game_engine.serialization.shared.custom_data.Rewards import Rewards


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


class {x.sub_type_as_text}(RelicSerializer):
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
                text += RelicDefaultFuncs.code_by_func_name[trigger].function_header
                text += code_by_function_name[trigger] + "\n"

            else:
                text += RelicDefaultFuncs.code_by_func_name[trigger].function_header
                text += RelicDefaultFuncs.code_by_func_name[trigger].function_body + "\n"
        return text


if __name__ == "__main__":
    r = RelicGenerator()
    r.generate_relics()
    r.generate_modules()
