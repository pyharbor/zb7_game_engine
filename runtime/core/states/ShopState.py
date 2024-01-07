import base64
import json
from collections import deque
from typing import List, Union

from zb7_game_engine.runtime.core.StackItem import StackItem
from zb7_game_engine.serialization.EmptySlotSerializer import EmptySlotSerializer
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer


class ShopState:
    def __init__(self,
                 wins: int,
                 health: int,
                 money: int,
                 turn: int,
                 operation_count: int,
                 friendly_recruits: List[Union[RecruitSerializer, EmptySlotSerializer]],
                 friendly_relics: List[RelicSerializer],
                 shop: List[Union[RelicSerializer, RecruitSerializer, EmptySlotSerializer]],
                 ):
        self.wins = wins
        self.health = health
        self.money = money
        self.turn = turn
        self.operation_count = operation_count
        self.player_decision_info = {}

        # for runtime logic
        self.stack: deque[StackItem] = deque()

        # these are packed in lists within json
        self.friendly_recruits = friendly_recruits
        self.friendly_relics = friendly_relics
        self.shop = shop
        self.objects_by_shop_id = {x.shop_id: x for x in self.friendly_recruits + self.friendly_relics}
        self.objects_sorted_by_initiative = sorted(self.objects_by_shop_id.values(), key=lambda x: x.initiative)
        self.shop_ids = list(reversed(range(0, 256)))
        current_shop_ids = set([x.shop_id for x in self.shop + self.friendly_recruits + self.friendly_relics])
        for x in current_shop_ids:
            self.shop_ids.remove(x)

    def update_object_by_shop_id(self, shop_id: int, object: Union[RecruitSerializer, RelicSerializer]):
        for i, x in enumerate(self.friendly_recruits):
            if x.shop_id == shop_id:
                self.friendly_recruits[i] = object
                return
        for i, x in enumerate(self.friendly_relics):
            if x.shop_id == shop_id:
                self.friendly_relics[i] = object
                return

    def filter_empty_slots(self):
        for i, x in enumerate(self.friendly_recruits):
            if isinstance(x, EmptySlotSerializer):
                del self.objects_by_shop_id[x.shop_id]
        self.friendly_recruits = [x for x in self.friendly_recruits if not isinstance(x, EmptySlotSerializer)]
        self.update_team_indices()

    def update_team_indices(self):
        for i, x in enumerate(self.friendly_recruits):
            x.team_index = i

    def add_recruit(self, recruit: RecruitSerializer, index: int = None, shop_id: int = None):
        recruit.team_index = index
        old = self.friendly_recruits[index]
        self.shop_ids.append(old.shop_id)
        self.objects_by_shop_id.pop(old.shop_id)
        if shop_id:
            recruit.shop_id = shop_id
        else:
            recruit.shop_id = self.get_next_shop_id()
        self.friendly_recruits[index] = recruit
        self.objects_by_shop_id[recruit.shop_id] = recruit
        self.objects_sorted_by_initiative = sorted(self.objects_by_shop_id.values(), key=lambda x: x.initiative)

    def add_relic(self, relic: RelicSerializer):
        relic.shop_id = self.get_next_shop_id()
        self.friendly_relics.append(relic)
        self.objects_by_shop_id[relic.shop_id] = relic
        self.objects_sorted_by_initiative = sorted(self.objects_by_shop_id.values(), key=lambda x: x.initiative)

    def get_next_shop_id(self):
        if len(self.shop_ids) == 0:
            raise ValueError("No shop ids left")
        return self.shop_ids.pop()

    def get_object_from_shop_id(self, shop_id: int) -> Union[RecruitSerializer, RelicSerializer]:
        return self.objects_by_shop_id.get(shop_id)

    def replace_empty_slot(self, recruit: RecruitSerializer, recruit_index: int):
        if not isinstance(self.friendly_recruits[recruit_index], EmptySlotSerializer):
            raise ValueError("Cannot set recruit at index, is not empty")
        del self.objects_by_shop_id[self.friendly_recruits[recruit_index].shop_id]
        recruit.team = self
        recruit.team_index = recruit_index
        self.friendly_recruits[recruit_index] = recruit
        self.objects_by_shop_id[recruit.shop_id] = recruit

    def queue_ability_for_all_objects(self, trigger: str, context=None):
        # this approach basically passes things to the objects to handle, so, start of battle is passed to every
        # object and it handles it accordingly
        self.queue_ability_for(trigger=trigger, context=context, objects=self.objects_sorted_by_initiative)

    def queue_ability_for(self, trigger: str, objects: list[Union[RelicSerializer, RecruitSerializer]], context=None):
        objects = sorted(objects, key=lambda x: x.initiative)
        for x in objects:
            if trigger in x.triggers:
                item = StackItem(op=trigger, object=x, context=context)
                self.stack.appendleft(item)

    def revert_to_empty_slot(self, recruit_index: int):
        if isinstance(self.friendly_recruits[recruit_index], EmptySlotSerializer):
            raise ValueError("Cannot revert anything but a recruit to an empty slot")
        target_to_remove = self.friendly_recruits[recruit_index]
        del self.objects_by_shop_id[self.friendly_recruits[recruit_index].shop_id]
        new_empty_slot = EmptySlotSerializer()
        new_empty_slot.team_index = target_to_remove.team_index
        new_empty_slot.shop_id = self.get_next_shop_id()
        self.friendly_recruits[target_to_remove.team_index] = new_empty_slot
        self.objects_by_shop_id[new_empty_slot.shop_id] = new_empty_slot

    def __str__(self):
        return f"ShopState(wins={self.wins}, health={self.health}, money={self.money}, turn={self.turn})"
