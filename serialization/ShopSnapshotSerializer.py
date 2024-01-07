import base64
from uuid import uuid4

from pyharbor_shared_library.Date import Date

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.RandomEngine import random_engine
from zb7_game_engine.runtime.core.StateSet import StateSet
from zb7_game_engine.runtime.core.snapshots.ShopSnapshot import ShopSnapshot
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer
from zb7_game_engine.serialization.EmptySlotSerializer import EmptySlotSerializer
from zb7_game_engine.serialization.PlayerDecisionInfoSerializer import PlayerDecisionInfoSerializer
from zb7_game_engine.serialization.ShopStateSerializer import ShopStateSerializer
from zb7_game_engine.serialization.animation_events.Animations import Animations


class ShopSnapshotSerializer(ShopSnapshot):
    @classmethod
    def from_human_readable_json(cls, _json: dict):
        pass

    def to_human_readable_json(self) -> dict:
        pass

    def convert_snapshot_data_to_bytes(self):
        _bytes = bytearray()
        snapshot_type_as_int_bytes = self.snapshot_type_as_int.to_bytes(length=1, byteorder="big")
        snapshot_sub_type_as_int_bytes = self.snapshot_sub_type_as_int.to_bytes(length=1, byteorder="big")
        state_id_bytes = self.state_id.to_bytes(length=2, byteorder="big")
        operation_count_bytes = self.operation_count.to_bytes(length=2, byteorder="big")
        username_bytes = self.username.encode("utf-8")
        username_len_bytes = len(username_bytes).to_bytes(length=1, byteorder="big")
        deck_bytes = self.deck.to_bytes()
        len_deck_bytes = len(deck_bytes).to_bytes(length=1, byteorder="big")
        uuid_bytes = self.uuid.encode("utf-8")
        len_uuid_bytes = len(uuid_bytes).to_bytes(length=1, byteorder="big")
        vs_mode_as_int_bytes = self.vs_mode_as_int.to_bytes(length=1, byteorder="big")
        run_status_bytes = self.run_status_as_int.to_bytes(length=1, byteorder="big")
        utc_date_str_bytes = self.utc_date_str.encode("utf-8")
        utc_date_str_len_bytes = len(utc_date_str_bytes).to_bytes(length=1, byteorder="big")
        player_decision_info_len_bytes = int(0).to_bytes(length=1, byteorder="big")
        player_decision_info_bytes = b""
        if self.player_decision_info is not None:
            player_decision_info_bytes = self.player_decision_info.to_bytes()
            player_decision_info_len_bytes = len(player_decision_info_bytes).to_bytes(length=1, byteorder="big")

        _bytes.extend(snapshot_type_as_int_bytes)
        _bytes.extend(snapshot_sub_type_as_int_bytes)
        _bytes.extend(state_id_bytes)
        _bytes.extend(operation_count_bytes)
        _bytes.extend(username_len_bytes)
        _bytes.extend(username_bytes)
        _bytes.extend(len_deck_bytes)
        _bytes.extend(deck_bytes)
        _bytes.extend(len_uuid_bytes)
        _bytes.extend(uuid_bytes)
        _bytes.extend(vs_mode_as_int_bytes)
        _bytes.extend(run_status_bytes)
        _bytes.extend(utc_date_str_len_bytes)
        _bytes.extend(utc_date_str_bytes)
        _bytes.extend(player_decision_info_len_bytes)
        _bytes.extend(player_decision_info_bytes)
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
    def from_json(_json) -> "ShopSnapshotSerializer":
        snapshot_base64_text = _json["i"]
        _bytes = base64.b64decode(snapshot_base64_text)
        current_index = 0
        snapshot_type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        snapshot_type_as_text = ImmutableData.Misc.from_int(snapshot_type_as_int)
        current_index += 1
        snapshot_sub_type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        snapshot_sub_type_as_text = ImmutableData.Misc.from_int(snapshot_sub_type_as_int)
        current_index += 1

        state_id = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 2

        operation_count = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 2

        username_len = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1

        username = _bytes[current_index:current_index + username_len].decode("utf-8")
        current_index += username_len

        deck_len = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        deck_bytes = _bytes[current_index:current_index + deck_len]
        current_index += deck_len
        base64_text = base64.b64encode(deck_bytes).decode("utf-8")
        deck = DeckSerializer.from_base64_text(base64_text)

        uuid_len = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        uuid = _bytes[current_index:current_index + uuid_len].decode("utf-8")
        current_index += uuid_len

        vs_mode_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        vs_mode_as_text = ImmutableData.Misc.from_int(vs_mode_as_int)
        current_index += 1
        run_status_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        run_status_as_text = ImmutableData.Misc.from_int(run_status_as_int)
        current_index += 1
        utc_date_str_len = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        utc_date_str = _bytes[current_index:current_index + utc_date_str_len].decode("utf-8")
        current_index += utc_date_str_len
        animation_event_sequence = AnimationEventSequence.from_json(_json=_json["a"])
        state_set = StateSet.from_json(_json=_json["s"], snapshot_type_as_text=snapshot_type_as_text)

        player_decision_info_len = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        player_decision_info = None
        if player_decision_info_len > 0:
            player_decision_info_bytes = _bytes[current_index:current_index + player_decision_info_len]
            player_decision_info = PlayerDecisionInfoSerializer.from_bytes(player_decision_info_bytes)
        previous_luuid = _json["previous_luuid"]
        luuid = _json["luuid"]
        return ShopSnapshotSerializer(
            username=username,
            previous_luuid=previous_luuid,
            luuid=luuid,
            deck=deck,
            operation_count=operation_count,
            uuid=uuid,
            state_id=state_id,
            snapshot_type_as_int=snapshot_type_as_int,
            snapshot_type_as_text=snapshot_type_as_text,
            snapshot_sub_type_as_int=snapshot_sub_type_as_int,
            snapshot_sub_type_as_text=snapshot_sub_type_as_text,
            vs_mode_as_int=vs_mode_as_int,
            vs_mode_as_text=vs_mode_as_text,
            run_status_as_int=run_status_as_int,
            run_status_as_text=run_status_as_text,
            animation_event_sequence=animation_event_sequence,
            utc_date_str=utc_date_str,
            state_set=state_set,
            player_decision_info=player_decision_info
        )

    @staticmethod
    def start_new_run(deck: DeckSerializer, username: str, run_uuid: str = None) -> "ShopSnapshotSerializer":
        # here is where we would need to basically have the deck to even know what the
        # tier 1 objects were
        _uuid = uuid4().__str__()
        if run_uuid is not None:
            _uuid = run_uuid
        active_relics = []
        shop = []
        for x in range(GameConstants.Numbers.shop_object_count):
            obj = random_engine.get_random_shop_object(deck=deck, seed=_uuid, active_relics=active_relics,
                                                       snapshot=None)
            if obj.type == "Relic":
                active_relics.append(obj.sub_type_as_text)
            shop.append(obj)

        # every item must have a unique identifier, which means it needs to be scraped or stored in the data
        shop_id = 1
        for x in shop:
            x.shop_id = shop_id
            shop_id += 1

        friendly_recruits = [
            EmptySlotSerializer(team_index=0),
            EmptySlotSerializer(team_index=1),
            EmptySlotSerializer(team_index=2),
            EmptySlotSerializer(team_index=3),
            EmptySlotSerializer(team_index=4),
            EmptySlotSerializer(team_index=5),
            EmptySlotSerializer(team_index=6)
        ]
        for x in friendly_recruits:
            x.shop_id = shop_id
            shop_id += 1

        shop_state = ShopStateSerializer(
            wins=0,
            money=45,
            health=5,
            turn=1,
            operation_count=10,
            friendly_recruits=friendly_recruits,
            friendly_relics=[],
            shop=shop,
        )
        state_set = StateSet()
        state_id = state_set.add_state(shop_state)
        e = Animations.ShopStartOfTurn(state_id=state_id)
        animation_event_sequence = AnimationEventSequence()
        animation_event_sequence.append(animation=e)
        snapshot = ShopSnapshotSerializer(
            uuid=_uuid,
            state_id=state_id,
            vs_mode_as_int=5,
            vs_mode_as_text="custom_deck",
            deck=deck,
            username=username,
            snapshot_type_as_int=6,
            snapshot_type_as_text="ShopSnapshot",
            operation_count=10,
            run_status_as_int=3,
            run_status_as_text="pending",
            animation_event_sequence=animation_event_sequence,
            previous_luuid="None",
            luuid="None",
            state_set=state_set,
            utc_date_str=Date.UTC.now_str(),
            snapshot_sub_type_as_int=GameConstants.SnapshotSubTypes.Int.start_of_run,
            snapshot_sub_type_as_text=GameConstants.SnapshotSubTypes.String.start_of_run,
        )
        return snapshot

    def copy(self) -> "ShopSnapshotSerializer":
        return ShopSnapshotSerializer.from_json(self.to_json())

    @staticmethod
    def from_original_shop_state_and_latest_snapshot(
            original_shop_state: "ShopStateSerializer",
            latest_snapshot: "ShopSnapshotSerializer",
    ) -> "ShopSnapshotSerializer":
        new_state_set = StateSet()
        state_id = new_state_set.add_state(original_shop_state)
        return ShopSnapshotSerializer(
            username=latest_snapshot.username,
            uuid=latest_snapshot.uuid,
            state_id=state_id,
            vs_mode_as_int=latest_snapshot.vs_mode_as_int,
            vs_mode_as_text=latest_snapshot.vs_mode_as_text,
            deck=latest_snapshot.deck,
            snapshot_type_as_int=latest_snapshot.snapshot_type_as_int,
            snapshot_type_as_text=latest_snapshot.snapshot_type_as_text,
            operation_count=latest_snapshot.operation_count,
            run_status_as_int=latest_snapshot.run_status_as_int,
            run_status_as_text=latest_snapshot.run_status_as_text,
            animation_event_sequence=latest_snapshot.animation_event_sequence,
            utc_date_str=latest_snapshot.utc_date_str,
            previous_luuid=latest_snapshot.previous_luuid,
            luuid=latest_snapshot.luuid,
            state_set=new_state_set,
            player_decision_info=latest_snapshot.player_decision_info,
            snapshot_sub_type_as_int=None,
            snapshot_sub_type_as_text=None,
        )


if __name__ == "__main__":
    pass
