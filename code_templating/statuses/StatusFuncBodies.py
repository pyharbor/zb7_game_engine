import importlib
import inspect
import re


class StatusFuncBodies:
    def __init__(self, module_path: str, sub_type_as_text: str):
        self.code_by_function_name = {}
        try:
            protected_function_names = [
                "__init__",
                ]
            function_names = [
                "update_battle_state",
                "stack",
                "on_append",
                "status_effect",

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
                "lt_shop_friendly_recruit_summoned"
            ]
            for x in function_names:
                self.code_by_function_name[x] = StatusFuncBodies.get_function_body_from_module(
                    module_path=module_path,
                    klass_name=sub_type_as_text,
                    function_name=x,
                )
            for x in protected_function_names:
                self.code_by_function_name[x] = StatusFuncBodies.get_section_from_function_body_from_module(
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
        for i in range(0, 10):
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
