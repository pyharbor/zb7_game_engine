from typing import List, TYPE_CHECKING
from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.objects.base.BaseListener import BaseListener
from zb7_game_engine.serialization.animation_events.Animations import Animations
from zb7_game_engine.serialization.animation_events.G.Group import Group

if TYPE_CHECKING:
    from zb7_game_engine.serialization.BattleStateSerializer import BattleStateSerializer
    from zb7_game_engine.runtime.core.StackItem import StackItem
    from zb7_game_engine.runtime.core.StateSet import StateSet
    from zb7_game_engine.serialization.ShopStateSerializer import ShopStateSerializer
    from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
    from zb7_game_engine.serialization.StatusSerializer import StatusSerializer


class BaseStatus(BaseListener):
    def __init__(self,
                 sub_type_as_int: int,
                 sub_type_as_text: str,
                 ability=None,
                 type: str = None,
                 triggers: List[str] = None,
                 arts: List[str] = None,
                 counter: int = None,
                 target: "RecruitSerializer" = None,
                 stack_order_number: int = None):
        self.sub_type_as_int = sub_type_as_int
        self.sub_type_as_text = sub_type_as_text
        immutable_data = ImmutableData.Subtype.from_int(sub_type_as_int)
        self.counter = counter or 0
        self.ability = ability or immutable_data["ability"]
        self.type = type or immutable_data["type"]
        self.triggers = triggers or immutable_data["triggers"]
        self.arts = arts or immutable_data["arts"]
        self.stack_order_number = immutable_data.get("stack_order_number")
        self.target = target

    def status_effect(self,
                      recruit: "RecruitSerializer",
                      battle_state: "BattleStateSerializer",
                      state_set: "StateSet",
                      stack_item: "StackItem",
                      animation_event_sequence: AnimationEventSequence,
                      original_shop_state: "ShopStateSerializer" = None):
        pass

    def stack(self,
              other: "StatusSerializer",
              recruit: "RecruitSerializer",
              battle_state: "BattleStateSerializer",
              state_set: "StateSet",
              animation_event_sequence: AnimationEventSequence,
              group: Group = None):
        self.counter += other.counter
        e = Animations.AddStatus(state_id=state_set.add_state(state=battle_state),
                                 shop_id=recruit.shop_id,
                                 battle_id=recruit.battle_id,
                                 status_sub_type_as_int=self.sub_type_as_int,
                                 amount=other.counter)
        if group:
            group.add_animation_event(e)
        else:
            animation_event_sequence.append(e)

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

    def __str__(self):
        return f"{self.sub_type_as_text}(counter={self.counter})"

    def __repr__(self):
        return self.__str__()
