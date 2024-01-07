from zb7_game_engine.runtime.objects.recruits.Recruits import Recruits
from zb7_game_engine.runtime.objects.relics.Relics import Relics
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer


class Crustacea:
    deck = DeckSerializer(
        objects=[
            Recruits.Crustacea.Krill(),
            Recruits.Crustacea.CoconutCrab(),
            Recruits.Crustacea.HermitCrab(),
            Recruits.Crustacea.BlackClawedCrab(),
            Recruits.Crustacea.AlaskanKingCrab(),
            Recruits.Crustacea.HarlequinLandCrab(),
            Recruits.Crustacea.TasmanianGiantCrab(),
            Recruits.Crustacea.JapaneseSpiderCrab(),
            Recruits.Crustacea.GiantIsopod(),
            Recruits.Crustacea.AmericanLobster(),

            Recruits.Reptilia.LeatherbackSeaTurtle(),
            Recruits.Reptilia.GreenAnaconda(),
            Recruits.Reptilia.RainbowAgama(),
            Recruits.Reptilia.AldabraGiantTortoise(),
            Recruits.Reptilia.NileCrocodile(),
            Recruits.Arachnida.DesertTarantula(),

            Relics.SapphireShell(),
            Relics.SunScreen(),
            Relics.AmazonPrime(),
            Relics.PlasmaShield(),
            Relics.ProtectiveCanopy(),
            Relics.PerfectCopy(),
            Relics.GraduationCap(),
            Relics.Sandstorm(),
            Relics.Fountain(),
            Relics.RubyRock(),
        ]
    )


if __name__ == "__main__":
    d = DeckSerializer.from_base64_text(Crustacea.deck.to_base64_text())
    print(d.to_base64_text())
    print(Crustacea.deck.to_base64_text())
    Crustacea.deck.validate_custom_deck()
