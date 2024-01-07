import inspect


class FunctionSourceCode:
    def __init__(self, function_name: str, function_header: str, function_body: str):
        self.function_header = function_header
        self.function_body = function_body
        self.function_name = function_name

    @classmethod
    def from_function(cls, function):
        lines = inspect.getsourcelines(function)[0]
        header = []
        current = lines.pop(0)
        while not current.endswith(":\n"):
            header.append(current)
            current = lines.pop(0)
        header.append(current)
        header = "".join(header)
        body = "".join(lines)
        return FunctionSourceCode(function.__name__, header, body)

