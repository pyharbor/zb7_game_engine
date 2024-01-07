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


class ThickBlubber(StatusSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=146,
                         sub_type_as_text="ThickBlubber", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def on_append(self, recruit: "RecruitSerializer",
                  battle_state: "BattleStateSerializer",
                  state_set: "StateSet",
                  animation_event_sequence: AnimationEventSequence,
                  group: Group = None):
        e = Animations.AddStatus(state_id=state_set.add_state(state=battle_state),
                                 shop_id=recruit.shop_id,
                                 battle_id=recruit.battle_id,
                                 status_sub_type_as_int=self.sub_type_as_int,
                                 amount=self.counter)
        if group:
            group.add_animation_event(e)
        else:
            animation_event_sequence.append(e)
        recruit.listeners.add_listener(hook=Listeners.Hooks.battle_receive_damage,
                                       listener=self)
        self.target = recruit

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
        percentage = 0.97 ** self.counter
        original_damage = damage
        damage = int(damage * percentage)
        diff = original_damage - damage
        if damage_reduction_stack is not None:
            damage_reduction_stack.append(dict(amount=diff, sub_type_as_int=GameConstants.DamageReductionStack.ThickBlubber))
        return [damage, False]

    def stack(self,
              other: "StatusSerializer",
              recruit: "RecruitSerializer",
              battle_state: "BattleStateSerializer",
              state_set: "StateSet",
              animation_event_sequence: AnimationEventSequence,
              group: Group = None):
        self.counter += other.counter
        self.counter = min(self.counter, 20)

