import base64
import importlib

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature
from zb7_game_engine.runtime.objects.base.BaseRecruit import BaseRecruit
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus
from zb7_game_engine.serialization.StatusSerializer import StatusSerializer
from zb7_game_engine.serialization.misc.BitFlags import BitFlags


class RecruitSerializer(BaseRecruit):

    @classmethod
    def from_config_json(cls, _json: dict) -> "RecruitSerializer":
        sub_type_as_int = _json["sub_type_as_int"]
        immutable_data = ImmutableData.Subtype.from_int(sub_type_as_int)
        binomial_nomenclature = BinomialNomenclature.from_json(immutable_data["binomial_nomenclature"])
        species = binomial_nomenclature.get_main_species()
        sub_type_as_text = immutable_data["sub_type_as_text"]
        module = importlib.import_module(f"zb7_game_engine.runtime.objects.recruits.{species}.{sub_type_as_text}")
        klass = module.__getattribute__(f"{sub_type_as_text}")
        rarity = _json["rarity"]
        return klass(
            sub_type_as_int=_json["sub_type_as_int"],
            sub_type_as_text=sub_type_as_text,
            team_index=0,
            melee_attack=_json["melee_attack"],
            ranged_attack=_json["ranged_attack"],
            armor=_json["armor"],
            health=_json["health"],
            initiative=_json["initiative"],
            statuses=[],
            max_health=_json["max_health"],
            experience=1,
            rarity=rarity,
            name="",
            binomial_nomenclature=_json["binomial_nomenclature"]
        )


    @classmethod
    def from_human_readable_json(cls, _json: dict):
        pass

    def to_human_readable_json(self) -> dict:
        pass

    def to_base64(self):
        return base64.b64encode(self.to_bytes()).decode("utf-8")

    def to_bytes(self):
        _bytes = bytearray()
        subtype_bytes = self.sub_type_as_int.to_bytes(length=2, byteorder="big")
        team_index_bytes = self.team_index.to_bytes(length=1, byteorder="big")
        bit_flags_signs = bytearray(b"\x00")
        for i, x in enumerate([self.melee_attack, self._ranged_attack, self._armor, self._health, self._initiative]):
            if x < 0:
                bit_flags_signs[0] |= 1 << i

        bit_flags_stats = bytearray(b"\x00")
        for i, x in enumerate([self.melee_attack, self._ranged_attack, self._armor, self._health, self._max_health,
                               self._experience]):
            if abs(x) > 255:
                bit_flags_stats[0] |= 1 << i

        if abs(self._melee_attack) > 255:
            melee_attack_bytes = abs(self._melee_attack).to_bytes(length=2, byteorder="big")
        else:
            melee_attack_bytes = abs(self._melee_attack).to_bytes(length=1, byteorder="big")
        if abs(self._ranged_attack) > 255:
            ranged_attack_bytes = abs(self._ranged_attack).to_bytes(length=2, byteorder="big")
        else:
            ranged_attack_bytes = abs(self._ranged_attack).to_bytes(length=1, byteorder="big")
        if abs(self._armor) > 255:
            armor_bytes = abs(self._armor).to_bytes(length=2, byteorder="big")
        else:
            armor_bytes = abs(self._armor).to_bytes(length=1, byteorder="big")
        if abs(self._health) > 255:
            health_bytes = abs(self._health).to_bytes(length=2, byteorder="big")
        else:
            health_bytes = abs(self._health).to_bytes(length=1, byteorder="big")
        if self._max_health > 255:
            max_health_bytes = self._max_health.to_bytes(length=2, byteorder="big")
        else:
            max_health_bytes = self._max_health.to_bytes(length=1, byteorder="big")
        if self._experience > 255:
            experience_bytes = self._experience.to_bytes(length=2, byteorder="big")
        else:
            experience_bytes = self._experience.to_bytes(length=1, byteorder="big")

        if self._initiative < 0:
            initiative_as_int = ImmutableData.Initiative.to_int(abs(self._initiative))
            initiative_bytes = initiative_as_int.to_bytes(length=2, byteorder="big")
        else:
            initiative_as_int = ImmutableData.Initiative.to_int(self._initiative)
            initiative_bytes = initiative_as_int.to_bytes(length=2, byteorder="big")
        cost_bytes = self._cost.to_bytes(length=1, byteorder="big")
        shop_id_bytes = self.shop_id.to_bytes(length=1, byteorder="big")
        if self.battle_id is None:
            battle_id_bytes = int(0).to_bytes(length=1, byteorder="big")
        else:
            battle_id_bytes = self.battle_id.to_bytes(length=1, byteorder="big")
        aaid_bytes = self._aaid.to_bytes(length=1, byteorder="big")
        # convert a variable length string into bytes
        name_bytes = self._name.encode("utf-8")
        len_of_name = len(name_bytes).to_bytes(length=1, byteorder="big")
        statuses_bytes = b"".join([x.to_bytes() for x in self.statuses])
        len_of_statuses = len(statuses_bytes).to_bytes(length=1, byteorder="big")
        added_types_as_ints = [ImmutableData.ScientificNomenclature.to_int(name_as_text=x) for x in self.added_types]
        added_types_bytes = b"".join([x.to_bytes(length=1, byteorder="big") for x in added_types_as_ints])
        len_of_added_types_bytes = len(added_types_bytes).to_bytes(length=1, byteorder="big")

        added_habitats_as_ints = [ImmutableData.Habitats.from_text(name_as_text=x) for x in self.added_habitats]
        len_of_added_habitats_bytes = len(added_habitats_as_ints).to_bytes(length=1, byteorder="big")

        custom_data_bytes = self.custom_data_to_bytes()


        _bytes.extend(subtype_bytes)
        _bytes.extend(team_index_bytes)
        _bytes.extend(bit_flags_signs)
        _bytes.extend(bit_flags_stats)
        _bytes.extend(melee_attack_bytes)
        _bytes.extend(ranged_attack_bytes)
        _bytes.extend(armor_bytes)
        _bytes.extend(health_bytes)
        _bytes.extend(max_health_bytes)
        _bytes.extend(experience_bytes)
        _bytes.extend(initiative_bytes)
        _bytes.extend(cost_bytes)
        _bytes.extend(shop_id_bytes)
        _bytes.extend(battle_id_bytes)
        _bytes.extend(aaid_bytes)

        _bytes.extend(len_of_name)
        _bytes.extend(name_bytes)

        _bytes.extend(len_of_statuses)
        _bytes.extend(statuses_bytes)

        _bytes.extend(len_of_added_types_bytes)
        _bytes.extend(added_types_bytes)

        _bytes.extend(len_of_added_habitats_bytes)
        _bytes.extend(added_habitats_as_ints)

        _bytes.extend(custom_data_bytes)
        return _bytes

    @classmethod
    def from_base64(cls, base64_string: str) -> "RecruitSerializer":
        _bytes = base64.b64decode(base64_string)
        return cls.from_bytes(_bytes)

    @classmethod
    def bytes_to_custom_data(cls, _bytes: bytes, current_index: int) -> dict:
        return {}

    def custom_data_to_bytes(self) -> bytes:
        return b""

    @classmethod
    def from_bytes(cls, _bytes: bytes) -> "RecruitSerializer":
        current_index = 0
        sub_type_as_int = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        immutable_data = ImmutableData.Subtype.from_int(sub_type_as_int)
        binomial_nomenclature = BinomialNomenclature.from_json(immutable_data["binomial_nomenclature"])
        species = binomial_nomenclature.get_main_species()
        sub_type_as_text = immutable_data["sub_type_as_text"]
        module = importlib.import_module(f"zb7_game_engine.runtime.objects.recruits.{species}.{sub_type_as_text}")
        klass = module.__getattribute__(f"{sub_type_as_text}")

        current_index += 2
        team_index = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        bit_flags_signs = BitFlags.Recruit.Signs(_bytes[current_index:current_index + 1])
        current_index += 1
        bit_flags_stats = BitFlags.Recruit.Stats(_bytes[current_index:current_index + 1])
        current_index += 1
        for key in bit_flags_stats.flags_by_key.keys():
            if bit_flags_stats.flags_by_key[key]:
                value = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
                if bit_flags_signs.flags_by_key.get(key, None):
                    value = value * -1
                bit_flags_stats.values_by_key[key] = value
                current_index += 2
            else:
                value = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
                if bit_flags_signs.flags_by_key.get(key, None):
                    value = value * -1
                bit_flags_stats.values_by_key[key] = value
                current_index += 1

        initiative_as_int = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        initiative_as_float = ImmutableData.Initiative.from_int(initiative_as_int)
        if bit_flags_signs.flags_by_key["initiative"]:
            initiative_as_float = initiative_as_float * -1
        current_index += 2

        cost = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1

        shop_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1

        battle_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1

        aaid = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1

        len_of_name = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        name = _bytes[current_index:current_index + len_of_name].decode("utf-8")
        current_index += len_of_name

        len_of_statuses = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        statuses = []
        for i in range(0, len_of_statuses, 4):
            status = StatusSerializer.from_bytes(_bytes[current_index:current_index + 4])
            statuses.append(status)
            current_index += 4

        len_of_added_types = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        added_types = []
        for i in range(len_of_added_types):
            added_type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
            added_type_as_text = ImmutableData.ScientificNomenclature.from_int(added_type_as_int)
            added_types.append(added_type_as_text)
            current_index += 1

        len_of_added_habitats = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        added_habitats = []
        for i in range(len_of_added_habitats):
            added_habitat_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
            added_habitat_as_text = ImmutableData.Habitats.from_int(added_habitat_as_int)
            added_habitats.append(added_habitat_as_text)
            current_index += 1

        custom_data = klass.bytes_to_custom_data(_bytes, current_index)
        return klass(
            sub_type_as_int=sub_type_as_int,
            sub_type_as_text=sub_type_as_text,
            team_index=team_index,
            melee_attack=bit_flags_stats.values_by_key["melee_attack"],
            ranged_attack=bit_flags_stats.values_by_key["ranged_attack"],
            health=bit_flags_stats.values_by_key["health"],
            max_health=bit_flags_stats.values_by_key["max_health"],
            armor=bit_flags_stats.values_by_key["armor"],
            statuses=statuses,
            triggers=[],
            initiative=initiative_as_float,
            experience=bit_flags_stats.values_by_key["experience"],
            cost=cost,
            shop_id=shop_id,
            battle_id=battle_id,
            random_seed=1,
            binomial_nomenclature=1,
            added_types=added_types,
            added_habitats=added_habitats,
            custom_data=custom_data,
            options={},
            name=name,
            aaid=aaid
        )

    def to_bytes_minimal(self):
        _bytes = bytearray()
        subtype_bytes = self.sub_type_as_int.to_bytes(length=2, byteorder="big")
        shop_id_bytes = self.shop_id.to_bytes(length=1, byteorder="big")
        aaid_bytes = self._aaid.to_bytes(length=1, byteorder="big")
        _bytes.extend(subtype_bytes)
        _bytes.extend(shop_id_bytes)
        _bytes.extend(aaid_bytes)
        return _bytes

    def to_base64_minimal(self):
        _bytes = self.to_bytes_minimal()
        base64_bytes = base64.b64encode(_bytes)
        return base64_bytes.decode("utf-8")

    @staticmethod
    def from_bytes_minimal(_bytes: bytes):
        current_index = 0
        sub_type_as_int = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        immutable_data = ImmutableData.Subtype.from_int(sub_type_as_int)
        binomial_nomenclature = BinomialNomenclature.from_json(immutable_data["binomial_nomenclature"])
        species = binomial_nomenclature.get_main_species()
        sub_type_as_text = immutable_data["sub_type_as_text"]
        module = importlib.import_module(f"zb7_game_engine.runtime.objects.recruits.{species}.{sub_type_as_text}")
        klass = module.__getattribute__(f"{sub_type_as_text}")

        current_index += 2
        shop_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        aaid = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1

        return klass(
            sub_type_as_int=sub_type_as_int,
            sub_type_as_text=sub_type_as_text,
            shop_id=shop_id,
            aaid=aaid,
            type="Recruit"
        )

    @staticmethod
    def from_base64_minimal(base64_string: str):
        _bytes = base64.b64decode(base64_string)
        return RecruitSerializer.from_bytes_minimal(_bytes)

    def copy(self):
        self.to_bytes()
        return self.from_bytes(self.to_bytes())