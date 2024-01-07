from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.Deck import Deck
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.StateSet import StateSet
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer
from zb7_game_engine.serialization.ShopStateSerializer import ShopStateSerializer


class BattleSnapshot:
    def __init__(self,
                 friendly_uuid: str,
                 friendly_deck: DeckSerializer,
                 friendly_username: str,
                 friendly_wins: int,
                 friendly_health: int,
                 friendly_money: int,
                 friendly_turn: int,
                 friendly_utc_date_str: str,
                 friendly_run_status_as_int: int,
                 friendly_run_status_as_text: str,
                 enemy_uuid: str,
                 enemy_deck: DeckSerializer,
                 enemy_username: str,
                 enemy_wins: int,
                 enemy_health: int,
                 enemy_money: int,
                 enemy_turn: int,
                 enemy_utc_date_str: str,
                 enemy_run_status_as_int: int,
                 enemy_run_status_as_text: str,
                 vs_mode_as_int: int,
                 vs_mode_as_text: str,
                 operation_count: int,
                 animation_event_sequence: AnimationEventSequence,
                 state_set: "StateSet",
                 battle_result_as_int: int,
                 snapshot_sub_type_as_int: int,
                 snapshot_sub_type_as_text: str,
                 original_shop_state: "ShopStateSerializer" = None,
                 previous_luuid: str = None,
                 luuid: str = None
                 ):
        self.friendly_uuid = friendly_uuid
        self.friendly_deck = friendly_deck
        self.friendly_username = friendly_username
        self.friendly_wins = friendly_wins
        self.friendly_health = friendly_health
        self.friendly_money = friendly_money
        self.friendly_turn = friendly_turn
        self.friendly_utc_date_str = friendly_utc_date_str
        self.friendly_run_status_as_int = friendly_run_status_as_int
        self.friendly_run_status_as_text = friendly_run_status_as_text
        self.enemy_uuid = enemy_uuid
        self.enemy_deck = enemy_deck
        self.enemy_username = enemy_username
        self.enemy_wins = enemy_wins
        self.enemy_health = enemy_health
        self.enemy_money = enemy_money
        self.enemy_turn = enemy_turn
        self.enemy_utc_date_str = enemy_utc_date_str
        self.enemy_run_status_as_int = enemy_run_status_as_int
        self.enemy_run_status_as_text = enemy_run_status_as_text
        self.vs_mode_as_int = vs_mode_as_int
        self.vs_mode_as_text = vs_mode_as_text
        self.snapshot_type_as_text = "BattleSnapshot"
        self.snapshot_type_as_int = ImmutableData.Misc.from_text(subtype_as_text=self.snapshot_type_as_text)
        self.snapshot_sub_type_as_int = snapshot_sub_type_as_int
        self.snapshot_sub_type_as_text = snapshot_sub_type_as_text
        self.operation_count = operation_count
        self.animation_event_sequence = animation_event_sequence
        self.previous_luuid = previous_luuid
        self.luuid = luuid
        self.state_set = state_set
        self.battle_result_as_int = battle_result_as_int
        self.original_shop_state = original_shop_state


if __name__ == "__main__":
    pass
