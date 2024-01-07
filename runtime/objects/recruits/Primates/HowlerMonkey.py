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


class HowlerMonkey(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=32,
                         sub_type_as_text="HowlerMonkey", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def start_of_battle(self,
                        battle_state: "BattleStateSerializer",
                        state_set: "StateSet",
                        stack_item: "StackItem",
                        animation_event_sequence: AnimationEventSequence,
                        original_shop_state: "ShopStateSerializer" = None):
        self.generic_ability_notification(
            state=battle_state,
            state_set=state_set,
            animation_event_sequence=animation_event_sequence)
        prob_increment = 0.025
        if self.experience >= GameConstants.Levels.level_3:
            prob_increment = 0.05

        info = battle_state.get_battle_info(battle_id=self.battle_id)
        for x in info.friendly_recruits:
            evasion_prob = 0.0
            if GameConstants.ScientificNames.Primates in x.binomial_nomenclature:
                evasion_prob += prob_increment
            if GameConstants.Habitats.TropicalRainForest in x.binomial_nomenclature:
                evasion_prob += prob_increment
            if evasion_prob > 0.0:
                x.listeners.add_listener(hook=Listeners.Hooks.battle_receive_damage, listener=self)

        g = Group()
        apes = [x for x in info.friendly_recruits if GameConstants.ScientificNames.Primates in x.binomial_nomenclature]
        highest_initiative_recruit = max(apes, key=lambda x: x.initiative)
        for x in info.friendly_recruits:
            if GameConstants.ScientificNames.Primates in x.binomial_nomenclature:
                diff = int(highest_initiative_recruit.initiative - x.initiative)
                x.battle_buff_stats(
                    battle_state=battle_state,
                    state_set=state_set,
                    stack_item=stack_item,
                    animation_event_sequence=animation_event_sequence,
                    initiative=diff,
                    group=g
                )
        g.set_state_id(state_id=state_set.add_state(state=battle_state))
        animation_event_sequence.append(g)

    def lt_battle_receive_damage(self, damage: int,
                                 battle_state: "BattleStateSerializer",
                                 enemy: "BaseRecruit",
                                 state_set: "StateSet",
                                 animation_event_sequence: AnimationEventSequence,
                                 recruit: "RecruitSerializer",
                                 origin: str = "melee",
                                 original_shop_state: "ShopStateSerializer" = None,
                                 damage_reduction_stack: list[dict] = None,
                                 ) -> list[int, bool]:
        prob_increment = 0.025
        if self.experience >= GameConstants.Levels.level_3:
            prob_increment = 0.05

        evasion_prob = 0.0
        if GameConstants.ScientificNames.Primates in recruit.binomial_nomenclature:
            evasion_prob += prob_increment
        if GameConstants.Habitats.TropicalRainForest in recruit.binomial_nomenclature:
            evasion_prob += prob_increment

        random_num = battle_state.random.random()
        if random_num < evasion_prob:
            damage_reduction_stack.append(
                dict(amount=damage, sub_type_as_int=GameConstants.DamageReductionStack.WarningCall))
            e = Animations.Dodge(state_id=state_set.add_state(state=battle_state),
                                 shop_id=recruit.shop_id,
                                 battle_id=recruit.battle_id,
                                 amount=damage)
            animation_event_sequence.append(e)
            return [0, True]

        return [damage, False]

