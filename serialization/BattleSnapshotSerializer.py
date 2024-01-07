import base64

from pyharbor_shared_library.Date import Date

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.StateSet import StateSet
from zb7_game_engine.runtime.core.snapshots.BattleSnapshot import BattleSnapshot
from zb7_game_engine.runtime.misc.decks.Decks import Decks
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer
from zb7_game_engine.serialization.ShopSnapshotSerializer import ShopSnapshotSerializer


class BattleSnapshotSerializer(BattleSnapshot):

    @classmethod
    def from_human_readable_json(cls, _json: dict):
        pass

    def to_human_readable_json(self) -> dict:
        pass

    def convert_snapshot_data_to_bytes(self):
        _bytes = bytearray()
        snapshot_type_as_int_bytes = self.snapshot_type_as_int.to_bytes(length=1, byteorder="big")
        snapshot_sub_type_as_int_bytes = self.snapshot_sub_type_as_int.to_bytes(length=1, byteorder="big")

        friendly_uuid_bytes = self.friendly_uuid.encode("utf-8")
        friendly_username_bytes = self.friendly_username.encode("utf-8")
        friendly_username_len_bytes = len(friendly_username_bytes).to_bytes(length=1, byteorder="big")
        friendly_deck_bytes = self.friendly_deck.to_bytes()
        len_friendly_deck_bytes = len(friendly_deck_bytes).to_bytes(length=1, byteorder="big")
        friendly_wins_bytes = self.friendly_wins.to_bytes(length=1, byteorder="big")
        friendly_health_bytes = self.friendly_health.to_bytes(length=1, byteorder="big")
        friendly_money_bytes = self.friendly_money.to_bytes(length=2, byteorder="big")
        friendly_turn_bytes = self.friendly_turn.to_bytes(length=1, byteorder="big")
        friendly_utc_date_str_bytes = self.friendly_utc_date_str.encode("utf-8")
        friendly_utc_date_str_len_bytes = len(friendly_utc_date_str_bytes).to_bytes(length=1, byteorder="big")
        friendly_run_status_as_int_bytes = self.friendly_run_status_as_int.to_bytes(length=1, byteorder="big")

        enemy_uuid_bytes = self.enemy_uuid.encode("utf-8")
        enemy_username_bytes = self.enemy_username.encode("utf-8")
        enemy_username_len_bytes = len(enemy_username_bytes).to_bytes(length=1, byteorder="big")
        enemy_deck_bytes = self.enemy_deck.to_bytes()
        len_enemy_deck_bytes = len(enemy_deck_bytes).to_bytes(length=1, byteorder="big")
        enemy_wins_bytes = self.enemy_wins.to_bytes(length=1, byteorder="big")
        enemy_health_bytes = self.enemy_health.to_bytes(length=1, byteorder="big")
        enemy_money_bytes = self.enemy_money.to_bytes(length=2, byteorder="big")
        enemy_turn_bytes = self.enemy_turn.to_bytes(length=1, byteorder="big")
        enemy_utc_date_str_bytes = self.enemy_utc_date_str.encode("utf-8")
        enemy_utc_date_str_len_bytes = len(enemy_utc_date_str_bytes).to_bytes(length=1, byteorder="big")
        enemy_run_status_as_int_bytes = self.enemy_run_status_as_int.to_bytes(length=1, byteorder="big")

        vs_mode_as_int_bytes = self.vs_mode_as_int.to_bytes(length=1, byteorder="big")
        operation_count_bytes = self.operation_count.to_bytes(length=2, byteorder="big")
        battle_result_as_int_bytes = self.battle_result_as_int.to_bytes(length=1, byteorder="big")

        _bytes.extend(snapshot_type_as_int_bytes)
        _bytes.extend(snapshot_sub_type_as_int_bytes)
        _bytes.extend(friendly_uuid_bytes)
        _bytes.extend(friendly_username_len_bytes)
        _bytes.extend(friendly_username_bytes)
        _bytes.extend(len_friendly_deck_bytes)
        _bytes.extend(friendly_deck_bytes)
        _bytes.extend(friendly_wins_bytes)
        _bytes.extend(friendly_health_bytes)
        _bytes.extend(friendly_money_bytes)
        _bytes.extend(friendly_turn_bytes)
        _bytes.extend(friendly_utc_date_str_len_bytes)
        _bytes.extend(friendly_utc_date_str_bytes)
        _bytes.extend(friendly_run_status_as_int_bytes)
        _bytes.extend(enemy_uuid_bytes)
        _bytes.extend(enemy_username_len_bytes)
        _bytes.extend(enemy_username_bytes)
        _bytes.extend(len_enemy_deck_bytes)
        _bytes.extend(enemy_deck_bytes)
        _bytes.extend(enemy_wins_bytes)
        _bytes.extend(enemy_health_bytes)
        _bytes.extend(enemy_money_bytes)
        _bytes.extend(enemy_turn_bytes)
        _bytes.extend(enemy_utc_date_str_len_bytes)
        _bytes.extend(enemy_utc_date_str_bytes)
        _bytes.extend(enemy_run_status_as_int_bytes)
        _bytes.extend(vs_mode_as_int_bytes)
        _bytes.extend(operation_count_bytes)
        _bytes.extend(battle_result_as_int_bytes)
        return _bytes

    def to_json(self):
        _bytes = self.convert_snapshot_data_to_bytes()
        snapshot_base64_text = base64.b64encode(_bytes).decode("utf-8")
        _json = {
            "i": snapshot_base64_text,
            "s": self.state_set.to_json(),
            "a": self.animation_event_sequence.to_json(),
            "previous_luuid": self.previous_luuid,
            "luuid": self.luuid,
        }
        return _json

    @staticmethod
    def from_json(_json) -> "BattleSnapshotSerializer":
        snapshot_base64_text = _json["i"]

        _bytes = base64.b64decode(snapshot_base64_text)
        current_index = 0
        snapshot_type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        snapshot_type_as_text = ImmutableData.Misc.from_int(snapshot_type_as_int)
        current_index += 1
        snapshot_sub_type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        snapshot_sub_type_as_text = ImmutableData.Misc.from_int(snapshot_sub_type_as_int)
        current_index += 1

        friendly_uuid = _bytes[current_index:current_index + 36].decode("utf-8")
        current_index += 36
        friendly_username_len = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        friendly_username = _bytes[current_index:current_index + friendly_username_len].decode("utf-8")
        current_index += friendly_username_len

        len_friendly_deck = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        friendly_deck_bytes = _bytes[current_index:current_index + len_friendly_deck]
        current_index += len_friendly_deck
        base64_text = base64.b64encode(friendly_deck_bytes).decode("utf-8")
        friendly_deck = DeckSerializer.from_base64_text(base64_text)


        friendly_wins = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        friendly_health = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        friendly_money = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 2
        friendly_turn = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        friendly_utc_date_str_len = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        friendly_utc_date_str = _bytes[current_index:current_index + friendly_utc_date_str_len].decode("utf-8")
        current_index += friendly_utc_date_str_len
        friendly_run_status_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        enemy_uuid = _bytes[current_index:current_index + 36].decode("utf-8")
        current_index += 36
        enemy_username_len = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        enemy_username = _bytes[current_index:current_index + enemy_username_len].decode("utf-8")
        current_index += enemy_username_len

        len_enemy_deck = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        enemy_deck_bytes = _bytes[current_index:current_index + len_enemy_deck]
        current_index += len_enemy_deck
        base64_text = base64.b64encode(enemy_deck_bytes).decode("utf-8")
        enemy_deck = DeckSerializer.from_base64_text(base64_text)


        enemy_wins = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        enemy_health = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        enemy_money = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 2
        enemy_turn = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        enemy_utc_date_str_len = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        enemy_utc_date_str = _bytes[current_index:current_index + enemy_utc_date_str_len].decode("utf-8")
        current_index += enemy_utc_date_str_len
        enemy_run_status_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1

        vs_mode_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1

        operation_count = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 2
        battle_result_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1

        friendly_run_status_as_text = ImmutableData.Misc.from_int(friendly_run_status_as_int)
        enemy_run_status_as_text = ImmutableData.Misc.from_int(enemy_run_status_as_int)
        vs_mode_as_text = ImmutableData.Misc.from_int(vs_mode_as_int)
        animation_event_sequence = AnimationEventSequence.from_json(_json=_json["a"])
        state_set = StateSet.from_json(_json=_json["s"], snapshot_type_as_text=snapshot_type_as_text)

        previous_luuid = _json["previous_luuid"]
        luuid = _json["luuid"]

        snapshot = BattleSnapshotSerializer(
            friendly_uuid=friendly_uuid,
            friendly_username=friendly_username,
            friendly_deck=friendly_deck,
            friendly_wins=friendly_wins,
            friendly_health=friendly_health,
            friendly_money=friendly_money,
            friendly_turn=friendly_turn,
            friendly_utc_date_str=friendly_utc_date_str,
            friendly_run_status_as_int=friendly_run_status_as_int,
            friendly_run_status_as_text=friendly_run_status_as_text,
            enemy_uuid=enemy_uuid,
            enemy_username=enemy_username,
            enemy_deck=enemy_deck,
            enemy_wins=enemy_wins,
            enemy_health=enemy_health,
            enemy_money=enemy_money,
            enemy_turn=enemy_turn,
            enemy_utc_date_str=enemy_utc_date_str,
            enemy_run_status_as_int=enemy_run_status_as_int,
            enemy_run_status_as_text=enemy_run_status_as_text,
            vs_mode_as_int=vs_mode_as_int,
            vs_mode_as_text=vs_mode_as_text,
            operation_count=operation_count,
            previous_luuid=previous_luuid,
            luuid=luuid,
            animation_event_sequence=animation_event_sequence,
            state_set=state_set,
            battle_result_as_int=battle_result_as_int,
            snapshot_sub_type_as_int=snapshot_sub_type_as_int,
            snapshot_sub_type_as_text=snapshot_sub_type_as_text
        )
        return snapshot


