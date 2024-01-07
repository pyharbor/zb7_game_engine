from zb7_game_engine.runtime.objects.recruits.Recruits import Recruits
from zb7_game_engine.runtime.objects.relics.Relics import Relics
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer


class Chondrichthyes:
    deck = DeckSerializer(
        objects=[
            Recruits.Chondrichthyes.GreatWhiteShark(),
            Recruits.Chondrichthyes.GreatHammerheadShark(),
            Recruits.Chondrichthyes.WhaleShark(),
            Recruits.Chondrichthyes.TigerShark(),
            Recruits.Chondrichthyes.BullShark(),
            Recruits.Chondrichthyes.NurseShark(),
            Recruits.Chondrichthyes.BaskingShark(),
            Recruits.Chondrichthyes.GiantOceanicMantaRay(),
            Recruits.Chondrichthyes.BlackTipReefShark(),
            Recruits.Chondrichthyes.GreenlandShark(),
            Recruits.Chondrichthyes.ShortTailStingray(),

            Recruits.Cetacea.AmazonRiverDolphin(),
            Recruits.Crustacea.Krill(),
            Recruits.Cetacea.Orca(),
            Recruits.Cetacea.BaleenWhale(),
            Recruits.Crustacea.CoconutCrab(),

            Relics.PinkOpal(),
            Relics.Fork(),
            Relics.AmazonPrime(),
            Relics.AmberAmulet(),
            Relics.ChumBucket(),
            Relics.PerfectCopy(),
            Relics.Chainsaw(),
            Relics.Rifle(),
            Relics.Fountain(),
            Relics.VitaminWater(),
        ]
    )


if __name__ == "__main__":
    d = DeckSerializer.from_base64_text(Chondrichthyes.deck.to_base64_text())
    print(d.to_base64_text())
    print(Chondrichthyes.deck.to_base64_text())
    Chondrichthyes.deck.validate_custom_deck()
