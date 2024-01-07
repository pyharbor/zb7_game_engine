class BaseAbility:
    def __init__(self, name: str, description: str, levels: str, matched_logical_level: list[int] = None):
        self.name = name
        self.description = description
        self.levels = levels
        self.matched_logical_level = matched_logical_level
