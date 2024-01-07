from zb7_game_engine.runtime.objects.recruits.Recruits import Recruits
from zb7_game_engine.runtime.objects.relics.Relics import Relics
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer


class Hymenoptera:
    deck = DeckSerializer(
        objects=[
            Recruits.Hymenoptera.VelvetAnt(),
            Recruits.Hymenoptera.BullAnt(),
            Recruits.Hymenoptera.QueenAnt(),
            Recruits.Hymenoptera.GhostAnt(),
            Recruits.Hymenoptera.PaperWasp(),
            Recruits.Hymenoptera.EasternBumblebee(),
            Recruits.Hymenoptera.YellowJacket(),
            Recruits.Hymenoptera.CarpenterAnt(),
            Recruits.Arachnida.TarantulaHawk(),
            Recruits.Hymenoptera.HoneyPotAnt(),
            Recruits.Hymenoptera.FireAnt(),
            Recruits.Hymenoptera.BombusPolaris(),

            Recruits.Arachnida.JumpingSpider(),
            Recruits.Arachnida.AnelosimusEximius(),
            Recruits.Arachnida.AsianForestScorpion(),
            Recruits.Arachnida.DeathWalkerScorpion(),

            Relics.PinkOpal(),
            Relics.SapphireShell(),
            Relics.CorrosiveSpit(),
            Relics.Chainsaw(),
            Relics.ProtectiveCanopy(),
            Relics.PerfectCopy(),
            Relics.GraduationCap(),
            Relics.TropicalThunderstorm(),
            Relics.Fountain(),
            Relics.RubyRock(),
        ]
    )


if __name__ == "__main__":
    d = DeckSerializer.from_base64_text(Hymenoptera.deck.to_base64_text())
    print(d.to_base64_text())
    print(Hymenoptera.deck.to_base64_text())
    Hymenoptera.deck.validate_custom_deck()
