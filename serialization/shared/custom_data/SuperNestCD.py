from zb7_game_engine.immutable_data.ImmutableData import ImmutableData


class SuperNestCD:

    @staticmethod
    def bytes_to_custom_data(_bytes: bytes, current_index: int) -> dict:
        construction_counter = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 2
        len_start_of_battle_sub_types = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        start_of_battle_buffs = {}
        battle_friendly_recruit_summoned = {}
        if len_start_of_battle_sub_types > 0:
            for x in range(len_start_of_battle_sub_types):
                sub_type_as_int = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
                sub_type_as_text = ImmutableData.Subtype.from_int(sub_type_as_int)["sub_type_as_text"]
                current_index += 2
                melee_buff = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
                current_index += 1
                ranged_buff = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
                current_index += 1
                armor_buff = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
                current_index += 1
                health_buff = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
                current_index += 1
                initiative_buff = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
                current_index += 1
                start_of_battle_buffs[sub_type_as_text] = {"melee_buff": melee_buff,
                                                           "ranged_buff": ranged_buff,
                                                           "armor_buff": armor_buff,
                                                           "health_buff": health_buff,
                                                           "initiative_buff": initiative_buff}

        len_on_summon_sub_types = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        if len_on_summon_sub_types > 0:
            for x in range(len_on_summon_sub_types):
                sub_type_as_int = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
                sub_type_as_text = ImmutableData.Subtype.from_int(sub_type_as_int)["sub_type_as_text"]
                current_index += 2

                melee_buff = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
                current_index += 1
                ranged_buff = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
                current_index += 1
                armor_buff = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
                current_index += 1
                health_buff = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
                current_index += 1
                initiative_buff = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
                current_index += 1
                battle_friendly_recruit_summoned[sub_type_as_text] = {"melee_buff": melee_buff,
                                                                            "ranged_buff": ranged_buff,
                                                                            "armor_buff": armor_buff,
                                                                            "health_buff": health_buff,
                                                                            "initiative_buff": initiative_buff}

        return {
            "construction_counter": construction_counter,
            "start_of_battle": start_of_battle_buffs,
            "battle_friendly_recruit_summoned": battle_friendly_recruit_summoned}

    @staticmethod
    def custom_data_to_bytes(self) -> bytes:

        _bytes = bytearray()
        construction_counter = self.custom_data["construction_counter"]
        construction_counter_as_bytes = construction_counter.to_bytes(2, byteorder="big")

        len_start_of_battle_sub_types = len(self.custom_data["start_of_battle"])
        len_start_of_battle_sub_types_as_bytes = len_start_of_battle_sub_types.to_bytes(1, byteorder="big")
        start_of_battle_sub_types_as_bytes = bytearray()
        for x in self.custom_data["start_of_battle"]:
            melee_buff = self.custom_data["start_of_battle"][x]["melee_buff"]
            melee_buff_as_bytes = melee_buff.to_bytes(1, byteorder="big")
            ranged_buff = self.custom_data["start_of_battle"][x]["ranged_buff"]
            ranged_buff_as_bytes = ranged_buff.to_bytes(1, byteorder="big")
            armor_buff = self.custom_data["start_of_battle"][x]["armor_buff"]
            armor_buff_as_bytes = armor_buff.to_bytes(1, byteorder="big")
            health_buff = self.custom_data["start_of_battle"][x]["health_buff"]
            health_buff_as_bytes = health_buff.to_bytes(1, byteorder="big")
            initiative_buff = self.custom_data["start_of_battle"][x]["initiative_buff"]
            initiative_buff_as_bytes = initiative_buff.to_bytes(1, byteorder="big")
            sub_type_as_int = ImmutableData.Subtype.from_text(x)["sub_type_as_int"]
            sub_type_as_int_as_bytes = sub_type_as_int.to_bytes(2, byteorder="big")
            start_of_battle_sub_types_as_bytes.extend(sub_type_as_int_as_bytes)
            start_of_battle_sub_types_as_bytes.extend(melee_buff_as_bytes)
            start_of_battle_sub_types_as_bytes.extend(ranged_buff_as_bytes)
            start_of_battle_sub_types_as_bytes.extend(armor_buff_as_bytes)
            start_of_battle_sub_types_as_bytes.extend(health_buff_as_bytes)
            start_of_battle_sub_types_as_bytes.extend(initiative_buff_as_bytes)
        
        len_on_summon_sub_types = len(self.custom_data["battle_friendly_recruit_summoned"])
        len_on_summon_sub_types_as_bytes = len_on_summon_sub_types.to_bytes(1, byteorder="big")
        on_summon_sub_types_as_bytes = bytearray()
        for x in self.custom_data["battle_friendly_recruit_summoned"]:
            melee_buff = self.custom_data["start_of_battle_buffs"][x]["melee_buff"]
            melee_buff_as_bytes = melee_buff.to_bytes(1, byteorder="big")
            ranged_buff = self.custom_data["start_of_battle_buffs"][x]["ranged_buff"]
            ranged_buff_as_bytes = ranged_buff.to_bytes(1, byteorder="big")
            armor_buff = self.custom_data["start_of_battle_buffs"][x]["armor_buff"]
            armor_buff_as_bytes = armor_buff.to_bytes(1, byteorder="big")
            health_buff = self.custom_data["start_of_battle_buffs"][x]["health_buff"]
            health_buff_as_bytes = health_buff.to_bytes(1, byteorder="big")
            initiative_buff = self.custom_data["start_of_battle_buffs"][x]["initiative_buff"]
            initiative_buff_as_bytes = initiative_buff.to_bytes(1, byteorder="big")
            sub_type_as_int = ImmutableData.Subtype.from_text(x)["sub_type_as_int"]
            sub_type_as_int_as_bytes = sub_type_as_int.to_bytes(2, byteorder="big")
            on_summon_sub_types_as_bytes.extend(sub_type_as_int_as_bytes)
            on_summon_sub_types_as_bytes.extend(melee_buff_as_bytes)
            on_summon_sub_types_as_bytes.extend(ranged_buff_as_bytes)
            on_summon_sub_types_as_bytes.extend(armor_buff_as_bytes)
            on_summon_sub_types_as_bytes.extend(health_buff_as_bytes)
            on_summon_sub_types_as_bytes.extend(initiative_buff_as_bytes)


        _bytes.extend(construction_counter_as_bytes)
        _bytes.extend(len_start_of_battle_sub_types_as_bytes)
        _bytes.extend(start_of_battle_sub_types_as_bytes)
        _bytes.extend(len_on_summon_sub_types_as_bytes)
        _bytes.extend(on_summon_sub_types_as_bytes)
        return _bytes
