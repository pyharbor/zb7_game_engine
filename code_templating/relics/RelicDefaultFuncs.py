from zb7_game_engine.code_templating.templates.TemplateRelic import TemplateRelic
from zb7_game_engine.code_templating.FunctionSourceCode import FunctionSourceCode


class RelicDefaultFuncs:
    code_by_func_name = {}
    for k, v in TemplateRelic.__dict__.items():
        if k.startswith("__"):
            continue
        x = FunctionSourceCode.from_function(v)
        code_by_func_name[x.function_name] = x
