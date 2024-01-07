from pyharbor_shared_library.Disk import Disk

from zb7_game_engine.code_templating.recruits.RecruitDefaultFuncs import RecruitDefaultFuncs
from zb7_game_engine.code_templating.recruits.RecruitFuncBodies import RecruitFuncBodies
from zb7_game_engine.runtime.objects.base.BaseRecruit import BaseRecruit


class RecruitGenerator:
    def __init__(self):
        objects = Disk.Sync.load_file_yaml(filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")
        recruits = [BaseRecruit(**x) for x in objects if x["type"] == "Recruit" or x["type"] == "EmptySlot"]
        self.recruits = recruits

    def generate_modules(self):
        for x in self.recruits:
            module_output_path = f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/" \
                                 f"zb7_game_engine/runtime/objects/recruits/{x.main_species}/{x.sub_type_as_text}.py"
            text = RecruitTemplate(x)
            print(text)
            compile(source=text, filename=module_output_path, mode="exec")
            Disk.Sync.write_file_text(filename=module_output_path, data=text)

    def generate_recruits(self):
        recruits_text = ""
        for x in self.recruits:
            sub_type = x.sub_type_as_text
            species = x.main_species
            recruits_text += f"from zb7_game_engine.runtime.objects.recruits.{species}.{sub_type} import {sub_type}\n"
        text_by_species = {}
        recruits_text += f"""
                
class Recruits:

"""
        for x in self.recruits:
            if x.main_species not in text_by_species:
                text_by_species[x.main_species] = f"""    class {x.main_species}:"""
            sub_type = x.sub_type_as_text
            text_by_species[x.main_species] += f"""
        {sub_type} = {sub_type}"""
        recruits_text += "\n\n".join(text_by_species.values())
        recruits_text += "\n"
        module_output_path = f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/runtime/objects/recruits/Recruits.py"
        compile(source=recruits_text, filename=module_output_path, mode="exec")
        Disk.Sync.write_file_text(filename=module_output_path, data=recruits_text)


class RecruitTemplate:
    def __new__(cls, x: BaseRecruit):
        func_bodies = RecruitFuncBodies(
            module_path=f"zb7_game_engine.runtime.objects.recruits.{x.main_species}.{x.sub_type_as_text}",
            sub_type_as_text=x.sub_type_as_text)
        code_by_function_name = func_bodies.code_by_function_name


        text = f"""from typing import List

from collections import deque        
from zb7_game_engine.runtime.objects.statuses.Statuses import Statuses
from zb7_game_engine.serialization.animation_events.G.Group import Group
from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature
from zb7_game_engine.runtime.objects.base.BaseRecruit import BaseRecruit
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.StateSet import StateSet
from typing import List, TYPE_CHECKING, Union
from zb7_game_engine.runtime.core.StackItem import StackItem
from zb7_game_engine.serialization.animation_events.Animations import Animations
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.Listeners import Listeners
from zb7_game_engine.runtime.core.RandomEngine import random_engine
from zb7_game_engine.serialization.EmptySlotSerializer import EmptySlotSerializer
from zb7_game_engine.serialization.shared.custom_data.ShopIDTarget import ShopIDTarget
from zb7_game_engine.serialization.shared.custom_data.Uint8ArrayOfScientificNomenclature import Uint8ArrayOfScientificNomenclature
from zb7_game_engine.serialization.shared.custom_data.Uint8Counter import Uint8Counter
from zb7_game_engine.serialization.shared.custom_data.Uint16Counter import Uint16Counter
from zb7_game_engine.runtime.objects.relics.Relics import Relics
from zb7_game_engine.serialization.shared.custom_data.CarpenterAntCD import CarpenterAntCD
from zb7_game_engine.serialization.shared.custom_data.SeaOtterCD import SeaOtterCD


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


class {x.sub_type_as_text}(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int={x.sub_type_as_int},
                         sub_type_as_text="{x.sub_type_as_text}", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------
{code_by_function_name.get('__init__', "")}
        
"""
        for trigger in x.template_triggers:
            if trigger in code_by_function_name and code_by_function_name[trigger]:
                text += RecruitDefaultFuncs.code_by_func_name[trigger].function_header
                text += code_by_function_name[trigger] + "\n"

            else:
                text += RecruitDefaultFuncs.code_by_func_name[trigger].function_header
                text += RecruitDefaultFuncs.code_by_func_name[trigger].function_body + "\n"
        return text


#         text = f"""from typing import List, TYPE_CHECKING, Union
# import uuid
# from zoo_game_engine.game_engine.objects.hooks.Hooks import Hooks
# from zoo_game_engine.game_engine.objects.Ability import Ability
# from zoo_game_engine.game_engine.objects.AnimationList import AnimationList
# from zoo_game_engine.game_engine.objects.AnimationEvent import AnimationEvent
# from zoo_game_engine.game_engine.objects.BaseRecruit import BaseRecruit
# from zoo_game_engine.game_engine.objects.StackItem import StackItem
# from uuid import uuid4
# from zoo_game_engine.game_engine.objects.Glossary import Glossary
# from zoo_game_engine.game_engine.objects.BaseStatus import BaseStatus
# from zoo_game_engine.game_engine.objects.EmptySlot import EmptySlot
# from zoo_game_engine.game_engine.objects.GameConstants import GameConstants
# from zoo_game_engine.game_engine.objects.RandomEngine import random_engine
# from zoo_game_engine.game_engine.objects.statuses.Statuses import Statuses
# from collections import deque, defaultdict
# from zoo_game_engine.game_engine.objects.BinomialNomenclatureMap import BinomialNomenclatureMap
# if TYPE_CHECKING:
#     from zoo_game_engine.game_engine.objects.BattleState import BattleState
#     from zoo_game_engine.game_engine.objects.ShopState import ShopState
#     from zoo_game_engine.game_engine.objects.RunSnapshot import RunSnapshot
#     from zoo_game_engine.game_engine.objects.ShopUserInput import ShopUserInput
#
#
# class {sub_type}(BaseRecruit):
#
#     def __init__(self,
#                  sub_type: str = None,
#                  type: str = None,
#                  melee_attack: int = None,
#                  ranged_attack: int = None,
#                  health: int = None,
#                  armor: int = None,
#                  statuses: List[BaseStatus] = None,
#                  initiative: int = None,
#                  team_index: int = None,
#                  uuid: str = None,
#                  cost: int = None,
#                  random_seed: str = None,
#                  experience: int = None,
#                  max_health: int = None,
#                  custom_data: dict = None,
#                  name: str = None,
#                  added_types: list[str] = None,
#                  options: list[str] = None,
#                  aaid: int = 0,
#                  **kwargs
#                  ):
#         super().__init__()
#         self.sub_type = "{sub_type}"
#         self.team_index = team_index
#         self.aaid = aaid
#         self.type = "Recruit"
#         self.armor = armor or {armor}
#         self.abilities = {abilities_text}
#         self.melee_attack = melee_attack or {melee_attack}
#         self.ranged_attack = ranged_attack or {ranged_attack}
#         self.health = health or {health}
#         self.statuses = statuses or {statuses}
#         self.triggers = {triggers}
#         self.rarity = "{rarity}"
#         self.probability = GameConstants.Rarity.rarity_to_probability_map[self.rarity]
#         self.cost = cost or {cost}
#         self.uuid = uuid or uuid4().__str__()
#         self.random_seed = random_seed
#         self.initiative = initiative or {initiative} + random_engine.random_float(seed=self.random_seed, snapshot=None)
#         self.experience = experience or 0
#         self.binomial_nomenclature = BinomialNomenclatureMap.map[self.sub_type].copy()
#         self.added_types = added_types or []
#         self.binomial_nomenclature.order.extend(self.added_types)
#         self.max_health = max_health or {health}
#         self.custom_data = custom_data or {{}}
#         self.name = name or self.uuid[:4]
#         self.options = options or ["edit name", "choose art", "make profile pic"]
#
#         # ------ Protect Below from Code Templating ------
# {func_bodies.init_protected_section_code}
#     def update_shop_state(self, shop_state: "ShopState", stack_item: "StackItem",
#                           animation_event_sequence: AnimationList,
#                           original_run_snapshot: "RunSnapshot"):
# {func_bodies.update_shop_state_code}
#     #override everything that happens basically in battle
#     def update_battle_state(self, battle_state: "BattleState", stack_item: "StackItem",
#                             animation_event_sequence: AnimationList, original_run_snapshot: "RunSnapshot"):
# {func_bodies.update_battle_state_code}
#     def receive_damage(self, damage: int, battle_state: "BattleState", enemy: "BaseRecruit",
#                        animation_event_sequence: AnimationList,origin: str = "melee",
#                        original_run_snapshot: "RunSnapshot" = None, damage_reduction_stack: list[int] = None) -> int:
# {func_bodies.receive_damage_code}
#     def receive_unblockable_damage(self, damage: int, battle_state: "BattleState", enemy: "BaseRecruit",
#                                    animation_event_sequence: AnimationList, group: AnimationEvent.InfoByUUID = None,
#                                    origin: str = "melee", original_run_snapshot: "RunSnapshot" = None) -> int:
# {func_bodies.receive_unblockable_damage_code}
#     def update_statuses(self, battle_state: "BattleState", stack_item: StackItem,
#                         animation_event_sequence: AnimationList,
#                         original_run_snapshot: "RunSnapshot" = None):
# {func_bodies.update_statuses_code}
#     def faint(self, battle_state: "BattleState", stack_item: "StackItem",
#               animation_event_sequence: AnimationList,
#               original_run_snapshot: "RunSnapshot" = None):
# {func_bodies.faint_code}
#     def passive_battle_ability(self, battle_state: "BattleState", stack_item: "StackItem",
#                                animation_event_sequence: AnimationList,
#                                original_run_snapshot: "RunSnapshot" = None):
# {func_bodies.passive_battle_ability_code}
#     def start_of_battle(self, battle_state: "BattleState", stack_item: "StackItem",
#                         animation_event_sequence: AnimationList,
#                         original_run_snapshot: "RunSnapshot" = None):
# {func_bodies.start_of_battle_code}
#     def attack_with_melee(self, battle_state: "BattleState", stack_item: "StackItem",
#                           animation_event_sequence: AnimationList,
#                           original_run_snapshot: "RunSnapshot" = None, damage_type: str = "default"):
# {func_bodies.attack_with_melee_code}
#     def attack_with_range(self, battle_state: "BattleState", stack_item: "StackItem",
#                           animation_event_sequence: AnimationList,
#                           original_run_snapshot: "RunSnapshot" = None, damage_type: str = "default"):
# {func_bodies.attack_with_range_code}
#     def shop_start_of_turn(self, shop_state: "ShopState", stack_item: "StackItem",
#                            animation_event_sequence: AnimationList):
# {func_bodies.shop_start_of_turn_code}
#     def shop_end_of_turn(self, shop_state: "ShopState", stack_item: "StackItem",
#                          animation_event_sequence: AnimationList):
# {func_bodies.shop_end_of_turn_code}
#     def shop_level_up(self, shop_state: "ShopState", stack_item: "StackItem",
#                       animation_event_sequence: AnimationList):
# {func_bodies.shop_level_up_code}
#     def shop_set_object_data(self, shop_state: "ShopState", stack_item: "StackItem",
#                              user_input: "ShopUserInput",
#                              animation_event_sequence: AnimationList):
# {func_bodies.shop_set_object_data_code}
#     def shop_gain_experience(self, shop_state: "ShopState", stack_item: "StackItem",
#                              animation_event_sequence: AnimationList):
# {func_bodies.shop_gain_experience_code}
#     def friendly_recruit_faints(self, battle_state: "BattleState", stack_item: StackItem,
#                                 animation_event_sequence: AnimationList,
#                                 original_run_snapshot: "RunSnapshot" = None):
# {func_bodies.friendly_recruit_faints_code}
#     def friendly_recruit_summoned(self, battle_state: "BattleState", stack_item: StackItem,
#                                     animation_event_sequence: AnimationList,
#                                     original_run_snapshot: "RunSnapshot" = None):
# {func_bodies.friendly_recruit_summoned_code}
#     def battle_before_everything(self, battle_state: "BattleState", stack_item: "StackItem",
#                                  animation_event_sequence: AnimationList, original_run_snapshot: "RunSnapshot" = None):
# {func_bodies.battle_before_everything_code}
#     def shop_bought(self, shop_state: "ShopState", stack_item: "StackItem",
#                     animation_event_sequence: AnimationList):
# {func_bodies.shop_bought_code}
#     def shop_sold(self, shop_state: "ShopState", stack_item: "StackItem",
#                   animation_event_sequence: AnimationList):
# {func_bodies.shop_sold_code}
#     def revive(self, battle_state: "BattleState", stack_item: "StackItem",
#                animation_event_sequence: AnimationList,
#                original_run_snapshot: "RunSnapshot" = None):
# {func_bodies.revive_code}
#     def buff_stats(self, state: Union["BattleState", "ShopState"], stack_item: "StackItem",
#                    animation_event_sequence: AnimationList, original_run_snapshot: "RunSnapshot" = None, melee: int = 0,
#                    ranged: int = 0, health: int = 0, armor: int = 0, initiative: int = 0, max_health: int = 0,
#                    buffer: Union["BaseRecruit", "BaseRelic"] = None, group: AnimationEvent.InfoByUUID = None):
# {func_bodies.buff_stats_code}
#
#     def debuff_stats(self, state: Union["BattleState", "ShopState"], stack_item: "StackItem",
#                      animation_event_sequence: AnimationList, original_run_snapshot: "RunSnapshot" = None,
#                      melee: int = 0, ranged: int = 0, health: int = 0, armor: int = 0, initiative: int = 0,
#                      buffer: Union["BaseRecruit", "BaseRelic"] = None, group: AnimationEvent.InfoByUUID = None):
# {func_bodies.debuff_stats_code}
#     def shop_rolled(self, shop_state: "ShopState", stack_item: "StackItem",
#                     animation_event_sequence: AnimationList):
# {func_bodies.shop_rolled_code}
#     def shop_friendly_recruit_summoned(self, shop_state: "ShopState", stack_item: "StackItem",
#                                        animation_event_sequence: AnimationList):
# {func_bodies.shop_friendly_recruit_summoned_code}
#     def heal(self, heal: int, battle_state: "BattleState", healer: "BaseRecruit",
#                  animation_event_sequence: AnimationList):
# {func_bodies.heal_code}
# """


if __name__ == "__main__":
    r = RecruitGenerator()
    r.generate_recruits()
    r.generate_modules()
