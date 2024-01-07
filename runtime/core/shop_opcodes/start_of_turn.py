from typing import TYPE_CHECKING

from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.RandomEngine import random_engine
from zb7_game_engine.runtime.core.StackItem import StackItem
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer
from zb7_game_engine.serialization.EmptySlotSerializer import EmptySlotSerializer
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer
from zb7_game_engine.serialization.animation_events.Animations import Animations

if TYPE_CHECKING:
    from zb7_game_engine.serialization.ShopStateSerializer import ShopStateSerializer
    from zb7_game_engine.runtime.core.StateSet import StateSet
    from zb7_game_engine.serialization.ShopSnapshotSerializer import ShopSnapshotSerializer


class StartOfTurn:
    @classmethod
    def update_shop_state(cls,
                          shop_snapshot: "ShopSnapshotSerializer",
                          shop_state: "ShopStateSerializer",
                          state_set: "StateSet",
                          stack_item: StackItem,
                          animation_event_sequence: AnimationEventSequence):
        user_input = stack_item.context

        shop_state.turn += 1
        e = Animations.ShopStartOfTurn(state_id=state_set.add_state(shop_state))
        animation_event_sequence.append(e)
        shop_state.money += 15
        e = Animations.ShopGainMoney(state_id=state_set.add_state(shop_state))
        animation_event_sequence.append(e)

        active_relics = [x.sub_type_as_text for x in shop_state.friendly_relics]
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
        if "MembershipCard" in [x.sub_type_as_text for x in shop_state.friendly_relics]:
            for x in shop:
                x.cost = int(x.cost * 0.8)
        shop_state.shop = shop
        e = Animations.ShopRoll(state_id=state_set.add_state(shop_state))
        animation_event_sequence.append(e)
        shop_state.queue_ability_for_all_objects(trigger=GameConstants.Opcodes.Shop.shop_start_of_turn, context={})

        gain_experience_group = Animations.Group()
        level_up_group = Animations.Group()

        # custom stuff hereÂ
        for x in shop_state.friendly_recruits:
            if isinstance(x, EmptySlotSerializer):
                continue
            x.experience += 1
            shop_state.queue_ability_for(trigger=GameConstants.Opcodes.Shop.shop_gain_experience,
                                         objects=[x],
                                         context={})
            e = Animations.ShopGainExperience(amount=1, shop_id=x.shop_id,
                                              battle_id=x.battle_id,
                                              state_id=None)
            gain_experience_group.add_animation_event(e)
            if x.experience in GameConstants.Levels.all:
                e = Animations.ShopLevelUp(amount=1, shop_id=x.shop_id, battle_id=x.battle_id, state_id=None)
                level_up_group.add_animation_event(e)
                shop_state.queue_ability_for(objects=[x],
                                             trigger=GameConstants.Opcodes.Shop.shop_level_up,
                                             context={"recruit": x})
        gain_experience_group.set_state_id(state_set.add_state(shop_state))
        level_up_group.set_state_id(state_set.add_state(shop_state))
        if len(gain_experience_group.animation_events) > 0:
            animation_event_sequence.append(gain_experience_group)
        if len(level_up_group.animation_events) > 0:
            animation_event_sequence.append(level_up_group)
