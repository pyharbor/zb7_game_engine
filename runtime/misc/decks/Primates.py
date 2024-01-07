from zb7_game_engine.runtime.objects.recruits.Recruits import Recruits
from zb7_game_engine.runtime.objects.relics.Relics import Relics
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer


class Primates:
    deck = DeckSerializer(
        objects=[
            Recruits.Primates.Bonobo(),
            Recruits.Primates.Baboon(),
            Recruits.Primates.Mandrill(),
            Recruits.Primates.LarGibon(),
            Recruits.Primates.HowlerMonkey(),
            Recruits.Primates.EasternGorilla(),
            Recruits.Primates.ProboscisMonkey(),
            Recruits.Primates.Chimpanzee(),
            Recruits.Primates.Orangutan(),
            Recruits.Primates.NoselessMonkey(),

            Recruits.Amphibia.TreeFrog(),
            Recruits.Amphibia.GoldenPoisonFrog(),
            Recruits.Amphibia.Axolotl(),
            Recruits.Arachnida.AsianForestScorpion(),
            Recruits.Amphibia.PoisonDartFrog(),
            Recruits.Arachnida.DesertTarantula(),

            Relics.PinkOpal(),
            Relics.Fork(),
            Relics.AmazonPrime(),
            Relics.RubyRock(),
            Relics.ProtectiveCanopy(),
            Relics.PerfectCopy(),
            Relics.GraduationCap(),
            Relics.GeneEditing(),
            Relics.Fountain(),
            Relics.VitaminWater(),
        ]
    )


if __name__ == "__main__":
    d = DeckSerializer.from_base64_text(Primates.deck.to_base64_text())
    print(d.to_base64_text())
    print(Primates.deck.to_base64_text())
    Primates.deck.validate_custom_deck()
