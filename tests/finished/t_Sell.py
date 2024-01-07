import json

from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.GameEngine import GameEngine
from zb7_game_engine.runtime.core.shop_opcodes.ShopUserInput import ShopUserInput
from zb7_game_engine.runtime.misc.debugging.Debug import Debug
from zb7_game_engine.runtime.misc.decks.Decks import Decks
from zb7_game_engine.runtime.objects.recruits.Recruits import Recruits
from zb7_game_engine.serialization.DeckSerializer import DeckSerializer
from zb7_game_engine.serialization.ShopSnapshotSerializer import ShopSnapshotSerializer


def asdf():
    uuid1 = "1"
    deck = Decks.Polyneoptera.deck
    shop_snapshot = ShopSnapshotSerializer.start_new_run(deck=deck, username="a1", run_uuid=uuid1)
    r = Recruits.Cetacea.Dolphin()
    shop_snapshot.current_state.add_recruit(recruit=r, index=0)
    s = ShopUserInput(op=GameConstants.Opcodes.Shop.shop_sell,
                      team_object=shop_snapshot.current_state.friendly_recruits[0])
    Debug.ShopSnapshotSerializer.print(shop_snapshot)

    GameEngine.reconcile_shop_user_input(shop_snapshot=shop_snapshot, user_input=s)
    shop_snapshot = ShopSnapshotSerializer.from_json(shop_snapshot.to_json())
    Debug.ShopSnapshotSerializer.print(shop_snapshot)

    print(shop_snapshot.to_json())
    print(len(json.dumps(shop_snapshot.to_json()).encode("utf-8")))

if __name__ == "__main__":
    asdf()
