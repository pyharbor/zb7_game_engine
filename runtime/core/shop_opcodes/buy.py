from typing import TYPE_CHECKING

from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.StackItem import StackItem
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer
from zb7_game_engine.serialization.EmptySlotSerializer import EmptySlotSerializer
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer
from zb7_game_engine.serialization.animation_events.Animations import Animations

if TYPE_CHECKING:
    from zb7_game_engine.serialization.ShopStateSerializer import ShopStateSerializer
    from zb7_game_engine.runtime.core.StateSet import StateSet


class Buy:
    @classmethod
    def update_shop_state(cls,
                          shop_state: "ShopStateSerializer",
                          state_set: "StateSet",
                          stack_item: StackItem,
                          animation_event_sequence: AnimationEventSequence,
                          shop_snapshot: "ShopSnapshotSerializer" = None):
        user_input = stack_item.context
        shop_index = None
        for i, x in enumerate(shop_state.shop):
            if x.shop_id == user_input.shop_object.shop_id:
                shop_index = i
                break

        if shop_index is None:
            raise ValueError("Shop entity does not exist")
        shop_object = shop_state.shop[shop_index]
        if isinstance(shop_object, EmptySlotSerializer):
            raise ValueError("Cannot buy EmptySlot")
        if shop_state.money - shop_object.cost < 0:
            raise ValueError(f"Not enough money to buy, money={shop_state.money} cost={shop_object.cost}")

        # add the pet to the team or merge it with an existing pet
        if shop_object.type == "Recruit":
            team_match = shop_state.get_object_from_shop_id(shop_id=user_input.team_object.shop_id)
            if team_match is None:
                raise ValueError("Team entity does not exist")

            if isinstance(team_match, EmptySlotSerializer) and isinstance(shop_object, RecruitSerializer):
                shop_state.replace_empty_slot(recruit=shop_object, recruit_index=team_match.team_index)
                shop_state.queue_ability_for_all_objects(trigger=GameConstants.Opcodes.Shop.shop_friendly_recruit_summoned,
                                                         context={"target": shop_object})
                shop_state.money -= shop_object.cost
                shop_state.shop[shop_index] = EmptySlotSerializer(shop_id=shop_state.get_next_shop_id())
                e = Animations.ShopBuy(state_id=state_set.add_state(shop_state))
                animation_event_sequence.append(e)
            elif not isinstance(team_match, EmptySlotSerializer) and isinstance(shop_object, RecruitSerializer):
                raise ValueError("Cannot buy a pet in that slot, already filled")
            shop_state.queue_ability_for(objects=[shop_object], trigger=GameConstants.Opcodes.Shop.shop_bought)

        elif shop_object.type == "Relic":
            shop_state.add_relic(shop_object)
            shop_object: RelicSerializer
            # shop_state.queue_ability_for(objects=[shop_object], trigger=GameConstants.Opcodes.Shop.consumable_relic)
            shop_state.money -= shop_object.cost
            shop_state.shop[shop_index] = EmptySlotSerializer(shop_id=0)
            e = Animations.ShopBuy(state_id=state_set.add_state(shop_state))
            animation_event_sequence.append(e)
            shop_state.queue_ability_for(objects=[shop_object], trigger=GameConstants.Opcodes.Shop.shop_bought)