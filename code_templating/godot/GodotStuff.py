from pyharbor_shared_library.Disk import Disk

from zb7_game_engine.runtime.core.Deck import Deck
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.misc.decks.Decks import Decks
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer

if __name__ == "__main__":
    sub_types = Disk.Sync.load_file_json(
        filename="/Users/jacobsanders/Desktop/PythonProjects/cloud_applications8/git/projects/games/zb7_game_engine/zb7_game_engine/immutable_data/configs/sub_types.json")
    for x in sub_types:
        if x["type"] != "Recruit":
            continue
        if "bytes_to_custom_data" in x["triggers"] or "custom_data_to_bytes" in x["triggers"] or x['sub_type_as_text'] == "Dolphin":
            obj = RecruitSerializer.from_config_json(_json=x)
            obj.shop_id = 1
            if obj.sub_type_as_text == "Dolphin":
                obj.added_types.append(GameConstants.ScientificNames.Arachnida)
                obj.added_habitats.append(GameConstants.Habitats.Alpine)
                obj.melee_attack += 1
            if obj.sub_type_as_text == "Orca":
                obj.custom_data["encountered_types"] = [GameConstants.ScientificNames.Chondrichthyes]
            if obj.sub_type_as_text == "GiantOceanicMantaRay":
                obj.custom_data["counsumption_counter"] = 17
            elif GameConstants.ScientificNames.Primates in obj.binomial_nomenclature:
                obj.custom_data["target"] = 4
                obj.target = 4
            print(str(obj).ljust(120))

    for k, v in Decks.__dict__.items():
        if k.startswith("_"):
            continue
        # print(f'["{k}", "{v.deck.base64_text}"],')
        d = DeckSerializer.from_base64_text(v.deck.base64_text)
        # print([(x.sub_type_as_int, x.aaid) for x in d.objects])
