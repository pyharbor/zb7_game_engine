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


class BaskingShark(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=29,
                         sub_type_as_text="BaskingShark", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def shop_start_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                           animation_event_sequence: AnimationEventSequence,
                           shop_snapshot: "ShopSnapshotSerializer" = None):
        krill = [x for x in shop_state.friendly_recruits if
                 x.sub_type_as_text == "Krill" and x.team_index < self.team_index]
        if len(krill) == 0:
            return
        logical_leve = self.get_logical_level()
        if logical_leve < 3:
            targets = [krill[-1]]
        else:
            targets = krill
        health_buff = 0
        melee = 0
        range = 0
        for target in targets:

            e = Animations.Swallow(state_id=state_set.add_state(shop_state),
                                   battle_id=target.battle_id,
                                   shop_id=target.shop_id,
                                   target_shop_id=target.shop_id,
                                   target_battle_id=target.battle_id)
            animation_event_sequence.append(e)

            target.shop_faint(shop_state=shop_state,
                              state_set=state_set,
                              stack_item=stack_item,
                              animation_event_sequence=animation_event_sequence,
                              original_shop_state=shop_snapshot)

            e = Animations.Consume(state_id=state_set.add_state(shop_state),
                                   battle_id=self.battle_id,
                                   shop_id=self.shop_id,
                                   target_shop_id=target.shop_id,
                                   target_battle_id=target.battle_id)
            animation_event_sequence.append(e)

            if self.experience <= GameConstants.Levels.level_2:
                health_buff += 8
                melee += 1
                range += 3
            elif self.experience <= GameConstants.Levels.level_3:
                health_buff += 16
                melee += 2
                range += 6
            else:
                health_buff += 24
                melee += 3
                range += 9

        self.shop_buff_stats(
            shop_state=shop_state,
            animation_event_sequence=animation_event_sequence,
            state_set=state_set,
            stack_item=stack_item,
            health=health_buff,
            max_health=health_buff,
            melee=melee,
            ranged=range,
        )

    def battle_faint(self, battle_state: "BattleStateSerializer",
                     state_set: StateSet,
                     stack_item: "StackItem",
                     animation_event_sequence: AnimationEventSequence,
                     original_shop_state: "ShopStateSerializer" = None):
        for x in self.listeners.get_listeners(hook=Listeners.Hooks.battle_faint):
            # basically we allow arbitrary other objects to affect the 'fainting' of a unit
            # if that unit is revived it doesn't actually need to faint and thus returns immediately
            should_return = x.lt_battle_faint(
                battle_state=battle_state,
                state_set=state_set,
                stack_item=stack_item,
                animation_event_sequence=animation_event_sequence,
                original_shop_state=original_shop_state
            )
            if should_return:
                return
        info = battle_state.get_battle_info(battle_id=self.battle_id)
        krill = [x for x in info.friendly_recruits if
                 x.sub_type_as_text == "Krill" and x.team_index < self.team_index]
        if len(krill) == 0:
            return super().battle_faint(battle_state=battle_state,
                                        state_set=state_set,
                                        stack_item=stack_item,
                                        animation_event_sequence=animation_event_sequence,
                                        original_shop_state=original_shop_state)
        target_krill = krill[0]
        e = Animations.Swallow(state_id=state_set.add_state(battle_state),
                               battle_id=target_krill.battle_id,
                               shop_id=target_krill.shop_id,
                               target_shop_id=target_krill.shop_id,
                               target_battle_id=target_krill.battle_id)
        animation_event_sequence.append(e)

        target_krill.battle_faint(battle_state=battle_state,
                                  state_set=state_set,
                                  stack_item=stack_item,
                                  animation_event_sequence=animation_event_sequence,
                                  original_shop_state=original_shop_state)

        self.battle_heal(
            battle_state=battle_state,
            state_set=state_set,
            animation_event_sequence=animation_event_sequence,
            healer=self,
            heal=int(self.max_health)
        )

    def shop_faint(self, shop_state: "ShopStateSerializer",
                   state_set: StateSet,
                   stack_item: "StackItem",
                   animation_event_sequence: AnimationEventSequence,
                   original_shop_state: "ShopStateSerializer" = None):
        krill = [x for x in shop_state.friendly_recruits if
                 x.sub_type_as_text == "Krill" and x.team_index > self.team_index]
        if len(krill) == 0:
            return super().shop_faint(shop_state=shop_state,
                                      state_set=state_set,
                                      stack_item=stack_item,
                                      animation_event_sequence=animation_event_sequence,
                                      original_shop_state=original_shop_state)
        target_krill = krill[0]
        e = Animations.Swallow(state_id=state_set.add_state(shop_state),
                               battle_id=target_krill.battle_id,
                               shop_id=target_krill.shop_id,
                               target_shop_id=target_krill.shop_id,
                               target_battle_id=target_krill.battle_id)
        animation_event_sequence.append(e)
        target_krill.shop_faint(shop_state=shop_state,
                                state_set=state_set,
                                stack_item=stack_item,
                                animation_event_sequence=animation_event_sequence,
                                original_shop_state=original_shop_state)
        self.health = self.max_health
        e = Animations.Heal(amount=self.max_health,
                            state_id=state_set.add_state(shop_state),
                            battle_id=self.battle_id,
                            shop_id=self.shop_id)
        animation_event_sequence.append(e)

