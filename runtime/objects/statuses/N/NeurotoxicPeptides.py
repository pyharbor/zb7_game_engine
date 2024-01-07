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


class NeurotoxicPeptides(StatusSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=155,
                         sub_type_as_text="NeurotoxicPeptides", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def status_effect(self,
                      recruit: "RecruitSerializer",
                      battle_state: "BattleStateSerializer",
                      state_set: "StateSet",
                      stack_item: "StackItem",
                      animation_event_sequence: AnimationEventSequence,
                      original_shop_state: "ShopStateSerializer" = None):
        damage = max(int(recruit.max_health * (self.counter * 0.01)), 0)
        recruit.battle_receive_status_damage(
            damage=damage,
            status=self,
            battle_state=battle_state,
            state_set=state_set,
            animation_event_sequence=animation_event_sequence
        )

    def lt_battle_attack_with_range(self, battle_state: "BattleStateSerializer",
                                    damage: int,
                                    enemy: "RecruitSerializer",
                                    state_set: "StateSet",
                                    stack_item: "StackItem",
                                    animation_event_sequence: AnimationEventSequence,
                                    original_shop_state: "ShopStateSerializer" = None,
                                    damage_type: str = "default",
                                    group: Group = None) -> list[int, bool]:
        damage = max(0, damage - self.counter)
        return [damage, False]

    def lt_battle_attack_with_melee(self, battle_state: "BattleStateSerializer",
                                    damage: int,
                                    enemy: "RecruitSerializer",
                                    state_set: "StateSet",
                                    stack_item: "StackItem",
                                    animation_event_sequence: AnimationEventSequence,
                                    original_shop_state: "ShopStateSerializer" = None,
                                    damage_type: str = "default"):
        damage = max(0, damage - self.counter)
        return [damage, False]

    def stack(self,
              other: "StatusSerializer",
              recruit: "RecruitSerializer",
              battle_state: "BattleStateSerializer",
              state_set: "StateSet",
              animation_event_sequence: AnimationEventSequence,
              group: Group = None):
        pass

    def on_append(self, recruit: "RecruitSerializer",
                  battle_state: "BattleStateSerializer",
                  state_set: "StateSet",
                  animation_event_sequence: AnimationEventSequence,
                  group: Group = None):
        recruit.listeners.add_listener(hook=Listeners.Hooks.battle_attack_with_range,
                                       listener=self)
        recruit.listeners.add_listener(hook=Listeners.Hooks.battle_attack_with_melee,
                                       listener=self)
        self.target = recruit
        e = Animations.AddStatus(state_id=state_set.add_state(state=battle_state),
                                 shop_id=recruit.shop_id,
                                 battle_id=recruit.battle_id,
                                 status_sub_type_as_int=self.sub_type_as_int,
                                 amount=self.counter)
        if group:
            group.add_animation_event(e)
        else:
            animation_event_sequence.append(e)

