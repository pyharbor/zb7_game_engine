import json

from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.GameEngine import GameEngine
from zb7_game_engine.runtime.core.RandomEngine import random_engine
from zb7_game_engine.runtime.core.shop_opcodes.ShopUserInput import ShopUserInput
from zb7_game_engine.runtime.misc.debugging.Debug import Debug
from zb7_game_engine.runtime.misc.decks.Decks import Decks
from zb7_game_engine.runtime.objects.recruits.Recruits import Recruits
from zb7_game_engine.runtime.objects.relics.Relics import Relics
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer
from zb7_game_engine.serialization.ShopSnapshotSerializer import ShopSnapshotSerializer
from zb7_game_engine.serialization.player_decision_info.TreasureChestPDInfo import TreasureChestPDInfo


def asdf():
    uuid1 = "1"
    deck = Decks.Polyneoptera.deck
    shop_snapshot = ShopSnapshotSerializer.start_new_run(deck=deck, username="a1", run_uuid=uuid1)
    shop_snapshot.current_state.add_relic(relic=Relics.TreasureChest())
    choices = []
    while len(choices) < 3:
        choice = random_engine.get_random_shop_object(deck=shop_snapshot.deck,
                                                      seed=shop_snapshot.uuid,
                                                      snapshot=shop_snapshot,
                                                      active_relics=shop_snapshot.current_state.friendly_relics,
                                                      filter_callback=lambda x: x.rarity == "Rare")
        choice.shop_id = shop_snapshot.current_state.get_next_shop_id()
        choices.append(choice)
    shop_snapshot.player_decision_info = TreasureChestPDInfo(shop_id=shop_snapshot.friendly_relics[0].shop_id, items=choices)
    s = ShopUserInput(op=GameConstants.Opcodes.Shop.shop_player_decision,
                      player_decision_choice=shop_snapshot.player_decision_info.items[0])
    Debug.ShopSnapshotSerializer.print(shop_snapshot)

    GameEngine.reconcile_shop_user_input(shop_snapshot=shop_snapshot, user_input=s)
    shop_snapshot = ShopSnapshotSerializer.from_json(shop_snapshot.to_json())
    Debug.ShopSnapshotSerializer.print(shop_snapshot)

    print(shop_snapshot.to_json())
    print(len(json.dumps(shop_snapshot.to_json()).encode("utf-8")))


if __name__ == "__main__":
    asdf()
