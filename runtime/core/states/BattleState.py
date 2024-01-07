import json
from collections import deque
import random
from typing import List, Union, Dict, TYPE_CHECKING

from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.StackItem import StackItem
from zb7_game_engine.runtime.core.states.BattleInfo import BattleInfo
from zb7_game_engine.runtime.objects.base.BaseRecruit import BaseRecruit
from zb7_game_engine.runtime.objects.base.BaseRelic import BaseRelic
from zb7_game_engine.serialization.EmptySlotSerializer import EmptySlotSerializer
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer
from zb7_game_engine.serialization.animation_events.Animations import Animations

if TYPE_CHECKING:
    from zb7_game_engine.runtime.core.StateSet import StateSet
    from zb7_game_engine.serialization.BattleStateSerializer import BattleStateSerializer


class BattleState:
    def __init__(self,
                 friendly_recruits: List[RecruitSerializer],
                 friendly_relics: List[RelicSerializer],
                 enemy_recruits: List[RecruitSerializer],
                 enemy_relics: List[RelicSerializer],
                 battle_turn: int = 0,
                 friendly_uuid: str = "",
                 enemy_uuid: str = "",
                 shop_turn: int = 0,
                 original_shop_state=None,
                 simulate: bool = False
                 ):
        # these are packed in lists within json
        self.battle_turn = battle_turn
        self.friendly_uuid = friendly_uuid
        self.enemy_uuid = enemy_uuid
        self.friendly_recruits = [x for x in friendly_recruits if not isinstance(x, EmptySlotSerializer)]
        self.friendly_relics = friendly_relics
        self.enemy_recruits = [x for x in enemy_recruits if not isinstance(x, EmptySlotSerializer)]
        self.enemy_relics = enemy_relics
        self.stack: deque[StackItem] = deque()
        if simulate:
            self.seed = str(random.randint(0, 2 ** 32))
        else:
            self.seed = self.friendly_uuid + ":" + self.enemy_uuid + ":" + str(shop_turn)
        self.random = random.Random(x=self.seed)
        self.original_shop_state = original_shop_state

        for i, x in enumerate(self.friendly_recruits):
            x.team_index = i

        for i, x in enumerate(self.enemy_recruits):
            x.team_index = i

        # All ties will favor the friendly team although they should very rarely happen
        self.objects_sorted = []
        self.objects_sorted.extend(self.enemy_recruits)
        self.objects_sorted.extend(self.enemy_relics)
        self.objects_sorted.extend(self.friendly_recruits)
        self.objects_sorted.extend(self.friendly_relics)
        self.objects_sorted = sorted(self.objects_sorted, key=lambda x: x.initiative)

        self.battle_ids = list(range(1, 256))
        for x in self.objects_sorted:
            if x.battle_id is None or x.battle_id == 0:
                x.battle_id = self.get_next_battle_id()

        self.info_by_battle_id: Dict[int, BattleInfo] = {}
        for x in self.friendly_recruits + self.friendly_relics:
            self.info_by_battle_id[x.battle_id] = BattleInfo(friendly_recruits=self.friendly_recruits,
                                                             friendly_relics=self.friendly_relics,
                                                             friendly_uuid=self.friendly_uuid,
                                                             enemy_recruits=self.enemy_recruits,
                                                             enemy_relics=self.enemy_relics,
                                                             enemy_uuid=self.enemy_uuid)
        for x in self.enemy_recruits + self.enemy_relics:
            self.info_by_battle_id[x.battle_id] = BattleInfo(friendly_recruits=self.enemy_recruits,
                                                             friendly_relics=self.enemy_relics,
                                                             friendly_uuid=self.enemy_uuid,
                                                             enemy_recruits=self.friendly_recruits,
                                                             enemy_relics=self.friendly_relics,
                                                             enemy_uuid=self.friendly_uuid)
    def update_objects_sorted(self):
        self.objects_sorted = []
        self.objects_sorted.extend(self.enemy_recruits)
        self.objects_sorted.extend(self.enemy_relics)
        self.objects_sorted.extend(self.friendly_recruits)
        self.objects_sorted.extend(self.friendly_relics)
        self.objects_sorted = sorted(self.objects_sorted, key=lambda x: x.initiative)
        for x in self.objects_sorted:
            if x.battle_id is None or x.battle_id == 0:
                x.battle_id = self.get_next_battle_id()

        self.info_by_battle_id: Dict[int, BattleInfo] = {}
        for x in self.friendly_recruits + self.friendly_relics:
            self.info_by_battle_id[x.battle_id] = BattleInfo(friendly_recruits=self.friendly_recruits,
                                                             friendly_relics=self.friendly_relics,
                                                             friendly_uuid=self.friendly_uuid,
                                                             enemy_recruits=self.enemy_recruits,
                                                             enemy_relics=self.enemy_relics,
                                                             enemy_uuid=self.enemy_uuid)
        for x in self.enemy_recruits + self.enemy_relics:
            self.info_by_battle_id[x.battle_id] = BattleInfo(friendly_recruits=self.enemy_recruits,
                                                             friendly_relics=self.enemy_relics,
                                                             friendly_uuid=self.enemy_uuid,
                                                             enemy_recruits=self.friendly_recruits,
                                                             enemy_relics=self.friendly_relics,
                                                             enemy_uuid=self.friendly_uuid)

    def get_next_battle_id(self):
        if len(self.battle_ids) == 0:
            raise ValueError("No battle ids left")
        id = self.battle_ids.pop(0)
        return id

    def queue_ability_for(self, trigger: str, objects: list[Union[BaseRelic, BaseRecruit]], context=None,
                          append_left=True):
        objects = sorted(objects, key=lambda x: x.initiative)
        for x in objects:
            if trigger in x.triggers or x.default_triggers:
                item = StackItem(op=trigger, object=x, context=context)
                if append_left:
                    self.stack.appendleft(item)
                else:
                    self.stack.append(item)

    def get_battle_info(self, battle_id: int) -> BattleInfo:
        return self.info_by_battle_id[battle_id]

    def get_object_from_battle_id(self, battle_id: int):
        for x in self.objects_sorted:
            if x.battle_id == battle_id:
                return x

    def remove_recruit_from_battle(self, recruit: BaseRecruit):
        battle_info = self.get_battle_info(recruit.battle_id)
        battle_info.friendly_recruits.pop(recruit.team_index)
        for i, x in enumerate(battle_info.friendly_recruits):
            x.team_index = i
        self.objects_sorted = [x for x in self.objects_sorted if x.battle_id != recruit.battle_id]

    def is_unresolved(self):
        return len(self.enemy_recruits) > 0 and len(self.friendly_recruits) > 0

    def queue_ability_for_all_objects(self, trigger: str, context=None):
        # this approach basically passes things to the objects to handle, so, start of battle is passed to every
        # object and it handles it accordingly
        self.queue_ability_for(trigger=trigger, context=context, objects=self.objects_sorted)

    def queue_default_for_all_objects(self, battle_state: "BattleStateSerializer", state_set: "StateSet", animation_event_sequence: AnimationEventSequence):
        # this approach basically passes things to the objects to handle, so, start of battle is passed to every
        # object and it handles it accordingly
        for x in self.objects_sorted:
            if x.type == "Recruit":
                # is_entangled = x.get_status(sub_type_as_text="EntangledWeb")
                # is_chlorotoxin = x.get_status(sub_type_as_text="Chlorotoxin")
                # if is_chlorotoxin:
                #     e = Animations.ChlorotoxinEffect(state_id=state_set.add_state(battle_state))
                #     animation_event_sequence.append(e)
                #     x.remove_status(status=is_chlorotoxin)
                # elif is_entangled:
                #     e = Animations.EntangledWebEffect(state_id=state_set.add_state(battle_state))
                #     animation_event_sequence.append(e)
                #     stack_item = StackItem(op=GameConstants.Opcodes.Stack.passive_battle_ability, context={}, object=x)
                #     self.stack.appendleft(stack_item)
                #     is_entangled.counter -= 1
                #     if is_entangled.counter <= 0:
                #         x.remove_status(status=is_entangled)
                # else:
                stack_item = StackItem(op=GameConstants.Opcodes.Stack.battle_attack_with_ranged, context={}, object=x)
                self.stack.appendleft(stack_item)
                stack_item = StackItem(op=GameConstants.Opcodes.Stack.battle_attack_with_melee, context={}, object=x)
                self.stack.appendleft(stack_item)
                stack_item = StackItem(op=GameConstants.Opcodes.Stack.passive_battle_ability, context={}, object=x)
                self.stack.appendleft(stack_item)
            elif x.type == "Relic":
                stack_item = StackItem(op=GameConstants.Opcodes.Stack.battle_attack_with_ranged, context={}, object=x)
                self.stack.appendleft(stack_item)
                stack_item = StackItem(op=GameConstants.Opcodes.Stack.battle_attack_with_melee, context={}, object=x)
                self.stack.appendleft(stack_item)
                stack_item = StackItem(op=GameConstants.Opcodes.Stack.passive_battle_ability, context={}, object=x)
                self.stack.appendleft(stack_item)
            # logically last item occurs first

    def calculate_winner(self):
        result = {}
        remaining_friendly_recruits = [x for x in self.friendly_recruits if x.health > 0]
        remaining_enemy_recruits = [x for x in self.enemy_recruits if x.health > 0]
        if len(remaining_friendly_recruits) > len(remaining_enemy_recruits):
            return GameConstants.Battle.won
        elif len(remaining_friendly_recruits) < len(remaining_enemy_recruits):
            return GameConstants.Battle.lost
        elif len(remaining_friendly_recruits) == len(remaining_enemy_recruits):
            return GameConstants.Battle.draw

    def __str__(self):
        pass
