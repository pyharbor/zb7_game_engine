from zb7_game_engine.runtime.objects.recruits.Recruits import Recruits
from zb7_game_engine.runtime.objects.relics.Relics import Relics
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer


class Canidae:
    deck = DeckSerializer(
        objects=[
            Recruits.Canidae.Wolf(),
            Recruits.Canidae.BatEaredFox(),
            Recruits.Canidae.AfricanWildDog(),
            Recruits.Ursidae.GiantPanda(),
            Recruits.Ursidae.GrizzlyBear(),
            Recruits.Ursidae.BlackBear(),
            Recruits.Mephitidae.HoodedSkunk(),
            Recruits.Ursidae.PolarBear(),
            Recruits.Diprotodontia.Koala(),
            Recruits.Canidae.ArcticFox(),


            Recruits.Hymenoptera.HoneyPotAnt(),
            Recruits.Pinnipedia.HarpSeal(),
            Recruits.Actinopterygii.SockeyeSalmon(),
            Recruits.Pinnipedia.ElephantSeal(),
            Recruits.Pinnipedia.LepoardSeal(),
            Recruits.Pinnipedia.FurSeal(),

            Relics.PinkOpal(),
            Relics.Fork(),
            Relics.AmazonPrime(),
            Relics.AmberAmulet(),
            Relics.MedKit(),
            Relics.Eruption(),
            Relics.GraduationCap(),
            Relics.LightningRaigeki(),
            Relics.Fountain(),
            Relics.VitaminWater(),
        ]
    )


if __name__ == "__main__":
    d = DeckSerializer.from_base64_text(Canidae.deck.to_base64_text())
    print(d.to_base64_text())
    print(Canidae.deck.to_base64_text())
    Canidae.deck.validate_custom_deck()
