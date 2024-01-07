import importlib
import inspect
import re


class AnimationEventFuncBodies:
    def __init__(self, module_path: str, sub_type_as_text: str):
        self.code_by_function_name = {}
        try:
            protected_function_names = [
                "__init__",
                ]
            function_names = [
                "update_shop_state",
                "update_battle_state",
                "receive_damage",
                "receive_unblockable_damage",
                "update_statuses",
                "faint",
                "revive",
                "passive_battle_ability",
                "start_of_battle",
                "attack_with_melee",
                "attack_with_range",
                "shop_start_of_turn",
                "shop_end_of_turn",
                "shop_level_up",
                "shop_set_object_data",
                "shop_gain_experience",
                "friendly_recruit_summoned"
            ]
            for x in function_names:
                self.code_by_function_name[x] = AnimationEventFuncBodies.get_function_body_from_module(
                    module_path=module_path,
                    klass_name=sub_type_as_text,
                    function_name=x,
                )
            for x in protected_function_names:
                self.code_by_function_name[x] = AnimationEventFuncBodies.get_section_from_function_body_from_module(
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
