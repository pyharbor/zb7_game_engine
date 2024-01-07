from zb7_game_engine.runtime.objects.recruits.Recruits import Recruits
from zb7_game_engine.runtime.objects.relics.Relics import Relics
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer


class Reptilia:
    deck = DeckSerializer(
        objects=[
            Recruits.Reptilia.LeatherbackSeaTurtle(),
            Recruits.Reptilia.BurmesePython(),
            Recruits.Reptilia.NileCrocodile(),
            Recruits.Reptilia.GreenAnaconda(),
            Recruits.Reptilia.RainbowAgama(),
            Recruits.Reptilia.ToadFacedTurtle(),
            Recruits.Reptilia.SaltwaterCrocodile(),
            Recruits.Reptilia.AldabraGiantTortoise(),
            Recruits.Reptilia.AlligatorSnappingTurtle(),
            Recruits.Reptilia.EasternBoxTurtle(),

            Recruits.Amphibia.Axolotl(),
            Recruits.Amphibia.TreeFrog(),
            Recruits.Reptilia.KomodoDragon(),
            Recruits.Amphibia.AfricanBullFrog(),
            Recruits.Reptilia.BlackMamba(),
            Recruits.Amphibia.PoisonDartFrog(),

            Relics.SapphireShell(),
            Relics.LightningRaigeki(),
            Relics.AmazonPrime(),
            Relics.RubyRock(),
            Relics.ProtectiveCanopy(),
            Relics.PerfectCopy(),
            Relics.GraduationCap(),
            Relics.Rifle(),
            Relics.ArmorSuit(),
            Relics.SunScreen(),
        ]
    )


if __name__ == "__main__":
    d = DeckSerializer.from_base64_text(Reptilia.deck.to_base64_text())
    print(d.to_base64_text())
    print(Reptilia.deck.to_base64_text())
    Reptilia.deck.validate_custom_deck()
