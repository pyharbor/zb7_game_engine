from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from collections import defaultdict
from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature
from zb7_game_engine.runtime.objects.base.BaseRecruit import BaseRecruit
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus
from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.StateSet import StateSet
from typing import List, TYPE_CHECKING, Union
from zb7_game_engine.runtime.core.StackItem import StackItem
from zb7_game_engine.serialization.animation_events.Animations import Animations
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer
from zb7_game_engine.runtime.core.Listeners import Listeners
from zb7_game_engine.serialization.animation_events.Animations import Animations
from zb7_game_engine.runtime.core.RandomEngine import random_engine
from zb7_game_engine.serialization.animation_events.G.Group import Group
from zb7_game_engine.runtime.objects.statuses.Statuses import Statuses
from zb7_game_engine.serialization.shared.custom_data.ShopIDTarget import ShopIDTarget
from zb7_game_engine.runtime.core.ObjectParser import ObjectParser
from zb7_game_engine.serialization.shared.custom_data.SuperNestCD import SuperNestCD
from zb7_game_engine.serialization.shared.custom_data.Rewards import Rewards


if TYPE_CHECKING:
    from zb7_game_engine.serialization.ShopStateSerializer import ShopStateSerializer
    from zb7_game_engine.serialization.BattleStateSerializer import BattleStateSerializer
    from zb7_game_engine.runtime.core.StackItem import StackItem
    from zb7_game_engine.runtime.core.StateSet import StateSet
    from zb7_game_engine.runtime.core.shop_opcodes.ShopUserInput import ShopUserInput
    from zb7_game_engine.serialization.BattleSnapshotSerializer import BattleSnapshotSerializer
    from zb7_game_engine.serialization.ShopSnapshotSerializer import ShopSnapshotSerializer
    from zb7_game_engine.serialization.RelicSerializer import RelicSerializer
    from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
    from zb7_game_engine.serialization.StatusSerializer import StatusSerializer


class TreasureChest(RelicSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=196,
                         sub_type_as_text="TreasureChest", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------
        if "rewards" not in self.custom_data:
            self.custom_data = {"rewards": []}

        
    def shop_bought(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                    animation_event_sequence: AnimationEventSequence,
                    shop_snapshot: "ShopSnapshotSerializer" = None):
        rewards = []
        active_relics = [x.sub_type_as_text for x in shop_snapshot.friendly_relics]
        for x in range(5):
            reward_object = random_engine.get_random_shop_object(
                deck=shop_snapshot.deck,
                seed=shop_snapshot.uuid,
                active_relics=active_relics,
                filter_callback=lambda x: x.rarity == "Rare",
                snapshot=shop_snapshot
            )
            if reward_object.type == "Relic":
                active_relics.append(reward_object.sub_type_as_text)
            reward_object.shop_id = shop_state.get_next_shop_id()
            rewards.append(reward_object)
        self.custom_data["rewards"] = rewards
        self.generic_ability_notification(state=shop_state, state_set=state_set,
                                          animation_event_sequence=animation_event_sequence)

    @classmethod
    def bytes_to_custom_data(cls, _bytes: bytes, current_index: int) -> dict:
        return Rewards.bytes_to_custom_data(_bytes=_bytes, current_index=current_index)

    def custom_data_to_bytes(self) -> bytes:
        return Rewards.custom_data_to_bytes(self)

    def shop_set_object_data(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                             user_input: "ShopUserInput", animation_event_sequence: AnimationEventSequence,
                             original_shop_snapshot: "ShopSnapshotSerializer" = None):
        if user_input.set_shop_object_data_opcode == GameConstants.Opcodes.ObjectData.shop_set_custom:
            if len(self.custom_data["rewards"]) == 0:
                raise Exception("Reward has already been claimed")
            if user_input.target_object is None:
                raise Exception("No target object provided")
            reward_match = None
            for x in self.custom_data["rewards"]:
                if int(user_input.target_object) == x.shop_id:
                    reward_match = x

            if reward_match is None:
                raise Exception("Target object not found")

            else:
                cost = reward_match.cost
                rebate = 45 - cost
                if reward_match.type == "Relic":
                    shop_state.money += rebate
                    reward_match.shop_bought(
                        shop_state=shop_state,
                        state_set=state_set,
                        stack_item=stack_item,
                        animation_event_sequence=animation_event_sequence,
                        shop_snapshot=original_shop_snapshot
                    )
                    shop_state.add_relic(relic=reward_match)
                    self.custom_data["rewards"] = []
                    self.generic_ability_notification(state=shop_state, state_set=state_set,
                                                      animation_event_sequence=animation_event_sequence)
                    return
                elif reward_match.type == "Recruit":
                    for x in shop_state.friendly_recruits:
                        if x.type == "EmptySlot":
                            shop_state.add_recruit(recruit=reward_match, index=x.team_index)
                            self.custom_data["rewards"] = []
                            shop_state.money += rebate
                            self.generic_ability_notification(state=shop_state, state_set=state_set,
                                                              animation_event_sequence=animation_event_sequence)
                            shop_state.queue_ability_for_all_objects(
                                trigger=GameConstants.Opcodes.Shop.shop_friendly_recruit_summoned,
                                context={"target": reward_match})
                            return
                    raise Exception("There is not room on your team to add reward, sell something first")
        else:
            super().shop_set_object_data(shop_state=shop_state, state_set=state_set,
                                         stack_item=stack_item, user_input=user_input,
                                         animation_event_sequence=animation_event_sequence)

