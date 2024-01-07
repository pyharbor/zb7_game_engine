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


class DivingBellSpider(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=241,
                         sub_type_as_text="DivingBellSpider", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def shop_bought(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                    animation_event_sequence: AnimationEventSequence,
                    shop_snapshot: "ShopSnapshotSerializer" = None):
        g = Group()
        for x in shop_state.friendly_recruits:
            if GameConstants.ScientificNames.Arachnida in x.binomial_nomenclature:
                if GameConstants.Habitats.Ponds not in x.binomial_nomenclature:
                    e = Animations.AddHabitat(
                        shop_id=x.shop_id,
                        battle_id=x.battle_id,
                        state_id=state_set.add_state(shop_state),
                        habitat_as_int=ImmutableData.Habitats.from_text(
                            GameConstants.Habitats.Ponds)
                    )
                    g.add_animation_event(e)
                x.binomial_nomenclature.append_type(type_name=GameConstants.Habitats.Ponds)
                x.added_types.append(GameConstants.Habitats.Ponds)
        g.set_state_id(state_set.add_state(shop_state))
        animation_event_sequence.append(g)

    def shop_sold(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                  animation_event_sequence: AnimationEventSequence):
        g = Group()
        for x in shop_state.friendly_recruits:
            if GameConstants.ScientificNames.Arachnida in x.binomial_nomenclature and GameConstants.Habitats.Ponds in x.binomial_nomenclature:
                x.binomial_nomenclature.remove_type(type_name=GameConstants.Habitats.Ponds)
                x.added_habitats.remove(GameConstants.Habitats.Ponds)
                e = Animations.ShopUpdatedRecruit(
                    shop_id=x.shop_id,
                    battle_id=x.battle_id,
                    state_id=state_set.add_state(shop_state)
                )
                g.add_animation_event(e)
        if len(g.animation_events) > 0:
            g.set_state_id(state_set.add_state(shop_state))
            animation_event_sequence.append(g)

    def battle_friendly_recruit_summoned(self, battle_state: "BattleStateSerializer",
                                         state_set: StateSet,
                                         stack_item: StackItem,
                                         animation_event_sequence: AnimationEventSequence,
                                         original_shop_state: "ShopStateSerializer" = None):
        recruit = stack_item.context
        if GameConstants.ScientificNames.Arachnida in recruit.binomial_nomenclature:
            recruit.binomial_nomenclature.append_type(type_name=GameConstants.Habitats.Ponds)
            recruit.added_habitats.append(GameConstants.Habitats.Ponds)
            if GameConstants.Habitats.Ponds not in recruit.binomial_nomenclature:
                e = Animations.AddHabitat(
                    shop_id=recruit.shop_id,
                    battle_id=recruit.battle_id,
                    state_id=state_set.add_state(battle_state),
                    habitat_as_int=ImmutableData.Habitats.from_text(
                        GameConstants.Habitats.Ponds)
                )
                animation_event_sequence.append(e)

    def shop_friendly_recruit_summoned(self, shop_state: "ShopStateSerializer",
                                       state_set: StateSet,
                                       stack_item: StackItem,
                                       animation_event_sequence: AnimationEventSequence,
                                       original_shop_state: "ShopSnapshotSerializer" = None):
        recruit = stack_item.context["target"]
        if GameConstants.ScientificNames.Arachnida in recruit.binomial_nomenclature:
            recruit.binomial_nomenclature.append_type(type_name=GameConstants.Habitats.Ponds)
            recruit.added_habitats.append(GameConstants.Habitats.Ponds)
            if GameConstants.Habitats.Ponds not in recruit.binomial_nomenclature:
                e = Animations.AddHabitat(
                    shop_id=recruit.shop_id,
                    battle_id=recruit.battle_id,
                    state_id=state_set.add_state(shop_state),
                    habitat_as_int=ImmutableData.Habitats.from_text(
                        GameConstants.Habitats.Ponds)
                )
                animation_event_sequence.append(e)

    def shop_end_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                         animation_event_sequence: AnimationEventSequence,
                         shop_snapshot: "ShopSnapshotSerializer" = None):
        logical_level = self.get_logical_level()
        if logical_level < 4:
            return
        fish_count = len([x for x in shop_state.friendly_recruits if GameConstants.ScientificNames.Actinopterygii in x.binomial_nomenclature])
        buff = fish_count * 3
        if buff > 0:
            self.generic_ability_notification(
                state=shop_state,
                state_set=state_set,
                animation_event_sequence=animation_event_sequence)
            g = Group()
            for x in shop_state.friendly_recruits:
                if GameConstants.ScientificNames.Arachnida in x.binomial_nomenclature:
                    x.shop_buff_stats(
                        shop_state=shop_state,
                        state_set=state_set,
                        stack_item=stack_item,
                        animation_event_sequence=animation_event_sequence,
                        ranged=buff,
                        health=buff,
                        max_health=buff,
                        melee=buff,
                        group=g
                    )

            g.set_state_id(state_id=state_set.add_state(state=shop_state))
            animation_event_sequence.append(g)

