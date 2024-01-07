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


class Chlorotoxin(StatusSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=137,
                         sub_type_as_text="Chlorotoxin", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------
        self.first_invocation = True

        
    def lt_battle_attack_with_range(self, battle_state: "BattleStateSerializer",
                                    damage: int,
                                    enemy: "RecruitSerializer",
                                    state_set: "StateSet",
                                    stack_item: "StackItem",
                                    animation_event_sequence: AnimationEventSequence,
                                    original_shop_state: "ShopStateSerializer" = None,
                                    damage_type: str = "default",
                                    group: Group = None) -> list[int, bool]:
        should_return = True
        return [0, should_return]

    def lt_battle_attack_with_melee(self, battle_state: "BattleStateSerializer",
                                    damage: int,
                                    enemy: "RecruitSerializer",
                                    state_set: "StateSet",
                                    stack_item: "StackItem",
                                    animation_event_sequence: AnimationEventSequence,
                                    original_shop_state: "ShopStateSerializer" = None,
                                    damage_type: str = "default"):
        should_return = True
        return [0, should_return]

    def lt_battle_friendly_recruit_faints(self, battle_state: "BattleStateSerializer",
                                          state_set: "StateSet",
                                          stack_item: "StackItem",
                                          animation_event_sequence: AnimationEventSequence,
                                          original_shop_state: "ShopStateSerializer" = None):
        should_return = True
        return should_return

    def lt_battle_friendly_recruit_summoned(self, battle_state: "BattleStateSerializer",
                                            state_set: "StateSet",
                                            stack_item: "StackItem",
                                            animation_event_sequence: AnimationEventSequence,
                                            original_shop_state: "ShopStateSerializer" = None):
        should_return = True
        return should_return

    def lt_passive_battle_ability(self,
                                  battle_state: "BattleStateSerializer",
                                  state_set: "StateSet",
                                  stack_item: "StackItem",
                                  animation_event_sequence: AnimationEventSequence,
                                  original_shop_state: "ShopStateSerializer" = None):
        should_return = True
        e = Animations.ChlorotoxinEffect(state_id=state_set.add_state(battle_state),
                                         battle_id=self.target.battle_id)
        animation_event_sequence.append(e)
        return should_return

    def status_effect(self,
                      recruit: "RecruitSerializer",
                      battle_state: "BattleStateSerializer",
                      state_set: "StateSet",
                      stack_item: "StackItem",
                      animation_event_sequence: AnimationEventSequence,
                      original_shop_state: "ShopStateSerializer" = None):
        if self.first_invocation:
            self.first_invocation = False
            return
        else:
            self.counter -= 1
            self.target.remove_status(status=self)
            self.target.listeners.remove_listener(hook=Listeners.Hooks.battle_receive_damage, listener=self)
            self.target.listeners.remove_listener(hook=Listeners.Hooks.passive_battle_ability, listener=self)
            self.target.listeners.remove_listener(hook=Listeners.Hooks.battle_friendly_recruit_summoned, listener=self)
            self.target.listeners.remove_listener(hook=Listeners.Hooks.battle_friendly_recruit_faints, listener=self)
            self.target.listeners.remove_listener(hook=Listeners.Hooks.battle_attack_with_range, listener=self)
            self.target.listeners.remove_listener(hook=Listeners.Hooks.battle_attack_with_melee, listener=self)

    def on_append(self, recruit: "RecruitSerializer",
                  battle_state: "BattleStateSerializer",
                  state_set: "StateSet",
                  animation_event_sequence: AnimationEventSequence,
                  group: Group = None):
        recruit.listeners.add_listener(hook=Listeners.Hooks.passive_battle_ability,
                                       listener=self)
        recruit.listeners.add_listener(hook=Listeners.Hooks.battle_friendly_recruit_faints,
                                       listener=self)
        recruit.listeners.add_listener(hook=Listeners.Hooks.battle_friendly_recruit_summoned,
                                       listener=self)
        recruit.listeners.add_listener(hook=Listeners.Hooks.battle_attack_with_melee,
                                       listener=self)
        recruit.listeners.add_listener(hook=Listeners.Hooks.battle_attack_with_range,
                                       listener=self)
        self.target = recruit

    def stack(self,
              other: "StatusSerializer",
              recruit: "RecruitSerializer",
              battle_state: "BattleStateSerializer",
              state_set: "StateSet",
              animation_event_sequence: AnimationEventSequence,
              group: Group = None):
        self.first_invocation = True

