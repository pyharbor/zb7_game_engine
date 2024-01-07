from collections import defaultdict

from zb7_game_engine.runtime.core.GameConstants import GameConstants


class BinomialNomenclature:
    def __init__(self, kingdom: list[str], phylum: list[str], nomenclature_class: list[str], order: list[str],
                 family: list[str], genus: list[str], species: list[str], clades: list[str] = None):
        self.kingdom = kingdom
        self.phylum = phylum
        self.nomenclature_class = nomenclature_class
        self.order = order
        self.family = family
        self.genus = genus
        self.species = species
        self.clades = clades or []
        self.added_types = []
        self._dict = defaultdict(int)
        for x in self.flatten_and_prune():
            self._dict[x] += 1

    def add_types(self, type_name: list[str]):
        self.added_types.extend(type_name)
        for x in type_name:
            self._dict[x] += 1

    def remove_type(self, type_name: str):
        self.added_types.remove(type_name)
        self._dict[type_name] -= 1
        if self._dict[type_name] == 0:
            del self._dict[type_name]

    def append_type(self, type_name: str):
        self.added_types.append(type_name)
        self._dict[type_name] += 1

    def add_habitats(self, type_name: list[str]):
        self.added_types.extend(type_name)
        for x in type_name:
            self._dict[x] += 1

    def to_json(self):
        return {
            "kingdom": self.kingdom,
            "phylum": self.phylum,
            "nomenclature_class": self.nomenclature_class,
            "order": self.order,
            "family": self.family,
            "genus": self.genus,
            "species": self.species,
            "clades": self.clades,
        }

    def get_main_species(self):
        items = [x for x in self.flatten_and_prune() if x not in ["Insecta", "Carnivora"]]
        return items[0]

    def flatten_and_prune(self):
        flattened = []
        flattened.extend(self.kingdom)
        flattened.extend(self.phylum)
        flattened.extend(self.nomenclature_class)
        flattened.extend(self.order)
        flattened.extend(self.family)
        flattened.extend(self.genus)
        flattened.extend(self.species)
        flattened.extend(self.clades)
        flattened.extend(self.added_types)
        return [x for x in flattened if x in GameConstants.ScientificNames.__dict__.keys() or x in GameConstants.Habitats.__dict__.keys()]

    @staticmethod
    def from_json(json: dict):
        return BinomialNomenclature(
            kingdom=json["kingdom"],
            phylum=json["phylum"],
            nomenclature_class=json["nomenclature_class"],
            order=json["order"],
            family=json["family"],
            genus=json["genus"],
            species=json["species"],
            clades=json["clades"]
        )

    def __contains__(self, item):
        return item in self._dict
