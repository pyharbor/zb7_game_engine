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
    friendly_shop_snapshot = ShopSnapshotSerializer.start_new_run(deck=deck, username="a1", run_uuid=uuid1)
    enemy_shop_snapshot = ShopSnapshotSerializer.start_new_run(deck=deck, username="a2", run_uuid=uuid1)
    friendly_shop_snapshot.current_state.add_recruit(recruit=Recruits.Amphibia.RoughSkinnedNewt(experience=GameConstants.Levels.level_5), index=0)
    friendly_shop_snapshot.current_state.add_recruit(recruit=Recruits.Amphibia.Axolotl(), index=1)
    friendly_shop_snapshot.current_state.add_recruit(recruit=Recruits.Amphibia.Axolotl(), index=2)

    enemy_shop_snapshot.current_state.add_recruit(recruit=Recruits.Arachnida.AsianForestScorpion(), index=0)
    
    # Battle
    battle_snapshot = GameEngine.reconcile_battle(friendly_shop_snapshot=friendly_shop_snapshot, enemy_shop_snapshot=enemy_shop_snapshot)
    print(Debug.BattleSnapshotSerializer.print(battle_snapshot))
    print(battle_snapshot.to_json())
    print(len(json.dumps(battle_snapshot.to_json()).encode("utf-8")))
    
    # Shop Start of turn
    # battle_snapshot = GameEngine.reconcile_shop_user_input(
    #     shop_snapshot=friendly_shop_snapshot, user_input=ShopUserInput(op=GameConstants.Opcodes.Stack.shop_start_of_turn),
    # )
    # print(Debug.ShopSnapshotSerializer.print(friendly_shop_snapshot))
    # print(friendly_shop_snapshot.to_json())
    # print(len(json.dumps(friendly_shop_snapshot.to_json()).encode("utf-8")))
    
    # Shop End of turn
    # GameEngine.reconcile_shop_user_input(
    #     shop_snapshot=friendly_shop_snapshot,
    #     user_input=ShopUserInput(op=GameConstants.Opcodes.Stack.shop_end_of_turn),
    # )
    # print(Debug.ShopSnapshotSerializer.print(friendly_shop_snapshot))
    # print(friendly_shop_snapshot.to_json())
    # print(len(json.dumps(friendly_shop_snapshot.to_json()).encode("utf-8")))
    # print(Debug.ShopSnapshotSerializer.print(friendly_shop_snapshot))


if __name__ == "__main__":
    asdf()
