import random
import uuid
from datetime import datetime
from typing import Dict, TYPE_CHECKING, List, Union
from pyharbor_shared_library.Date import Date

if TYPE_CHECKING:
    from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
    from zb7_game_engine.serialization.RelicSerializer import RelicSerializer


class RandomEngine:
    def __init__(self):
        self.random_gens_by_seed: Dict[str, random.Random] = {}
        self.expiry_by_seed: Dict[str, datetime] = {}

    def fast_forward(self, seed: str, number_of_repetitions: int = 1):
        if seed not in self.random_gens_by_seed:
            self.random_gens_by_seed[seed] = random.Random(x=seed)
            self.expiry_by_seed[seed] = Date.UTC.from_now_datetime(hours=1)
        for x in range(number_of_repetitions):
            self.random_gens_by_seed[seed].random()

    def get_random_shop_object(self, deck: "Deck", seed: str, snapshot,
                               active_relics: list[str] = None,
                               filter_callback=None) -> Union["RecruitSerializer", "RelicSerializer"]:
        if active_relics is None:
            active_relics = []
        valid_objects = [x for x in deck.objects if x.sub_type_as_text not in active_relics]
        if filter_callback is not None:
            valid_objects = [x for x in valid_objects if filter_callback(x)]
        objects_sum = sum([x.probability for x in valid_objects])
        if seed not in self.random_gens_by_seed:
            self.random_gens_by_seed[seed] = random.Random(x=seed)
            self.expiry_by_seed[seed] = Date.UTC.from_now_datetime(hours=1)
        num = self.random_gens_by_seed[seed].random() * objects_sum
        _sum = 0
        if len(valid_objects) == 0:
            return None
        prev = valid_objects[0]
        for x in valid_objects:
            if _sum > num:
                return prev.__class__(aaid=prev.aaid)
            _sum += x.probability
            prev = x
        if snapshot:
            snapshot.operation_count += 1
        return prev.__class__(aaid=prev.aaid)

    def random_float(self, seed: str, snapshot) -> float:
        if seed not in self.random_gens_by_seed:
            self.random_gens_by_seed[seed] = random.Random(x=seed)
            self.expiry_by_seed[seed] = Date.UTC.from_now_datetime(hours=1)
        if snapshot:
            snapshot.operation_count += 1
        return round(self.random_gens_by_seed[seed].random(), 4)

    def choice(self, _list, seed: str, snapshot):
        if seed not in self.random_gens_by_seed:
            self.random_gens_by_seed[seed] = random.Random(x=seed)
            self.expiry_by_seed[seed] = Date.UTC.from_now_datetime(hours=1)
        if snapshot:
            snapshot.operation_count += 1
        return self.random_gens_by_seed[seed].choice(_list)

    def shuffle(self, shuffle_this_reference, seed: str, snapshot):
        if seed not in self.random_gens_by_seed:
            self.random_gens_by_seed[seed] = random.Random(x=seed)
            self.expiry_by_seed[seed] = Date.UTC.from_now_datetime(hours=1)
        if snapshot:
            snapshot.operation_count += 1
        self.random_gens_by_seed[seed].shuffle(shuffle_this_reference)


random_engine = RandomEngine()