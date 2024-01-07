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


class Sell:
    @classmethod
    def update_shop_state(cls,
                          shop_state: "ShopStateSerializer",
                          state_set: "StateSet",
                          stack_item: StackItem,
                          animation_event_sequence: AnimationEventSequence):

        user_input = stack_item.context
        team_match = shop_state.get_object_from_shop_id(shop_id=user_input.team_object.shop_id)
        if team_match is None:
            raise ValueError("Team entity does not exist")

        # remove the pet to prevent sell effects hitting it
        shop_state.revert_to_empty_slot(recruit_index=team_match.team_index)
        amount = 3
        shop_state.money += amount
        e = Animations.ShopSell(state_id=state_set.add_state(shop_state))
        animation_event_sequence.append(e)
        shop_state.queue_ability_for(objects=[user_input.team_object], trigger=GameConstants.Opcodes.Shop.shop_sold)
        shop_state.queue_ability_for_all_objects(trigger=GameConstants.Opcodes.Stack.shop_friendly_recruit_sold,
                                                 context={'target': team_match})

        animation_event_sequence.append(e)
