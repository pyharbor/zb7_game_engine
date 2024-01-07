from typing import List

from collections import deque        
from zb7_game_engine.runtime.objects.statuses.Statuses import Statuses
from zb7_game_engine.serialization.animation_events.G.Group import Group
from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature
from zb7_game_engine.runtime.objects.base.BaseRecruit import BaseRecruit
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.StateSet import StateSet
from typing import List, TYPE_CHECKING, Union
from zb7_game_engine.runtime.core.StackItem import StackItem
from zb7_game_engine.serialization.animation_events.Animations import Animations
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.Listeners import Listeners
from zb7_game_engine.runtime.core.RandomEngine import random_engine
from zb7_game_engine.serialization.EmptySlotSerializer import EmptySlotSerializer
from zb7_game_engine.serialization.shared.custom_data.ShopIDTarget import ShopIDTarget
from zb7_game_engine.serialization.shared.custom_data.Uint8ArrayOfScientificNomenclature import Uint8ArrayOfScientificNomenclature
from zb7_game_engine.serialization.shared.custom_data.Uint8Counter import Uint8Counter
from zb7_game_engine.serialization.shared.custom_data.Uint16Counter import Uint16Counter
from zb7_game_engine.runtime.objects.relics.Relics import Relics
from zb7_game_engine.serialization.shared.custom_data.CarpenterAntCD import CarpenterAntCD
from zb7_game_engine.serialization.shared.custom_data.SeaOtterCD import SeaOtterCD


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


class SeaOtter(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=67,
                         sub_type_as_text="SeaOtter", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------
        self.valid_subtypes_as_text = [
            "BeardedSeal",
            "CrabEaterSeal",
            "ElephantSeal",
            "FurSeal",
            "HarpSeal",
            "LepoardSeal",
            "SeaOtter",
            "SouthAmericanSeaLion",
            "Walrus",
        ]
        if "trigger" not in self.custom_data:
            self.custom_data["trigger"] = 1

        
    def shop_start_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                           animation_event_sequence: AnimationEventSequence,
                           shop_snapshot: "ShopSnapshotSerializer" = None):
        self.generic_ability_notification(
            state=shop_state,
            state_set=state_set,
            animation_event_sequence=animation_event_sequence)
        g1 = Group()
        g2 = Group()
        for sub_type_as_text, v in self.custom_data.items():
            if sub_type_as_text == "trigger":
                continue
            for x in shop_state.friendly_recruits:
                if x.sub_type_as_text == sub_type_as_text:
                    amount = v['experience']
                    before_level = x.get_logical_level()
                    x.experience += amount
                    e = Animations.ShopGainExperience(
                        shop_id=x.shop_id,
                        amount=amount,
                        battle_id=self.battle_id,
                        state_id=None
                    )
                    g1.add_animation_event(e)
                    shop_state.queue_ability_for(trigger=GameConstants.Opcodes.Shop.shop_gain_experience,
                                                 objects=[x],
                                                 context={})
                    after_level = x.get_logical_level()
                    if after_level > before_level:
                        e = Animations.ShopLevelUp(
                            shop_id=x.shop_id,
                            amount=amount,
                            battle_id=x.battle_id,
                            state_id=None
                        )
                        g2.add_animation_event(e)
                        shop_state.queue_ability_for(objects=[x],
                                                     trigger=GameConstants.Opcodes.Shop.shop_level_up,
                                                     context={"recruit": x})
        if len(g1.animation_events) > 0:
            g1.set_state_id(state_id=state_set.add_state(shop_state))
            animation_event_sequence.append(g1)
        if len(g2.animation_events) > 0:
            g2.set_state_id(state_id=state_set.add_state(shop_state))
            animation_event_sequence.append(g2)

    @classmethod
    def bytes_to_custom_data(cls, _bytes: bytes, current_index: int) -> dict:
        return SeaOtterCD.bytes_to_custom_data(_bytes, current_index)

    def custom_data_to_bytes(self) -> bytes:
        return SeaOtterCD.custom_data_to_bytes(self)

    def shop_set_object_data(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                             user_input: "ShopUserInput", animation_event_sequence: AnimationEventSequence,
                             original_shop_snapshot: "ShopSnapshotSerializer" = None):
        if user_input.set_shop_object_data_opcode == GameConstants.Opcodes.ObjectData.shop_set_custom:
            if self.custom_data['trigger'] == 0:
                raise Exception("This ability has already been triggered, wait until the next level-up to use it again")

            sub_type_as_text = user_input.player_decision_choice['sub_type_as_text']
            if self.experience < GameConstants.Levels.level_2:
                buff = 1
            elif self.experience < GameConstants.Levels.level_3:
                buff = 2
            else:
                buff = 3


            if sub_type_as_text is None:
                raise Exception("Must supply a sub_type_as_text")

            if sub_type_as_text not in self.valid_subtypes_as_text:
                raise ValueError("Invalid sub_type_as_text, must be a valid 'Pinipedia' sub-species")
            if sub_type_as_text not in self.custom_data:
                self.custom_data[sub_type_as_text] = {"experience": 0}
            self.custom_data[sub_type_as_text]["experience"] += buff
            self.custom_data['trigger'] = 0
            e = Animations.ShopUpdatedRecruit(
                state_id=state_set.add_state(shop_state),
                shop_id=self.shop_id,
                battle_id=self.battle_id
            )
            animation_event_sequence.append(e)

        else:
            super().shop_set_object_data(shop_state=shop_state, state_set=state_set,
                                         stack_item=stack_item, user_input=user_input,
                                         animation_event_sequence=animation_event_sequence)

    def shop_level_up(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                      animation_event_sequence: AnimationEventSequence):
        logical_level = self.get_logical_level()
        if logical_level <= 4:
            self.custom_data["trigger"] = 1
            e = Animations.ShopUpdatedRecruit(
                state_id=state_set.add_state(shop_state),
                shop_id=self.shop_id,
                battle_id=self.battle_id
            )
            animation_event_sequence.append(e)

