from typing import TYPE_CHECKING

from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.RandomEngine import random_engine
from zb7_game_engine.runtime.core.StackItem import StackItem
from zb7_game_engine.runtime.core.snapshots.ShopSnapshot import ShopSnapshot
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer
from zb7_game_engine.serialization.ShopSnapshotSerializer import ShopSnapshotSerializer
from zb7_game_engine.serialization.animation_events.Animations import Animations

if TYPE_CHECKING:
    from zb7_game_engine.serialization.ShopStateSerializer import ShopStateSerializer
    from zb7_game_engine.runtime.core.StateSet import StateSet


class Roll:
    @classmethod
    def stack_less_roll(cls,
                        shop_snapshot: ShopSnapshot,
                        animation_event_sequence: AnimationEventSequence):
        active_relics = [x.sub_type_as_text for x in shop_snapshot.friendly_relics]
        shop = []
        while len(shop) < GameConstants.Numbers.shop_object_count:
            shop_object = random_engine.get_random_shop_object(
                deck=shop_snapshot.deck,
                seed=shop_snapshot.uuid,
                active_relics=active_relics
            )
            if shop_object.type == "Relic":
                active_relics.append(shop_object.sub_type)
            shop.append(shop_object)
        if "MembershipCard" in [x.sub_type_as_text for x in shop_snapshot.friendly_relics]:
            for x in shop:
                x.cost = int(x.cost * 0.8)
        # e = AnimationEventSerializer(
        #     animation_type_as_text=GameConstants.Animations.shop_buy,
        #     state_id=state_set.add_state(shop_state)
        # )
        # animation_event_sequence.append(e)
        shop_snapshot.shop = shop

    @classmethod
    def update_shop_state(cls,
                          shop_snapshot: ShopSnapshotSerializer,
                          shop_state: "ShopStateSerializer",
                          state_set: "StateSet",
                          stack_item: StackItem,
                          animation_event_sequence: AnimationEventSequence):
        cost = GameConstants.Numbers.shop_roll_cost
        for x in shop_state.friendly_relics:
            if x.sub_type_as_text == "Dice" and x.custom_data["free_rolls"] > 0:
                x.custom_data["free_rolls"] -= 1
                cost = 0

        if shop_state.money - cost < 0:
            raise ValueError("Not enough money to buy")
        shop_state.money -= cost

        shop_state.queue_ability_for_all_objects(trigger=GameConstants.Opcodes.Shop.shop_roll, context={})
        active_relics = [x.sub_type_as_text for x in shop_state.friendly_relics]
        # add the shop_objects
        shop = []
        while len(shop) < GameConstants.Numbers.shop_object_count:
            shop_object = random_engine.get_random_shop_object(
                deck=shop_snapshot.deck,
                seed=shop_snapshot.uuid,
                active_relics=active_relics,
                snapshot=shop_state
            )
            if shop_object.type == "Relic":
                active_relics.append(shop_object.sub_type_as_text)
            shop_object.shop_id = shop_state.get_next_shop_id()
            shop.append(shop_object)
        # if "MemberShipCard" in [x.sub_type_as_text for x in shop_state.friendly_relics]:
        #     for x in shop:
        #         x.cost = int(x.cost * 0.8)
        shop_state.shop = shop
        e = Animations.ShopRoll(state_id=state_set.add_state(shop_state))
        animation_event_sequence.append(e)
        shop_state.queue_ability_for_all_objects(trigger=GameConstants.Opcodes.Shop.shop_roll, context={})

