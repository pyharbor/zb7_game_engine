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


class AmericanLobster(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=247,
                         sub_type_as_text="AmericanLobster", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def shop_buff_stats(self, shop_state: "ShopStateSerializer",
                        stack_item: "StackItem",
                        state_set: "StateSet",
                        animation_event_sequence: AnimationEventSequence,
                        original_shop_state: "ShopStateSerializer" = None,
                        melee: int = 0,
                        ranged: int = 0,
                        health: int = 0,
                        max_health: int = 0,
                        armor: int = 0,
                        initiative: int = 0,
                        buffer: Union["RecruitSerializer", "RelicSerializer"] = None,
                        group: Group = None):
        self.melee_attack += melee
        self.ranged_attack += ranged
        self.health += health
        self.initiative += initiative
        self.initiative = round(self.initiative, 3)
        self.armor += armor
        self.melee_attack = self.melee_attack
        self.ranged_attack = self.ranged_attack
        self.health = max(1, self.health)
        self.max_health += max_health
        self.initiative = max(1, self.initiative)
        self.armor = max(0, self.armor)

        self.armor = min(50, self.armor)
        self.melee_attack = min(50, self.melee_attack)
        self.ranged_attack = min(50, self.ranged_attack)
        self.health = min(50, self.health)
        self.max_health = min(50, self.max_health)
        self.initiative = min(50, self.initiative)

        e = Animations.BuffStats(
            state_id=None,
            shop_id=self.shop_id,
            battle_id=self.battle_id,
            melee=melee,
            ranged=ranged,
            health=health,
            armor=armor,
            initiative=initiative,
            max_health=max_health,
        )
        if group is None:
            e.state_id = state_set.add_state(state=shop_state)
            animation_event_sequence.append(e)
        else:
            group.add_animation_event(e)

    def battle_buff_stats(self, battle_state: "BattleStateSerializer",
                          stack_item: "StackItem",
                          state_set: "StateSet",
                          animation_event_sequence: AnimationEventSequence,
                          original_shop_state: "ShopStateSerializer" = None,
                          melee: int = 0,
                          ranged: int = 0,
                          health: int = 0,
                          max_health: int = 0,
                          armor: int = 0,
                          initiative: int = 0,
                          buffer: Union["RecruitSerializer", "RelicSerializer"] = None,
                          group: Group = None):
        for x in self.listeners.get_listeners(hook=Listeners.Hooks.battle_buff_stats):
            should_return = x.lt_battle_buff_stats(
                battle_state=battle_state,
                state_set=state_set,
                animation_event_sequence=animation_event_sequence,
                original_shop_state=original_shop_state,
                melee=melee,
                ranged=ranged,
                health=health,
                max_health=max_health,
                armor=armor,
                initiative=initiative,
                stack_item=stack_item,
                buffer=buffer,
                group=group
            )
            if should_return:
                return

        self.melee_attack += melee
        self.ranged_attack += ranged
        self.health += health
        self.max_health += max_health
        self.initiative += initiative
        self.initiative = round(self.initiative, 3)
        self.armor += armor
        self.health = max(1, self.health)
        self.max_health = max(1, self.max_health)
        self.initiative = max(1, self.initiative)
        self.armor = max(0, self.armor)

        self.armor = min(50, self.armor)
        self.melee_attack = min(50, self.melee_attack)
        self.ranged_attack = min(50, self.ranged_attack)
        self.health = min(50, self.health)
        self.max_health = min(50, self.max_health)
        self.initiative = min(50, self.initiative)

        e = Animations.BuffStats(
            state_id=None,
            shop_id=self.shop_id,
            battle_id=self.battle_id,
            melee=melee,
            ranged=ranged,
            health=health,
            max_health=max_health,
            armor=armor,
            initiative=initiative,
        )
        if group is None:
            e.state_id = state_set.add_state(state=battle_state)
            animation_event_sequence.append(e)
        else:
            group.add_animation_event(e)

