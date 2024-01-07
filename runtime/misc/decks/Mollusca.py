from zb7_game_engine.runtime.objects.recruits.Recruits import Recruits
from zb7_game_engine.runtime.objects.relics.Relics import Relics
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer


class Mollusca:
    deck = DeckSerializer(
        objects=[
            Recruits.Mollusca.Nautilus(),
            Recruits.Mollusca.Cuttlefish(),
            Recruits.Mollusca.GiantClam(),
            Recruits.Mollusca.GiantSquid(),
            Recruits.Mollusca.GiantPacificOctopus(),
            Recruits.Mollusca.GiantAfricanSnail(),
            Recruits.Mollusca.VampireSquid(),
            Recruits.Mollusca.BlueRingedOctopus(),
            Recruits.Mollusca.ConeSnail(),
            Recruits.Mollusca.CaribbeanReefSquid(),
            Recruits.Mollusca.NembrothaAurea(),

            Recruits.Reptilia.LeatherbackSeaTurtle(),
            Recruits.Chondrichthyes.GreatWhiteShark(),
            Recruits.Crustacea.Krill(),
            Recruits.Actinopterygii.AtlanticBluefinTuna(),
            Recruits.Actinopterygii.RoyalGramma(),

            Relics.PinkOpal(),
            Relics.Fork(),
            Relics.MedKit(),
            Relics.AmberAmulet(),
            Relics.RustedAnchor(),
            Relics.PerfectCopy(),
            Relics.GraduationCap(),
            Relics.Rifle(),
            Relics.SapphireShell(),
            Relics.SpitBall(),
        ]
    )


if __name__ == "__main__":
    d = DeckSerializer.from_base64_text(Mollusca.deck.to_base64_text())
    print(d.to_base64_text())
    print(Mollusca.deck.to_base64_text())
    Mollusca.deck.validate_custom_deck()
