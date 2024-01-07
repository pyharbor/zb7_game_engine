from zb7_game_engine.code_templating.templates.TemplateRecruit import TemplateRecruit
from zb7_game_engine.code_templating.FunctionSourceCode import FunctionSourceCode


class AnimationEventDefaultFuncs:
    code_by_func_name = {}
    for k, v in TemplateRecruit.__dict__.items():
        if k.startswith("__"):
            continue
        x = FunctionSourceCode.from_function(v)
        code_by_func_name[x.function_name] = x
