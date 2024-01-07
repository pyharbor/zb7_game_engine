from typing import TYPE_CHECKING

from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.StackItem import StackItem
from zb7_game_engine.runtime.objects.recruits.EmptySlot.EmptySlot import EmptySlot
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer
from zb7_game_engine.serialization.animation_events.Animations import Animations

if TYPE_CHECKING:
    from zb7_game_engine.serialization.ShopStateSerializer import ShopStateSerializer
    from zb7_game_engine.runtime.core.StateSet import StateSet
    from zb7_game_engine.serialization.ShopSnapshotSerializer import ShopSnapshotSerializer


class PlayerDecision:
    @classmethod
    def update_shop_state(cls,
                          shop_state: "ShopStateSerializer",
                          state_set: "StateSet",
                          stack_item: StackItem,
                          animation_event_sequence: AnimationEventSequence,
                          original_run_snapshot: "ShopSnapshotSerializer"):
        target_shop_id = original_run_snapshot.player_decision_info.shop_id
        object_match = None
        objects = []
        objects.extend(shop_state.friendly_recruits)
        objects.extend(shop_state.friendly_relics)
        for x in objects:
            if x.shop_id == target_shop_id:
                object_match = x
                break

        object_match.shop_player_decision(shop_state=shop_state,state_set=state_set, stack_item=stack_item,
                                          animation_event_sequence=animation_event_sequence,
                                          original_run_snapshot=original_run_snapshot)
        shop_state.snapshot_type = GameConstants.SnapshotTypes.shop_default