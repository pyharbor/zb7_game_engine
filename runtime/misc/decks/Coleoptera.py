from zb7_game_engine.runtime.objects.recruits.Recruits import Recruits
from zb7_game_engine.runtime.objects.relics.Relics import Relics
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer


class Coleoptera:
    deck = DeckSerializer(
        objects=[
            Recruits.Coleoptera.Firefly(),
            Recruits.Coleoptera.LadyBug(),
            Recruits.Coleoptera.DungBeetle(),
            Recruits.Coleoptera.SpiderBeetle(),
            Recruits.Coleoptera.GiraffeBeetle(),
            Recruits.Coleoptera.BombardierBeetle(),
            Recruits.Coleoptera.GoliathBeetle(),
            Recruits.Coleoptera.HerculesBeetle(),
            Recruits.Coleoptera.LonghornBeetle(),
            Recruits.Hymenoptera.FireAnt(),

            Recruits.Arachnida.SixEyedSandSpider(),
            Recruits.Arachnida.JumpingSpider(),
            Recruits.Arachnida.AnelosimusEximius(),
            Recruits.Arachnida.AsianForestScorpion(),
            Recruits.Arachnida.DeathWalkerScorpion(),
            Recruits.Arachnida.DesertTarantula(),

            Relics.PinkOpal(),
            Relics.SunScreen(),
            Relics.RustedAnchor(),
            Relics.AmberAmulet(),
            Relics.ProtectiveCanopy(),
            Relics.PerfectCopy(),
            Relics.GraduationCap(),
            Relics.GeneEditing(),
            Relics.Fountain(),
            Relics.VitaminWater(),
        ]
    )


if __name__ == "__main__":
    d = DeckSerializer.from_base64_text(Coleoptera.deck.to_base64_text())
    print(d.to_base64_text())
    print(Coleoptera.deck.to_base64_text())
    Coleoptera.deck.validate_custom_deck()
