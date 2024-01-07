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


class Krill(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=48,
                         sub_type_as_text="Krill", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def shop_start_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                           animation_event_sequence: AnimationEventSequence,
                           shop_snapshot: "ShopSnapshotSerializer" = None):
        empty_slots = [x for x in shop_state.friendly_recruits if x.sub_type_as_text == "EmptySlot"]
        if len(empty_slots) >= 1:
            logical_level = self.get_logical_level()
            self.generic_ability_notification(
                state=shop_state,
                state_set=state_set,
                animation_event_sequence=animation_event_sequence)
            if logical_level >= 4:
                number_of_spawned_clones = min(2, len(empty_slots))
                g = Group()
                for i in range(number_of_spawned_clones):
                    choice = empty_slots.pop(0)
                    _copy = Krill()
                    _copy.shop_id = shop_state.get_next_shop_id()
                    _copy.name = f"copy-{choice.team_index}"
                    _copy.aaid = self.aaid
                    _copy.health = self.health
                    _copy.max_health = self.max_health
                    _copy.melee_attack = self.melee_attack
                    _copy.ranged_attack = self.ranged_attack
                    _copy.armor = self.armor
                    _copy.initiative = self.initiative
                    shop_state.replace_empty_slot(recruit=_copy, recruit_index=choice.team_index)
                    shop_state.update_team_indices()
                    e = Animations.PerfectCopy(state_id=state_set.add_state(shop_state),
                                               battle_id=_copy.battle_id,
                                               shop_id=_copy.shop_id
                                               )
                    g.add_animation_event(e)
                g.set_state_id(state_id=state_set.add_state(shop_state))
                animation_event_sequence.append(g)

            else:
                choice = random_engine.choice(empty_slots, seed=shop_snapshot.uuid, snapshot=shop_snapshot)
                _copy = Krill()
                _copy.shop_id = shop_state.get_next_shop_id()
                _copy.name = f"copy-{choice.team_index}"
                _copy.aaid = self.aaid
                shop_state.replace_empty_slot(recruit=_copy, recruit_index=choice.team_index)
                shop_state.update_team_indices()
                e = Animations.PerfectCopy(state_id=state_set.add_state(shop_state),
                                           battle_id=_copy.battle_id,
                                           shop_id=_copy.shop_id
                                           )
                animation_event_sequence.append(e)

