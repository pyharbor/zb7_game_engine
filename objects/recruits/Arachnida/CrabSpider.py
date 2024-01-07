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


class CrabSpider(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=13,
                         sub_type_as_text="CrabSpider", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def battle_attack_with_range(self, battle_state: "BattleStateSerializer",
                                 state_set: StateSet,
                                 stack_item: "StackItem",
                                 animation_event_sequence: AnimationEventSequence,
                                 original_shop_state: "ShopStateSerializer" = None,
                                 damage_type: str = "default",
                                 group=None) -> Union["RecruitSerializer", None]:
        if self.team_index != 0 and self.ranged_attack > 0:
            random_enemy = super().battle_attack_with_range(battle_state, state_set, stack_item,
                                                            animation_event_sequence,
                                                            original_shop_state, damage_type, group)
            if self.experience < GameConstants.Levels.level_2:
                status = Statuses.Cytotoxin(counter=1)
            elif self.experience < GameConstants.Levels.level_3:
                status = Statuses.Cytotoxin(counter=2)
            else:
                status = Statuses.Cytotoxin(counter=3)
            if random_enemy is not None:
                random_enemy.add_status(status=status, battle_state=battle_state, state_set=state_set,
                                        animation_event_sequence=animation_event_sequence,
                                        enemy=self)
            return random_enemy

    def shop_bought(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                    animation_event_sequence: AnimationEventSequence,
                    shop_snapshot: "ShopSnapshotSerializer" = None):
        g = Group()
        for x in shop_state.friendly_recruits:
            if GameConstants.ScientificNames.Arachnida in x.binomial_nomenclature:
                if GameConstants.ScientificNames.Crustacea not in x.binomial_nomenclature:
                    e = Animations.AddSpecies(
                        shop_id=x.shop_id,
                        battle_id=x.battle_id,
                        state_id=state_set.add_state(shop_state),
                        species_as_int=ImmutableData.ScientificNomenclature.to_int(
                            GameConstants.ScientificNames.Crustacea)
                    )
                    g.add_animation_event(e)
                    x.binomial_nomenclature.append_type(type_name=GameConstants.ScientificNames.Crustacea)
                    x.added_types.append(GameConstants.ScientificNames.Crustacea)
        g.set_state_id(state_set.add_state(shop_state))
        animation_event_sequence.append(g)

    def shop_sold(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                  animation_event_sequence: AnimationEventSequence):
        g = Group()
        for x in shop_state.friendly_recruits:
            if GameConstants.ScientificNames.Arachnida in x.binomial_nomenclature and GameConstants.ScientificNames.Crustacea in x.binomial_nomenclature:
                x.binomial_nomenclature.remove_type(type_name=GameConstants.ScientificNames.Crustacea)
                x.added_types.remove(GameConstants.ScientificNames.Crustacea)
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
            recruit.binomial_nomenclature.append_type(type_name=GameConstants.ScientificNames.Crustacea)
            recruit.added_types.append(GameConstants.ScientificNames.Crustacea)
            if GameConstants.ScientificNames.Crustacea not in recruit.binomial_nomenclature:
                e = Animations.AddSpecies(
                    shop_id=recruit.shop_id,
                    battle_id=recruit.battle_id,
                    state_id=state_set.add_state(battle_state),
                    species_as_int=ImmutableData.ScientificNomenclature.to_int(
                        GameConstants.ScientificNames.Crustacea)
                )
                animation_event_sequence.append(e)

    def shop_friendly_recruit_summoned(self, shop_state: "ShopStateSerializer",
                                       state_set: StateSet,
                                       stack_item: StackItem,
                                       animation_event_sequence: AnimationEventSequence,
                                       original_shop_state: "ShopSnapshotSerializer" = None):
        recruit = stack_item.context["target"]
        if GameConstants.ScientificNames.Arachnida in recruit.binomial_nomenclature:
            recruit.binomial_nomenclature.append_type(type_name=GameConstants.ScientificNames.Crustacea)
            recruit.added_types.append(GameConstants.ScientificNames.Crustacea)
            if GameConstants.ScientificNames.Crustacea not in recruit.binomial_nomenclature:
                e = Animations.AddSpecies(
                    shop_id=recruit.shop_id,
                    battle_id=recruit.battle_id,
                    state_id=state_set.add_state(shop_state),
                    species_as_int=ImmutableData.ScientificNomenclature.to_int(
                        GameConstants.ScientificNames.Crustacea)
                )
                animation_event_sequence.append(e)

