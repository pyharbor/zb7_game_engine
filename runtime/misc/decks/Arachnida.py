from zb7_game_engine.runtime.objects.recruits.Recruits import Recruits
from zb7_game_engine.runtime.objects.relics.Relics import Relics
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer


class Arachnida:
    deck = DeckSerializer(
        objects=[
            Recruits.Arachnida.DesertTarantula(),
            Recruits.Arachnida.CrabSpider(),
            Recruits.Arachnida.BrownRecluseSpider(),
            Recruits.Arachnida.AsianForestScorpion(),
            Recruits.Arachnida.SixEyedSandSpider(),
            Recruits.Arachnida.AnelosimusEximius(),
            Recruits.Arachnida.JumpingSpider(),
            Recruits.Arachnida.DeathWalkerScorpion(),
            Recruits.Arachnida.BandedGardenSpider(),
            Recruits.Arachnida.DivingBellSpider(),

            Recruits.Crustacea.CoconutCrab(),
            Recruits.Crustacea.JapaneseSpiderCrab(),
            Recruits.Crustacea.HarlequinLandCrab(),
            Recruits.Crustacea.TasmanianGiantCrab(),
            Recruits.Crustacea.HermitCrab(),
            Recruits.Crustacea.AlaskanKingCrab(),

            Relics.PinkOpal(),
            Relics.JadeNecklace(),
            Relics.AmazonPrime(),
            Relics.AmberAmulet(),
            Relics.ProtectiveCanopy(),
            Relics.PerfectCopy(),
            Relics.CrystalBall(),
            Relics.MemberShipCard(),
            Relics.Fountain(),
            Relics.SpitBall(),
        ]
    )


if __name__ == "__main__":
    d = DeckSerializer.from_base64_text(Arachnida.deck.to_base64_text())
    print(d.to_base64_text())
    print(Arachnida.deck.to_base64_text())
    Arachnida.deck.validate_custom_deck()
