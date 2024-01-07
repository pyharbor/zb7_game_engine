from zb7_game_engine.runtime.objects.recruits.Recruits import Recruits
from zb7_game_engine.runtime.objects.relics.Relics import Relics
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer


class Amphibia:
    deck = DeckSerializer(
        objects=[
            Recruits.Amphibia.Axolotl(),
            Recruits.Amphibia.TreeFrog(),
            Recruits.Amphibia.GlassFrog(),
            Recruits.Amphibia.JapaneseGiantSalamander(),
            Recruits.Amphibia.RoughSkinnedNewt(),
            Recruits.Amphibia.AfricanBullFrog(),
            Recruits.Amphibia.PoisonDartFrog(),
            Recruits.Amphibia.GoldenPoisonFrog(),
            Recruits.Amphibia.ForestRainFrog(),
            Recruits.Amphibia.BlueSpottedSalamander(),


            Recruits.Reptilia.ToadFacedTurtle(),
            Recruits.Reptilia.AldabraGiantTortoise(),
            Recruits.Reptilia.RainbowAgama(),
            Recruits.Reptilia.GreenAnaconda(),
            Recruits.Reptilia.LeatherbackSeaTurtle(),
            Recruits.Reptilia.NileCrocodile(),


            Relics.PlasmaShield(),
            Relics.NicotinePatch(),
            Relics.AmazonPrime(),
            Relics.AmberAmulet(),
            Relics.ProtectiveCanopy(),
            Relics.PerfectCopy(),
            Relics.ArmorSuit(),
            Relics.Meteor(),
            Relics.Fountain(),
            Relics.VitaminWater(),
        ]
    )


if __name__ == "__main__":
    d = DeckSerializer.from_base64_text(Amphibia.deck.to_base64_text())
    print(d.to_base64_text())
    print(Amphibia.deck.to_base64_text())
    Amphibia.deck.validate_custom_deck()
