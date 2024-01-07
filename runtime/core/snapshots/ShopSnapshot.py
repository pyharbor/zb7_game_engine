from uuid import uuid4
from pyharbor_shared_library.Date import Date

from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.StateSet import StateSet
from zb7_game_engine.runtime.objects.base.BasePlayerDecisionInfo import BasePlayerDecisionInfo
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer
from zb7_game_engine.serialization.ShopStateSerializer import ShopStateSerializer


class ShopSnapshot:
    def __init__(self,
                 uuid: str,
                 state_id: int,
                 vs_mode_as_int: int,
                 vs_mode_as_text: str,
                 deck: DeckSerializer,
                 username: str,
                 snapshot_type_as_int: int,
                 snapshot_type_as_text: str,
                 snapshot_sub_type_as_int: int,
                 snapshot_sub_type_as_text: str,
                 operation_count: int = 0,
                 run_status_as_int: int = None,
                 run_status_as_text: str = None,
                 animation_event_sequence: AnimationEventSequence = None,
                 previous_luuid: str = None,
                 luuid: str = None,
                 state_set: "StateSet" = None,
                 utc_date_str: str = None,
                 player_decision_info: BasePlayerDecisionInfo = None):
        if uuid is None:
            uuid = uuid4().__str__()
        self.username = username
        self.previous_luuid = previous_luuid
        self.luuid = luuid
        self.deck = deck
        self.operation_count = operation_count
        self.uuid = uuid
        self.state_id = state_id
        self.snapshot_type_as_int = snapshot_type_as_int
        self.snapshot_type_as_text = snapshot_type_as_text
        self.snapshot_sub_type_as_int = snapshot_sub_type_as_int
        self.snapshot_sub_type_as_text = snapshot_sub_type_as_text
        self.vs_mode_as_int = vs_mode_as_int
        self.vs_mode_as_text = vs_mode_as_text
        self.run_status_as_int = run_status_as_int
        self.run_status_as_text = run_status_as_text

        if animation_event_sequence is None:
            animation_event_sequence = AnimationEventSequence()
        self.animation_event_sequence = animation_event_sequence
        self.utc_date_str = utc_date_str or Date.UTC.now_str()
        self.state_set: StateSet = state_set
        self.player_decision_info = player_decision_info
        self.current_state: ShopStateSerializer = self.state_set.get_state_by_state_id(self.state_id)

        # copied from the state
        self.wins = self.current_state.wins
        self.money = self.current_state.money
        self.health = self.current_state.health
        self.turn = self.current_state.turn
        self.friendly_recruits = self.current_state.friendly_recruits
        self.friendly_relics = self.current_state.friendly_relics


if __name__ == "__main__":
    pass
