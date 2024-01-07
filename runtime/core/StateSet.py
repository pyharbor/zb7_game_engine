import json
from typing import List, Union

from zb7_game_engine.runtime.core.states.BattleState import BattleState
from zb7_game_engine.runtime.core.states.ShopState import ShopState
from zb7_game_engine.serialization.BattleStateSerializer import BattleStateSerializer
from zb7_game_engine.serialization.ShopStateSerializer import ShopStateSerializer


class StateSet:
    def __init__(self):
        self._state_set_by_json_content: dict[str, int] = {}
        self._state_set_by_state_id: dict[int, dict] = {}
        self.state_id = 0

    def add_state(self, state: Union[ShopStateSerializer, BattleStateSerializer]) -> int:
        json_str = json.dumps(state.to_json())
        if json_str not in self._state_set_by_json_content:
            self.state_id += 1
            self._state_set_by_json_content[json_str] = self.state_id
            self._state_set_by_state_id[self.state_id] = state.to_json()
        return self.state_id

    def get_state_by_state_id(self, state_id: int, _type: str = "ShopSnapshot") -> Union[ShopStateSerializer, BattleStateSerializer]:
        if _type == 'ShopSnapshot':
            return ShopStateSerializer.from_json(self._state_set_by_state_id[state_id])
        elif _type == 'BattleSnapshot':
            return BattleStateSerializer.from_json(self._state_set_by_state_id[state_id])

    def to_json(self):
        return self._state_set_by_state_id

    @staticmethod
    def from_json(_json, snapshot_type_as_text: str):
        states = StateSet()
        max_state_id = 0
        for state_id, state in _json.items():
            if isinstance(state_id, str):
                state_id = int(state_id)
            max_state_id = max(max_state_id, state_id)
            if snapshot_type_as_text == 'ShopSnapshot':
                states._state_set_by_state_id[state_id] = state
            elif snapshot_type_as_text == 'BattleSnapshot':
                states._state_set_by_state_id[state_id] = state
        states.state_id = max_state_id + 1
        return states


if __name__ == '__main__':
    print('Hello World')