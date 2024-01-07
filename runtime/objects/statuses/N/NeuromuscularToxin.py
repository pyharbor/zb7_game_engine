from typing import List
from zb7_game_engine.serialization.animation_events.G.Group import Group
from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature
from zb7_game_engine.runtime.core.StackItem import StackItem
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus
from zb7_game_engine.serialization.StatusSerializer import StatusSerializer
from typing import List, TYPE_CHECKING, Union
from zb7_game_engine.runtime.core.Listeners import Listeners
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


class NeuromuscularToxin(StatusSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=248,
                         sub_type_as_text="NeuromuscularToxin", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def status_effect(self,
                      recruit: "RecruitSerializer",
                      battle_state: "BattleStateSerializer",
                      state_set: "StateSet",
                      stack_item: "StackItem",
                      animation_event_sequence: AnimationEventSequence,
                      original_shop_state: "ShopStateSerializer" = None):
        recruit.battle_receive_status_damage(damage=self.counter,
                                             battle_state=battle_state,
                                             state_set=state_set,
                                             status=self,
                                             animation_event_sequence=animation_event_sequence)
        e = Animations.ReceiveStatusDamage(status_sub_type_as_int=self.sub_type_as_int,
                                           battle_id=recruit.battle_id,
                                           shop_id=recruit.shop_id,
                                           amount=self.counter,
                                           state_id=state_set.add_state(state=battle_state))
        animation_event_sequence.append(e)
        self.target.remove_status(status=self)

    def on_append(self, recruit: "RecruitSerializer",
                  battle_state: "BattleStateSerializer",
                  state_set: "StateSet",
                  animation_event_sequence: AnimationEventSequence,
                  group: Group = None):
        self.target = recruit
        recruit.battle_receive_status_damage(damage=self.counter,
                                             battle_state=battle_state,
                                             state_set=state_set,
                                             status=self,
                                             animation_event_sequence=animation_event_sequence)
        e = Animations.ReceiveStatusDamage(status_sub_type_as_int=self.sub_type_as_int,
                                           battle_id=recruit.battle_id,
                                           shop_id=recruit.shop_id,
                                           amount=self.counter,
                                           state_id=state_set.add_state(state=battle_state))
        animation_event_sequence.append(e)

