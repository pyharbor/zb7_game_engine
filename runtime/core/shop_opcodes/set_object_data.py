from typing import TYPE_CHECKING

from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.StackItem import StackItem
from zb7_game_engine.runtime.core.shop_opcodes.ShopUserInput import ShopUserInput
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer
from zb7_game_engine.serialization.animation_events.Animations import Animations

if TYPE_CHECKING:
    from zb7_game_engine.serialization.ShopStateSerializer import ShopStateSerializer
    from zb7_game_engine.runtime.core.StateSet import StateSet
    from zb7_game_engine.serialization.ShopSnapshotSerializer import ShopSnapshotSerializer


class SetObjectData:
    @classmethod
    def update_shop_state(cls,
                          shop_state: "ShopStateSerializer",
                          state_set: "StateSet",
                          stack_item: StackItem,
                          animation_event_sequence: AnimationEventSequence,
                          original_shop_snapshot: "ShopSnapshotSerializer"):
        user_input: ShopUserInput = stack_item.context
        found = False
        for x in shop_state.objects_by_shop_id.values():
            if x.shop_id == user_input.team_object.shop_id:
                x.shop_set_object_data(shop_state=shop_state,
                                       state_set=state_set,
                                       stack_item=stack_item,
                                       user_input=user_input,
                                       animation_event_sequence=animation_event_sequence,
                                       original_shop_snapshot=original_shop_snapshot)
                found = True
                break
        e = Animations.SetObjectData(state_id=state_set.add_state(shop_state))
        animation_event_sequence.append(e)
        if not found:
            raise ValueError("Team entity does not exist")
