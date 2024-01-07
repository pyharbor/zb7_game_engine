import json
from collections import defaultdict
from pathlib import Path
from typing import List

from pyharbor_shared_library.Date import Date
from pyharbor_shared_library.Disk import Disk

from __deprecated.artists import artists
from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature


class NewFile:
    def __init__(self, sub_type_as_text: str, path: Path, artist_alias: str, artists_social_media: str, aaid: str):
        self.sub_type_as_text = sub_type_as_text
        self.path = path
        self.artist_alias = artist_alias
        self.artists_social_media = artists_social_media
        self.aaid = aaid
        self.item_id = self.sub_type_as_text + "_" + self.aaid
        self.immutable_data = ImmutableData.Subtype.from_text(subtype_as_text=sub_type_as_text)


class HandleNewArts:
    @staticmethod
    def update_sub_types_json(objects: list[NewFile]):
        for o in objects:
            if not o.path.name.endswith("_large.png"):
                continue
            print(
                f"check: {o.sub_type_as_text.ljust(20)} {o.aaid.ljust(4)} {o.artist_alias.ljust(20)} {o.artists_social_media} {o.path.name}")
            for x in sub_types:
                if x['sub_type_as_text'] == o.sub_type_as_text:
                    for art in x['arts']:
                        if art['item_id'] == o.item_id and art['alias'] is not None and art['social_info'] is not None:
                            raise Exception(f"item_id {o.item_id} == {art['item_id']}, should be unique")
                    print(f"add:   {o.sub_type_as_text.ljust(20)} "
                          f"{o.aaid.ljust(4)} {o.artist_alias.ljust(20)} "
                          f"{o.artists_social_media}"
                          f" {o.path.name}")
                    x['arts'].append({
                        "item_id": o.item_id,
                        "alias": o.artist_alias,
                        "social_info": o.artists_social_media,
                    })
        Disk.Sync.write_file_text(data=json.dumps(sub_types, indent=4),
                                  filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")

    @staticmethod
    def copy_files_to_scientific_and_artist_locations(objects: List[NewFile]):
        parent_path = "/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts"
        for o in objects:
            if o.immutable_data['type'] == "Recruit":
                x = BinomialNomenclature.from_json(o.immutable_data['binomial_nomenclature'])
                species = x.get_main_species()
                scientific_path = f"{parent_path}/recruits/{species}/{o.sub_type_as_text}/{o.path.name}"
                artist_path = f"{parent_path}/artists/{o.artist_alias}/{o.path.name}"
                print(f"copy: {o.path.name} -> {scientific_path}")
                print(f"copy: {o.path.name} -> {artist_path}")
                Disk.Sync.write_file_bytes(data=o.path.read_bytes(), filename=scientific_path)
                Disk.Sync.write_file_bytes(data=o.path.read_bytes(), filename=artist_path)
            elif o.immutable_data['type'] == "Relic":
                scientific_path = f"{parent_path}/relics/{o.sub_type_as_text[0]}/{o.sub_type_as_text}/{o.path.name}"
                artist_path = f"{parent_path}/artists/{o.artist_alias}/{o.path.name}"
                print(f"copy: {o.path.name} -> {scientific_path}")
                print(f"copy: {o.path.name} -> {artist_path}")
                Disk.Sync.write_file_bytes(data=o.path.read_bytes(), filename=scientific_path)
                Disk.Sync.write_file_bytes(data=o.path.read_bytes(), filename=artist_path)

    @staticmethod
    def update_artists_and_animals_text_files(sub_types):
        artist_info = defaultdict(list)
        for x in sub_types:
            if x["type"] == "Recruit":
                for alt_art in x["arts"]:
                    artist_info[alt_art["alias"]].append(alt_art["item_id"])
        artist_text = []
        for artist, item_ids in artist_info.items():
            artist_text.append(f"{artist} total={len(item_ids)}")
            for i, item_id in enumerate(item_ids):
                artist_text.append(f"    {str(i + 1).ljust(3)} {item_id}")
            artist_text.append("\n")
        Disk.Sync.write_file_text(data="\n".join(artist_text),
                                  filename=f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/artists.txt")

        animals_list = ["Animals List"]
        header = "1   name                           species              rarity     alt art count      artists who have contributed"
        animals_list.append(header)

        def sort_by_species(x):
            if x["type"] == "Recruit":
                binomial_nomenclature = BinomialNomenclature.from_json(x["binomial_nomenclature"])
                species = binomial_nomenclature.get_main_species()
                return species
            else:
                return "None"

        def sort_by_number_of_alt_arts(x):
            if x["type"] == "Recruit":
                return len(x['arts'])
            else:
                return 0

        recruits_sorted_by_species = sorted(list(sub_types), key=lambda x: sort_by_species(x))
        recruits_sorted_by_species = [x for x in recruits_sorted_by_species if x["type"] == "Recruit"]

        recruits_sorted_by_number_of_alt_arts = sorted(sub_types, key=lambda x: sort_by_number_of_alt_arts(x))
        recruits_sorted_by_number_of_alt_arts = [x for x in recruits_sorted_by_number_of_alt_arts if
                                                 x["type"] == "Recruit"]

        for i, x in enumerate(recruits_sorted_by_species):
            if x["type"] == "Recruit":
                binomial_nomenclature = BinomialNomenclature.from_json(x["binomial_nomenclature"])
                species = [x for x in binomial_nomenclature.flatten_and_prune() if x not in ["Insecta", "Carnivora"]][0]
                alt_count = str(len(x['arts'])).ljust("alt art count      ".__len__())
                artists = [y['alias'] for y in x['arts']]
                animals_list.append(
                    f"{str(i + 1).ljust(3)} {x['sub_type_as_text'].ljust(30)} {species.ljust(20)} {x['rarity'].ljust(10)} {alt_count} {artists}")
        Disk.Sync.write_file_text(data="\n".join(animals_list),
                                  filename=f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/animal_list_sorted_by_species.txt")

        animals_list = ["Animals List"]
        header = "1   name                           species              rarity     alt art count      artists who have contributed"
        animals_list.append(header)
        for i, x in enumerate(recruits_sorted_by_number_of_alt_arts):
            if x["type"] == "Recruit":
                binomial_nomenclature = BinomialNomenclature.from_json(x["binomial_nomenclature"])
                species = [x for x in binomial_nomenclature.flatten_and_prune() if x not in ["Insecta", "Carnivora"]][0]
                alt_count = str(len(x['arts'])).ljust("alt art count      ".__len__())
                artists = [y['alias'] for y in x['arts']]
                animals_list.append(
                    f"{str(i + 1).ljust(3)} {x['sub_type_as_text'].ljust(30)} {species.ljust(20)} {x['rarity'].ljust(10)} {alt_count} {artists}")
        Disk.Sync.write_file_text(data="\n".join(animals_list),
                                  filename=f"/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/animal_list_sorted_by_alt_art_count.txt")

    @staticmethod
    def generate_new_art_pack():
        today = Date.US_Eastern.now_str(format='%Y-%m-%d')
        artists_files = [x for x in Disk.Sync.rglob(
            directory="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/artists/")
                         if x.is_file() and x.name != ".DS_Store"]
        recruit_files = [x for x in Disk.Sync.rglob(
            directory="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/recruits/")
                         if x.is_file() and x.name != ".DS_Store"]
        relic_files = [x for x in Disk.Sync.rglob(
            directory="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/relics/")
                       if x.is_file() and x.name != ".DS_Store"]
        statuses = [x for x in Disk.Sync.rglob(
            directory="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/statuses/")
                    if x.is_file() and x.name != ".DS_Store"]
        animal_list_1 = Path(
            "/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/animal_list_sorted_by_alt_art_count.txt")
        animal_list_2 = Path(
            "/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/animal_list_sorted_by_species.txt")
        artist_list = Path(
            "/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/artists.txt")
        overview = Path(
            "/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/overview.txt")
        Disk.Sync.write_file_bytes(data=animal_list_1.read_bytes(),
                                   filename=f"/Users/jacobsanders/Desktop/art_packs/{today}/animal_list_sorted_by_alt_art_count.txt")
        Disk.Sync.write_file_bytes(data=animal_list_2.read_bytes(),
                                   filename=f"/Users/jacobsanders/Desktop/art_packs/{today}/animal_list_sorted_by_species.txt")
        Disk.Sync.write_file_bytes(data=artist_list.read_bytes(),
                                   filename=f"/Users/jacobsanders/Desktop/art_packs/{today}/artists.txt")
        Disk.Sync.write_file_bytes(data=overview.read_bytes(),
                                   filename=f"/Users/jacobsanders/Desktop/art_packs/{today}/overview.txt")
        for x in artists_files:
            relative_path = "/".join(x.parts[-2:])
            Disk.Sync.write_file_bytes(data=x.read_bytes(),
                                       filename=f"/Users/jacobsanders/Desktop/art_packs/{today}/artists/{relative_path}")

        for x in recruit_files:
            relative_path = "/".join(x.parts[-3:])
            Disk.Sync.write_file_bytes(data=x.read_bytes(),
                                       filename=f"/Users/jacobsanders/Desktop/art_packs/{today}/recruits/{relative_path}")
        for x in relic_files:
            relative_path = "/".join(x.parts[-2:])
            Disk.Sync.write_file_bytes(data=x.read_bytes(),
                                       filename=f"/Users/jacobsanders/Desktop/art_packs/{today}/relics/{relative_path}")
        for x in statuses:
            Disk.Sync.write_file_bytes(data=x.read_bytes(),
                                       filename=f"/Users/jacobsanders/Desktop/art_packs/{today}/statuses/{x.name}")

    @staticmethod
    def reset_artists_directory(sub_types):
        parent_path = "/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts"
        for x in sub_types:
            if x['type'] != "Recruit":
                continue
            b = BinomialNomenclature.from_json(x['binomial_nomenclature'])
            sub_type_as_text = x['sub_type_as_text']
            species = b.get_main_species()
            for a in x['arts']:
                alias = a['alias']
                item_id = a['item_id']
                scientific_path = f"{parent_path}/recruits/{species}/{sub_type_as_text}/{item_id}_large.png"
                artist_path = f"{parent_path}/artists/{alias}/{item_id}_large.png"
                Disk.Sync.write_file_bytes(data=Path(scientific_path).read_bytes(), filename=artist_path)

    @staticmethod
    def update_overview_text_files(sub_types: list):
        by_main_species = {}
        total_number_of_arts = 0
        artists = set()
        text = []
        species_count = {}
        for x in sub_types:
            if x['type'] == "Status":
                continue
            species_count.setdefault(x.get('main_species', "Relic"), []).append(x)
            for a in x['arts']:
                by_main_species.setdefault(x.get('main_species', "Relic"), []).append(a)
                total_number_of_arts += 1
                artists.add(a['alias'])
        text.append(f"Total number of arts: {total_number_of_arts}")
        text.append(f"Total number of artists: {artists.__len__()}")
        text.append(f"Artists: {artists.__len__()}")
        for x in artists:
            text.append(f"\t{x}")
        text.append(f"Species:")
        for k, v in sorted(by_main_species.items(), key=lambda x: x[1].__len__() / species_count[x[0]].__len__(), reverse=True):
            if k == "Relic":
                continue
            text.append(f"""\t{k}:  
        alt_arts: {v.__len__()} 
        sub_types: {species_count[k].__len__()}
        ratio: {v.__len__() / species_count[k].__len__()}""")
        text.append(f"""Relics:  
    alt_arts: {by_main_species['Relic'].__len__()}
    sub_types: {species_count['Relic'].__len__()}
    ratio: {by_main_species['Relic'].__len__() / species_count['Relic'].__len__()}""")

        Disk.Sync.write_file_bytes(data="\n".join(text).encode("utf-8"),
                                   filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/overview.txt")


if __name__ == "__main__":
    sub_types = Disk.Sync.load_file_json(
        filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")
    new_files = [x for x in Disk.Sync.rglob(
        directory="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/assets/arts/__script")
                 if x.is_file() and x.name != ".DS_Store"]
    objects = []
    for x in new_files:
        sub_type_as_text = x.name.split("_")[0]
        aaid = x.name.split("_")[1]
        obj = NewFile(sub_type_as_text=sub_type_as_text,
                      aaid=aaid,
                      path=x,
                      artist_alias=artists[x.parent.name]['alias'],
                      artists_social_media=artists[x.parent.name]['social_info'])
        objects.append(obj)


    HandleNewArts.update_sub_types_json(objects=objects)
    HandleNewArts.copy_files_to_scientific_and_artist_locations(objects=objects)
    HandleNewArts.update_artists_and_animals_text_files(sub_types=sub_types)
    HandleNewArts.update_overview_text_files(sub_types=sub_types)
    HandleNewArts.generate_new_art_pack()
    # HandleNewArts.reset_artists_directory(sub_types=sub_types)

    total_number_of_arts = 0
    for x in sub_types:
        if x['type'] != "Recruit":
            continue
        for a in x['arts']:
            total_number_of_arts += 1
    print(f"Total number of arts: {total_number_of_arts}")

