from zb7_game_engine.runtime.objects.recruits.Recruits import Recruits
from zb7_game_engine.runtime.objects.relics.Relics import Relics
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer


class Aves:
    deck = DeckSerializer(
        objects=[
            Recruits.Aves.Chickadee(),
            Recruits.Aves.ArcticTern(),
            Recruits.Aves.GoldenEagle(),
            Recruits.Aves.WanderingAlbatross(),
            Recruits.Aves.AndeanCondor(),
            Recruits.Aves.BurrowingOwl(),
            Recruits.Aves.GriffonVulture(),
            Recruits.Aves.RedBilledQuelea(),
            Recruits.Aves.GreaterFlamingo(),
            Recruits.Aves.EmperorPenguin(),
            Recruits.Aves.MacaroniPenguin(),
            Recruits.Aves.ShoeBill(),

            Recruits.Reptilia.LeatherbackSeaTurtle(),
            Recruits.Reptilia.RainbowAgama(),
            Recruits.Reptilia.NileCrocodile(),
            Recruits.Cetacea.Dolphin(),

            Relics.Dice(),
            Relics.Fork(),
            Relics.AmazonPrime(),
            Relics.AmberAmulet(),
            Relics.ProtectiveCanopy(),
            Relics.PerfectCopy(),
            Relics.GraduationCap(),
            Relics.TropicalThunderstorm(),
            Relics.Fountain(),
            Relics.VitaminWater(),
        ]
    )


if __name__ == "__main__":
    d = DeckSerializer.from_base64_text(Aves.deck.to_base64_text())
    print(d.to_base64_text())
    print(Aves.deck.to_base64_text())
    Aves.deck.validate_custom_deck()
