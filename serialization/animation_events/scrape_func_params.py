import inspect
from collections import defaultdict

from zb7_game_engine.serialization.animation_events.Animations import Animations
if __name__ == "__main__":
    unique_args = defaultdict(list)
    for i, (k, v) in enumerate(Animations.__dict__.items()):
        if k.startswith("_"):
            continue
        lines = inspect.getsourcelines(v.__init__)[0]
        header = []
        current = lines.pop(0)
        while not current.endswith(":\n"):
            header.append(current)
            current = lines.pop(0)
        header.append(current)
        header = "".join(header)
        body = "".join(lines)
        args = header.split("def __init__(self,")[-1]
        args = args.split(")")[0]
        args = args.replace("\n", "")
        args = ' '.join(args.split())
        unique_args[args].append(str(v.__name__))
    for i, (k, v) in enumerate(unique_args.items()):
        print(str(i).ljust(3), k.ljust(140), len(v), v)

