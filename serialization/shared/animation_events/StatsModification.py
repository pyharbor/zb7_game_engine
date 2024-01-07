from zb7_game_engine.serialization.misc.BitFlags import BitFlags


class StatsModification:
    @staticmethod
    def to_bytes(self) -> bytearray:
        _bytes = bytearray()
        animation_type_bytes = self.animation_type_as_int.to_bytes(1, byteorder="big")
        state_id_bytes = self.state_id.to_bytes(2, byteorder="big")
        shop_id_bytes = self.shop_id.to_bytes(1, byteorder="big")
        if self.battle_id is None:
            battle_id_bytes = int(0).to_bytes(1, byteorder="big")
        else:
            battle_id_bytes = self.battle_id.to_bytes(1, byteorder="big")

        bit_flags = bytearray(b"\x00")
        for i, x in enumerate([self.melee, self.ranged, self.armor, self.health,
                               self.max_health, self.initiative]):
            if x > 255:
                bit_flags[0] |= 1 << i
        if self.melee > 255:
            melee_attack_bytes = self.melee.to_bytes(length=2, byteorder="big")
        else:
            melee_attack_bytes = self.melee.to_bytes(length=1, byteorder="big")
        if self.ranged > 255:
            ranged_attack_bytes = self.ranged.to_bytes(length=2, byteorder="big")
        else:
            ranged_attack_bytes = self.ranged.to_bytes(length=1, byteorder="big")
        if self.armor > 255:
            armor_bytes = self.armor.to_bytes(length=2, byteorder="big")
        else:
            armor_bytes = self.armor.to_bytes(length=1, byteorder="big")
        if self.health > 255:
            health_bytes = self.health.to_bytes(length=2, byteorder="big")
        else:
            health_bytes = self.health.to_bytes(length=1, byteorder="big")
        if self.max_health > 255:
            max_health_bytes = self.max_health.to_bytes(length=2, byteorder="big")
        else:
            max_health_bytes = self.max_health.to_bytes(length=1, byteorder="big")
        if self.initiative > 255:
            initiative_bytes = self.initiative.to_bytes(length=2, byteorder="big")
        else:
            initiative_bytes = self.initiative.to_bytes(length=1, byteorder="big")

        _bytes = bytearray()
        _bytes.extend(animation_type_bytes)
        _bytes.extend(state_id_bytes)
        _bytes.extend(shop_id_bytes)
        _bytes.extend(battle_id_bytes)
        _bytes.extend(bit_flags)
        _bytes.extend(melee_attack_bytes)
        _bytes.extend(ranged_attack_bytes)
        _bytes.extend(armor_bytes)
        _bytes.extend(health_bytes)
        _bytes.extend(max_health_bytes)
        _bytes.extend(initiative_bytes)
        return _bytes

    @staticmethod
    def from_bytes(cls, _bytes: bytes):
        current_index = 0
        animation_type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        state_id = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 2
        shop_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        battle_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        bit_flags = BitFlags.Debuff(_bytes[current_index:current_index + 1])
        current_index += 1
        for key in bit_flags.flags_by_key.keys():
            if bit_flags.flags_by_key[key]:
                bit_flags.values_by_key[key] = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
                current_index += 2
            else:
                bit_flags.values_by_key[key] = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
                current_index += 1

        return cls(state_id=state_id, health=bit_flags.values_by_key["health"], melee=bit_flags.values_by_key["melee"],
                   ranged=bit_flags.values_by_key["ranged"], armor=bit_flags.values_by_key["armor"],
                   initiative=bit_flags.values_by_key["initiative"], max_health=bit_flags.values_by_key["max_health"],
                   shop_id=shop_id, battle_id=battle_id)
