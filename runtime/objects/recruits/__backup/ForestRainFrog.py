from typing import List
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


class ForestRainFrog(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=52,
                         sub_type_as_text="ForestRainFrog", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def shop_start_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                           animation_event_sequence: AnimationEventSequence):
        self.generic_ability_notification(description=self.ability[0].name,
                                          state=shop_state,
                                          state_set=state_set,
                                          animation_event_sequence=animation_event_sequence)

        gain_experience_group = Animations.Group()
        level_up_group = Animations.Group()

        # custom stuff here
        for x in shop_state.friendly_recruits:
            if GameConstants.ScientificNames.Amphibia in x.binomial_nomenclature:
                x.experience += 1
                shop_state.queue_ability_for(trigger=GameConstants.Opcodes.Shop.shop_gain_experience,
                                             objects=[x],
                                             context={})
                e = Animations.ShopGainExperience(amount=1, shop_id=x.shop_id,
                                                  state_id=None)
                gain_experience_group.add_animation_event(e)
                if x.experience in GameConstants.Levels.all:
                    e = Animations.ShopLevelUp(amount=1, shop_id=x.shop_id, state_id=None)
                    shop_state.queue_ability_for(objects=[x],
                                                 trigger=GameConstants.Opcodes.Shop.shop_level_up,
                                                 context={"recruit": x})
        if len(gain_experience_group.animation_events) > 0:
            animation_event_sequence.append(gain_experience_group)
        if len(level_up_group.animation_events) > 0:
            animation_event_sequence.append(level_up_group)
        gain_experience_group.set_state_id(state_set.add_state(shop_state))
        level_up_group.set_state_id(state_set.add_state(shop_state))


