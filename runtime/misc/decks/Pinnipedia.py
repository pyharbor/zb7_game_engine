from zb7_game_engine.runtime.objects.recruits.Recruits import Recruits
from zb7_game_engine.runtime.objects.relics.Relics import Relics
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer


class Pinnipedia:
    deck = DeckSerializer(
        objects=[
            Recruits.Pinnipedia.FurSeal(),
            Recruits.Pinnipedia.Walrus(),
            Recruits.Pinnipedia.HarpSeal(),
            Recruits.Pinnipedia.BeardedSeal(),
            Recruits.Pinnipedia.ElephantSeal(),
            Recruits.Pinnipedia.LepoardSeal(),
            Recruits.Pinnipedia.SouthAmericanSeaLion(),
            Recruits.Pinnipedia.CrabEaterSeal(),
            Recruits.Pinnipedia.SeaOtter(),

            Recruits.Reptilia.LeatherbackSeaTurtle(),
            Recruits.Ursidae.GrizzlyBear(),
            Recruits.Cetacea.Dolphin(),
            Recruits.Ursidae.GiantPanda(),
            Recruits.Ursidae.PolarBear(),
            Recruits.Diprotodontia.Koala(),
            Recruits.Arachnida.DesertTarantula(),

            Relics.PinkOpal(),
            Relics.Fork(),
            Relics.AmazonPrime(),
            Relics.AmberAmulet(),
            Relics.ProtectiveCanopy(),
            Relics.PerfectCopy(),
            Relics.GraduationCap(),
            Relics.PlasmaShield(),
            Relics.Fountain(),
            Relics.VitaminWater(),
        ]
    )


if __name__ == "__main__":
    d = DeckSerializer.from_base64_text(Pinnipedia.deck.to_base64_text())
    print(d.to_base64_text())
    print(Pinnipedia.deck.to_base64_text())
    Pinnipedia.deck.validate_custom_deck()
