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


class BurrowingOwl(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=106,
                         sub_type_as_text="BurrowingOwl", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def start_of_battle(self,
                        battle_state: "BattleStateSerializer",
                        state_set: "StateSet",
                        stack_item: "StackItem",
                        animation_event_sequence: AnimationEventSequence,
                        original_shop_state: "ShopStateSerializer" = None):
        self.generic_ability_notification(
            state_set=state_set,
            animation_event_sequence=animation_event_sequence,
            state=battle_state
        )
        if self.experience < GameConstants.Levels.level_2:
            self.add_status(Statuses.Burrowed(counter=1), battle_state=battle_state, state_set=state_set,
                            animation_event_sequence=animation_event_sequence,
                            enemy=None)
        else:
            self.add_status(Statuses.Burrowed(counter=2), battle_state=battle_state, state_set=state_set,
                            animation_event_sequence=animation_event_sequence,
                            enemy=None)

    def battle_receive_damage(self, damage: int,
                              battle_state: "BattleStateSerializer",
                              enemy: "RecruitSerializer",
                              state_set: StateSet,
                              animation_event_sequence: AnimationEventSequence,
                              origin: str = "melee",
                              original_shop_state: "ShopStateSerializer" = None,
                              damage_reduction_stack: list[dict] = None
                              ) -> int:
        overkill = super().battle_receive_damage(damage, battle_state, enemy, state_set, animation_event_sequence,
                                                 origin, original_shop_state, damage_reduction_stack)
        if overkill > 0:
            g = Group()
            g2 = Group()
            info = battle_state.get_battle_info(battle_id=self.battle_id)
            heal_amount = 0
            if self.experience < GameConstants.Levels.level_2:
                heal_amount = 10
            elif self.experience < GameConstants.Levels.level_3:
                heal_amount = 15
            elif self.experience < GameConstants.Levels.level_4:
                heal_amount = 20
            else:
                heal_amount = 25

            for x in info.friendly_recruits:
                status = x.get_status(sub_type_as_text="Airborne")
                if status:
                    x.add_status(status=Statuses.Airborne(counter=1), battle_state=battle_state, state_set=state_set,
                                 animation_event_sequence=animation_event_sequence, group=g2,
                                 enemy=None)
                for h in GameConstants.Habitats.Arid:
                    if h in x.binomial_nomenclature:
                        x.battle_heal(
                            healer=self,
                            heal=heal_amount,
                            battle_state=battle_state,
                            state_set=state_set,
                            animation_event_sequence=animation_event_sequence,
                            group=g
                        )
            g.set_state_id(state_id=state_set.add_state(battle_state))
            g2.set_state_id(state_id=state_set.add_state(battle_state))
            if len(g.animation_events) > 0:
                animation_event_sequence.append(g)
            if len(g2.animation_events) > 0:
                animation_event_sequence.append(g2)

        return overkill

