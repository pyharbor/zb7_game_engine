from zb7_game_engine.immutable_data.ImmutableData import ImmutableData


class CarpenterAntCD:

    @staticmethod
    def custom_data_to_bytes(self) -> bytes:
        _bytes = bytearray()
        trigger_as_bytes = self.custom_data["trigger"].to_bytes(length=1, byteorder="big")
        _bytes.extend(trigger_as_bytes)
        for sub_type_as_text, stats in self.custom_data.items():
            if sub_type_as_text == "trigger":
                continue
            sub_type_as_int = ImmutableData.Subtype.from_text(sub_type_as_text)["sub_type_as_int"]
            subtype_bytes = sub_type_as_int.to_bytes(length=2, byteorder="big")
            melee_attack = stats["melee_attack"].to_bytes(length=1, byteorder="big")
            ranged_attack = stats["ranged_attack"].to_bytes(length=1, byteorder="big")
            armor = stats["armor"].to_bytes(length=1, byteorder="big")
            max_health = stats["health"].to_bytes(length=1, byteorder="big")
            initiative = stats["initiative"].to_bytes(length=1, byteorder="big")
            _bytes.extend(subtype_bytes)
            _bytes.extend(melee_attack)
            _bytes.extend(ranged_attack)
            _bytes.extend(armor)
            _bytes.extend(max_health)
            _bytes.extend(initiative)

        return _bytes

    @staticmethod
    def bytes_to_custom_data(_bytes: bytes, current_index: int) -> dict:
        custom_data = {}
        trigger = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        custom_data["trigger"] = trigger
        while current_index < len(_bytes):
            sub_type_as_int = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
            sub_type_as_text = ImmutableData.Subtype.from_int(sub_type_as_int)["sub_type_as_text"]
            current_index += 2
            melee_attack = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
            current_index += 1
            ranged_attack = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
            current_index += 1
            armor = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
            current_index += 1
            max_health = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
            current_index += 1
            initiative = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
            current_index += 1
            custom_data[sub_type_as_text] = {
                "sub_type_as_text": sub_type_as_text,
                "melee_attack": melee_attack,
                "ranged_attack": ranged_attack,
                "armor": armor,
                "health": max_health,
                "initiative": initiative,
            }
        return custom_data