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


class Shoal(StatusSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=141,
                         sub_type_as_text="Shoal", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def on_append(self, recruit: "RecruitSerializer",
                  battle_state: "BattleStateSerializer",
                  state_set: "StateSet",
                  animation_event_sequence: AnimationEventSequence,
                  group: Group = None):
        recruit.listeners.add_listener(hook=Listeners.Hooks.battle_faint,
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

    def lt_battle_faint(self, battle_state: "BattleStateSerializer",
                        state_set: "StateSet",
                        stack_item: "StackItem",
                        animation_event_sequence: AnimationEventSequence,
                        original_shop_state: "ShopStateSerializer" = None):
        print("Shoal.lt_battle_faint")
        should_return = True
        if self.counter > 0:
            self.counter -= 1
            if self.target.sub_type_as_text == "AtlanticBluefinTuna":
                self.target.health = int(self.target.max_health / 2)
            elif self.target.sub_type_as_text == "AtlanticHerring":
                self.target.health = int(self.target.max_health / 3)
            else:
                self.target.health = int(self.target.max_health / 4)
            e = Animations.ShoalDeath(state_id=state_set.add_state(state=battle_state),
                                      shop_id=self.target.shop_id,
                                      battle_id=self.target.battle_id)
            animation_event_sequence.append(e)
            info = battle_state.get_battle_info(self.target.battle_id)
            objects = [x for x in info.friendly_recruits]
            objects.extend(info.friendly_relics)
            battle_state.queue_ability_for(objects=objects,
                                           trigger=GameConstants.Opcodes.Stack.battle_friendly_recruit_faints,
                                           context={"target": self.target})
            if self.counter == 0:
                self.target.remove_status(status=self)
                self.target.listeners.remove_listener(hook=Listeners.Hooks.battle_faint, listener=self)
        else:
            should_return = False

        return should_return

