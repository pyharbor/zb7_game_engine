from zb7_game_engine.runtime.objects.recruits.Recruits import Recruits
from zb7_game_engine.runtime.objects.relics.Relics import Relics
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer


class Actinopterygii:
    deck = DeckSerializer(

        objects=[
            Recruits.Actinopterygii.SunFish(),
            Recruits.Actinopterygii.AnglerFish(),
            Recruits.Actinopterygii.PufferFish(),
            Recruits.Actinopterygii.AtlanticBluefinTuna(),
            Recruits.Actinopterygii.AlligatorGar(),
            Recruits.Actinopterygii.Barracuda(),
            Recruits.Actinopterygii.RoyalGramma(),
            Recruits.Actinopterygii.SockeyeSalmon(),
            Recruits.Actinopterygii.AtlanticHerring(),
            Recruits.Actinopterygii.MorayEel(),
            Recruits.Actinopterygii.ElectricEel(),
            Recruits.Actinopterygii.Lionfish(),

            Recruits.Amphibia.Axolotl(),
            Recruits.Chondrichthyes.BullShark(),
            Recruits.Chondrichthyes.GiantOceanicMantaRay(),
            Recruits.Crustacea.Krill(),

            Relics.PinkOpal(),
            Relics.RubyRock(),
            Relics.AnemoneAllies(),
            Relics.AmberAmulet(),
            Relics.GreatBarrierReef(),
            Relics.PerfectCopy(),
            Relics.GraduationCap(),
            Relics.TropicalThunderstorm(),
            Relics.Fountain(),
            Relics.SapphireShell(),
        ]
    )


if __name__ == "__main__":
    d = DeckSerializer.from_base64_text(Actinopterygii.deck.to_base64_text())
    print(d.to_base64_text())
    print(Actinopterygii.deck.to_base64_text())
    Actinopterygii.deck.validate_custom_deck()