if __name__ == "__main__":
    from zb7_game_engine.runtime.misc.debugging.Debug import Debug
    import uuid
    s = uuid.uuid4().__str__()
    s2 = uuid.uuid4().__str__()
    luuid = uuid.uuid4().__str__()
    previous_luuid = uuid.uuid4().__str__()
    b = BattleSnapshotSerializer(
        friendly_uuid=s,
        friendly_username="test",
        friendly_deck=Decks.Polyneoptera.deck,
        friendly_wins=1,
        friendly_health=6,
        friendly_money=23,
        friendly_turn=7,
        friendly_utc_date_str=Date.US_Eastern.now_str(),
        friendly_run_status_as_int=3,
        friendly_run_status_as_text="pending",
        enemy_uuid=s2,
        enemy_username="test2",
        enemy_deck=Decks.Polyneoptera.deck,
        enemy_wins=2,
        enemy_health=9,
        enemy_money=14,
        enemy_turn=7,
        enemy_utc_date_str=Date.US_Eastern.now_str(),
        enemy_run_status_as_int=3,
        enemy_run_status_as_text="pending",
        vs_mode_as_int=5,
        vs_mode_as_text="custom_deck",
        operation_count=0,
        previous_luuid=previous_luuid,
        luuid=luuid,
        animation_event_sequence=AnimationEventSequence(),
        state_set=StateSet(),
        battle_result_as_int=0
    )
    b2 = BattleSnapshotSerializer.from_json(b.to_json())
    print(b.to_json())
    print(b2.to_json())
    print(b.to_json() == b2.to_json())
    Debug.BattleSnapshotSerializer.print(b)
    Debug.BattleSnapshotSerializer.print(b2)

