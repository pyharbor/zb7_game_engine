class BitFlags:
    class Recruit:
        class Stats:
            # basically we store bits to indicate the length of the value
            def __init__(self, _bytes: bytes):
                self.flags_by_key = {
                    "melee_attack": _bytes[0] & 0b00000001,
                    "ranged_attack": _bytes[0] & 0b00000010,
                    "armor": _bytes[0] & 0b00000100,
                    "health": _bytes[0] & 0b00001000,
                    "max_health": _bytes[0] & 0b00010000,
                    "experience": _bytes[0] & 0b00100000
                }
                self.values_by_key = {
                    "melee_attack": None,
                    "ranged_attack": None,
                    "armor": None,
                    "health": None,
                    "max_health": None,
                    "experience": None
                }

            def __str__(self):
                return str(self.flags_by_key)

        class Signs:
            # basically we store bits to indicate if the number is positive or negative
            def __init__(self, _bytes: bytes):
                self.flags_by_key = {
                    "melee_attack": _bytes[0] & 0b00000001,
                    "ranged_attack": _bytes[0] & 0b00000010,
                    "armor": _bytes[0] & 0b00000100,
                    "health": _bytes[0] & 0b00001000,
                    "initiative": _bytes[0] & 0b00010000,
                }

            def __str__(self):
                return str(self.flags_by_key)

    class Debuff:
        def __init__(self, _bytes: bytes):
            self.flags_by_key = {
                "melee": _bytes[0] & 0b00000001,
                "ranged": _bytes[0] & 0b00000010,
                "armor": _bytes[0] & 0b00000100,
                "health": _bytes[0] & 0b00001000,
                "max_health": _bytes[0] & 0b00010000,
                "initiative": _bytes[0] & 0b00100000,
            }
            self.values_by_key = {
                "melee_attack": None,
                "ranged_attack": None,
                "armor": None,
                "health": None,
                "max_health": None,
                "initiative": None
            }

        def __str__(self):
            return str(self.flags_by_key)
