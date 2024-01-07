from typing import TYPE_CHECKING

from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.StackItem import StackItem
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer
from zb7_game_engine.serialization.animation_events.Animations import Animations

if TYPE_CHECKING:
    from zb7_game_engine.serialization.ShopStateSerializer import ShopStateSerializer
    from zb7_game_engine.runtime.core.StateSet import StateSet


class Move:
    @classmethod
    def update_shop_state(cls,
                          shop_state: "ShopStateSerializer",
                          state_set: "StateSet",
                          stack_item: StackItem,
                          animation_event_sequence: AnimationEventSequence):
        user_input = stack_item.context
        team_match_1: RecruitSerializer = shop_state.get_object_from_shop_id(shop_id=user_input.team_object_1.shop_id)
        team_match_2: RecruitSerializer = shop_state.get_object_from_shop_id(shop_id=user_input.team_object_2.shop_id)
        if team_match_1 is None:
            raise ValueError("Team entity does not exist")
        if team_match_2 is None:
            raise ValueError("Team entity does not exist")
        if team_match_1.shop_id == team_match_2.shop_id:
            raise ValueError("Cannot move team entity without two different instances, received the same uuid for both")
        team_index_1 = team_match_1.team_index
        team_index_2 = team_match_2.team_index
        team_match_1.team_index = team_index_2
        team_match_2.team_index = team_index_1
        shop_state.friendly_recruits[team_index_1] = team_match_2
        shop_state.friendly_recruits[team_index_2] = team_match_1
        e = Animations.ShopMove(state_id=state_set.add_state(shop_state))
        animation_event_sequence.append(e)
