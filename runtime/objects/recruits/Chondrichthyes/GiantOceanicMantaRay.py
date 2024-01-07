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


class GiantOceanicMantaRay(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=59,
                         sub_type_as_text="GiantOceanicMantaRay", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------
        if "consumption_counter" not in self.custom_data:
            self.custom_data["consumption_counter"] = 0
        self.consumption_counter = self.custom_data["consumption_counter"]

        
    def shop_start_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                           animation_event_sequence: AnimationEventSequence,
                           shop_snapshot: "ShopSnapshotSerializer" = None):
        krill = [x for x in shop_state.friendly_recruits if
                 x.sub_type_as_text == "Krill" and x.team_index < self.team_index]
        if len(krill) == 0:
            return
        target_krill = krill[-1]

        e = Animations.Swallow(state_id=state_set.add_state(shop_state),
                               battle_id=target_krill.battle_id,
                               shop_id=target_krill.shop_id,
                               target_shop_id=target_krill.shop_id,
                               target_battle_id=target_krill.battle_id)
        animation_event_sequence.append(e)

        target_krill.shop_faint(shop_state=shop_state,
                                state_set=state_set,
                                stack_item=stack_item,
                                animation_event_sequence=animation_event_sequence,
                                original_shop_state=shop_snapshot)

        e = Animations.Consume(state_id=state_set.add_state(shop_state),
                               battle_id=self.battle_id,
                               shop_id=self.shop_id,
                               target_shop_id=target_krill.shop_id,
                               target_battle_id=target_krill.battle_id)
        animation_event_sequence.append(e)
        self.consumption_counter += 1
        self.custom_data["consumption_counter"] = self.consumption_counter
        boost = self.consumption_counter + 2

        g = Group()
        for x in shop_state.friendly_recruits:
            if GameConstants.Habitats.OpenOcean in x.binomial_nomenclature:
                x.shop_buff_stats(
                    shop_state=shop_state,
                    state_set=state_set,
                    animation_event_sequence=animation_event_sequence,
                    stack_item=stack_item,
                    melee=boost-1,
                    ranged=boost-1,
                    health=boost+2,
                    max_health=boost+2,
                    group=g
                )

        g.set_state_id(state_id=state_set.add_state(state=shop_state))
        animation_event_sequence.append(g)

    def custom_data_to_bytes(self) -> bytes:
        return Uint8Counter.custom_data_to_bytes(self, key="consumption_counter")

    @classmethod
    def bytes_to_custom_data(cls, _bytes: bytes, current_index: int) -> dict:
        return Uint8Counter.bytes_to_custom_data(_bytes=_bytes, current_index=current_index, key="consumption_counter")

    def passive_battle_ability(self,
                               battle_state: "BattleStateSerializer",
                               state_set: StateSet,
                               stack_item: "StackItem",
                               animation_event_sequence: AnimationEventSequence,
                               original_shop_state: "ShopStateSerializer" = None):
        for x in self.listeners.get_listeners(hook=Listeners.Hooks.passive_battle_ability):
            # basically we allow arbitrary other objects to affect the 'fainting' of a unit
            # if that unit is revived it doesn't actually need to faint and thus returns immediately
            should_return = x.lt_passive_battle_ability(
                battle_state=battle_state,
                state_set=state_set,
                stack_item=stack_item,
                animation_event_sequence=animation_event_sequence,
                original_shop_state=original_shop_state
            )
            if should_return:
                return
        if self.get_logical_level() >= 3:
            info = battle_state.get_battle_info(battle_id=self.battle_id)
            krill = [x for x in info.friendly_recruits if
                     x.sub_type_as_text == "Krill"]
            self.generic_ability_notification(
                state=battle_state,
                state_set=state_set,
                animation_event_sequence=animation_event_sequence)
            g = Group()
            for x in krill:
                s = Statuses.Protected(counter=2)
                x.add_status(status=s,
                             battle_state=battle_state,
                             state_set=state_set,
                             enemy=None,
                             original_shop_state=original_shop_state,
                             animation_event_sequence=animation_event_sequence,
                             group=g)

            g.set_state_id(state_id=state_set.add_state(state=battle_state))
            animation_event_sequence.append(g)

