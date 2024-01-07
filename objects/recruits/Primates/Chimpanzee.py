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


class Chimpanzee(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=87,
                         sub_type_as_text="Chimpanzee", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------
        self.target = self.custom_data.get("target", None)

        
    @classmethod
    def bytes_to_custom_data(cls, _bytes: bytes, current_index: int) -> dict:
        return ShopIDTarget.bytes_to_custom_data(_bytes=_bytes, current_index=current_index)

    def custom_data_to_bytes(self) -> bytes:
        return ShopIDTarget.custom_data_to_bytes(self)

    def shop_set_object_data(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                             user_input: "ShopUserInput", animation_event_sequence: AnimationEventSequence,
                             original_shop_snapshot: "ShopSnapshotSerializer" = None):
        if user_input.set_shop_object_data_opcode == GameConstants.Opcodes.ObjectData.shop_set_custom:
            if user_input.target_object is None:
                raise Exception("No target object provided")

            team_match = shop_state.get_object_from_shop_id(shop_id=int(user_input.target_object))
            if team_match is None:
                raise ValueError("Target entity does not exist")

            if GameConstants.ScientificNames.Primates not in team_match.binomial_nomenclature:
                raise ValueError("Target entity is not a primate")

            else:
                self.custom_data["target"] = team_match.shop_id
                self.target = team_match.shop_id
                e = Animations.ShopUpdatedRecruit(shop_id=self.shop_id,
                                                  state_id=state_set.add_state(shop_state),
                                                  battle_id=self.battle_id)
                animation_event_sequence.append(e)
        else:
            super().shop_set_object_data(shop_state=shop_state, state_set=state_set,
                                         stack_item=stack_item, user_input=user_input,
                                         animation_event_sequence=animation_event_sequence)

    def shop_end_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                         animation_event_sequence: AnimationEventSequence,
                         shop_snapshot: "ShopSnapshotSerializer" = None):
        super().shop_end_of_turn(shop_state, state_set, stack_item, animation_event_sequence)
        self.generic_ability_notification(state=shop_state, state_set=state_set,
                                          description=self.ability[0].name,
                                          animation_event_sequence=animation_event_sequence)
        if self.target is not None:
            target_match = shop_state.get_object_from_shop_id(shop_id=self.target)
            if target_match is not None:
                if self.experience < GameConstants.Levels.level_2:
                    buff = 4
                elif self.experience < GameConstants.Levels.level_3:
                    buff = 6
                else:
                    buff = 8
                target_match.shop_buff_stats(melee=buff,
                                             ranged=buff,
                                             initiative=buff,
                                             shop_state=shop_state,
                                             state_set=state_set,
                                             stack_item=stack_item, buffer=self,
                                             animation_event_sequence=animation_event_sequence)

    def shop_friendly_recruit_sold(self, shop_state: "ShopStateSerializer",
                                   state_set: "StateSet",
                                   stack_item: "StackItem",
                                   animation_event_sequence: AnimationEventSequence,
                                   original_run_snapshot: "ShopSnapshotSerializer" = None):
        target = stack_item.context["target"]
        if target.shop_id == self.custom_data["target"]:
            self.custom_data["target"] = None
            self.target = None

