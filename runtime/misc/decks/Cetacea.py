from zb7_game_engine.runtime.objects.recruits.Recruits import Recruits
from zb7_game_engine.runtime.objects.relics.Relics import Relics
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer


class Cetacea:
    deck = DeckSerializer(
        objects=[
            Recruits.Cetacea.BlueWhale(),
            Recruits.Chondrichthyes.WhaleShark(),
            Recruits.Cetacea.Dolphin(),
            Recruits.Cetacea.BaleenWhale(),
            Recruits.Cetacea.BelugaWhale(),
            Recruits.Cetacea.BowheadWhale(),
            Recruits.Cetacea.Orca(),
            Recruits.Cetacea.Narwhal(),
            Recruits.Cetacea.SpermWhale(),
            Recruits.Cetacea.PilotWhale(),
            Recruits.Cetacea.AmazonRiverDolphin(),
            Recruits.Hippopotamidae.Hippopotamus(),


            Recruits.Reptilia.RainbowAgama(),
            Recruits.Reptilia.NileCrocodile(),
            Recruits.Reptilia.BurmesePython(),
            Recruits.Arachnida.DesertTarantula(),

            Relics.PinkOpal(),
            Relics.Fork(),
            Relics.AmazonPrime(),
            Relics.AmberAmulet(),
            Relics.LivyatanFossil(),
            Relics.PerfectCopy(),
            Relics.GraduationCap(),
            Relics.GeneEditing(),
            Relics.Fountain(),
            Relics.VitaminWater(),
        ]
    )


if __name__ == "__main__":
    d = DeckSerializer.from_base64_text(Cetacea.deck.to_base64_text())
    print(d.to_base64_text())
    print(Cetacea.deck.to_base64_text())
    Cetacea.deck.validate_custom_deck()
