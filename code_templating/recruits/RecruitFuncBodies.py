import importlib
import inspect
import re


class RecruitFuncBodies:
    def __init__(self, module_path: str, sub_type_as_text: str):
        self.code_by_function_name = {}
        try:
            protected_function_names = [
                "__init__",
                ]
            function_names = [
                "shop_bought",
                "shop_sold",
                "shop_rolled",
                "shop_level_up",
                "battle_level_up",
                "shop_set_object_data",
                "shop_gain_experience",
                "battle_gain_experience",
                "battle_receive_status_damage",
                "battle_before_everything",
                "shop_start_of_turn",
                "shop_end_of_turn",
                "battle_heal",
                "battle_receive_damage",
                "shop_receive_damage",
                "shop_receive_unblockable_damage",
                "battle_receive_unblockable_damage",
                "battle_debuff_stats",
                "shop_debuff_stats",
                "battle_buff_stats",
                "shop_buff_stats",
                "generic_ability_notification",
                "shop_attack_with_range",
                "battle_attack_with_range",
                "shop_revive",
                "battle_revive",
                "shop_attack_with_melee",
                "battle_attack_with_melee",
                "shop_faint",
                "battle_faint",
                "passive_battle_ability",
                "start_of_battle",
                "battle_friendly_recruit_faints",
                "battle_friendly_recruit_summoned",
                "shop_friendly_recruit_faints",
                "shop_friendly_recruit_summoned",
                "update_battle_state",
                "update_shop_state",
                "bytes_to_custom_data",
                "custom_data_to_bytes",
                "shop_friendly_recruit_sold",

                "lt_shop_bought",
                "lt_shop_sold",
                "lt_shop_rolled",
                "lt_shop_level_up",
                "lt_battle_level_up",
                "lt_shop_set_object_data",
                "lt_shop_gain_experience",
                "lt_battle_gain_experience",
                "lt_battle_receive_status_damage",
                "lt_battle_before_everything",
                "lt_shop_start_of_turn",
                "lt_shop_end_of_turn",
                "lt_battle_heal",
                "lt_battle_receive_damage",
                "lt_shop_receive_damage",
                "lt_shop_receive_unblockable_damage",
                "lt_battle_receive_unblockable_damage",
                "lt_battle_debuff_stats",
                "lt_shop_debuff_stats",
                "lt_battle_buff_stats",
                "lt_shop_buff_stats",
                "lt_shop_attack_with_range",
                "lt_battle_attack_with_range",
                "lt_shop_revive",
                "lt_battle_revive",
                "lt_shop_attack_with_melee",
                "lt_battle_attack_with_melee",
                "lt_shop_faint",
                "lt_battle_faint",
                "lt_passive_battle_ability",
                "lt_start_of_battle",
                "lt_battle_friendly_recruit_faints",
                "lt_battle_friendly_recruit_summoned",
                "lt_shop_friendly_recruit_faints",
                "lt_shop_friendly_recruit_summoned",
                "lt_add_status"

            ]
            for x in function_names:
                self.code_by_function_name[x] = RecruitFuncBodies.get_function_body_from_module(
                    module_path=module_path,
                    klass_name=sub_type_as_text,
                    function_name=x,
                )
            for x in protected_function_names:
                self.code_by_function_name[x] = RecruitFuncBodies.get_section_from_function_body_from_module(
                    module_path=module_path,
                    klass_name=sub_type_as_text,
                    function_name=x,
                    nested_regex="(?P<section># ------ Protect Below from Code Templating ------\n)(?P<code>[\S\s]*).*",
                )

        except ModuleNotFoundError as e:
            print(repr(e))

    @staticmethod
    def get_function_body_from_module(module_path: str, klass_name: str,  function_name: str):
        module = importlib.import_module(module_path)
        klass = module.__getattribute__(f"{klass_name}")
        try:
            function = getattr(klass, function_name)
            for x in ["BaseRecruit", "BaseRelic", "BaseStatus", "BaseListener"]:
                if x in str(function):
                    return None
        except AttributeError:
            return None
        lines = inspect.getsource(function)
        matched = False
        for i in range(0, 20):
            amount_of_new_lines = "\n.*" * i
            func_body_regex = f"(?P<func_name>def {function_name}\(.*{amount_of_new_lines}\).*:)\n(?P<func_body>[\S\s]*)"
            match = re.search(string=lines, pattern=func_body_regex)
            if match is not None:
                matched = True
                break
        if not matched:
            raise ValueError(f"Could not find function body for {klass_name} {function_name} in {klass}")
        return match.group("func_body")

    @staticmethod
    def get_section_from_function_body_from_module(module_path: str, klass_name: str, nested_regex: str, function_name: str):
        module = importlib.import_module(module_path)
        klass = module.__getattribute__(f"{klass_name}")
        function = getattr(klass, function_name)
        lines = inspect.getsource(function)
        section = re.search(pattern=nested_regex, string=lines)
        if section is not None:
            return section.group("code")
        else:
            return ""
