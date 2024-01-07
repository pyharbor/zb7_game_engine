from zb7_game_engine.runtime.objects.recruits.Recruits import Recruits
from zb7_game_engine.runtime.objects.relics.Relics import Relics
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer


class Polyneoptera:
    deck = DeckSerializer(
        objects=[
            Recruits.Mantodea.OrchidMantis(),
            Recruits.Mantodea.EuropeanMantis(),
            Recruits.Mantodea.ShieldMantis(),
            Recruits.Blattodea.HissingCockroach(),
            Recruits.Orthoptera.Katydid(),
            Recruits.Orthoptera.DesertLocust(),
            Recruits.Orthoptera.MoleCricket(),
            Recruits.Phasmatodea.LeafInsect(),
            Recruits.Phasmatodea.GiantWalkingStick(),

            Recruits.Arachnida.AsianForestScorpion(),
            Recruits.Arachnida.DesertTarantula(),
            Recruits.Arachnida.SixEyedSandSpider(),
            Recruits.Arachnida.BrownRecluseSpider(),
            Recruits.Crustacea.CoconutCrab(),
            Recruits.Arachnida.CrabSpider(),
            Recruits.Hymenoptera.VelvetAnt(),



            Relics.PinkOpal(),
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
    # base64_str = "4wyIQBgAAACQB/AAAEuAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQQDAAAAAgAKAAAAAAAAAAAAAAAAAAA="
    base64_text = "AKgAAMkAAAcAAA4AALMAABAAALYAAA0AAG8AAAsAAHIAANAAAM4AAHQAAK0AAHUAAG4AAHMAAHYAAHEAAMoAAHAAAAwAANgAABYAANMA"
    d = DeckSerializer.from_base64_text(Polyneoptera.deck.to_base64_text())
    print(d.to_base64_text())
    print(Polyneoptera.deck.to_base64_text(), len(Polyneoptera.deck.to_base64_text()))
    Polyneoptera.deck.validate_custom_deck()
    for x in d.objects:
        print(x.sub_type_as_text.ljust(30), x.aaid)
