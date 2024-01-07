import json
from zb7_game_engine.runtime.objects.relics.Relics import Relics
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
    r = Relics.Dice()
    r2 = Recruits.Arachnida.AsianForestScorpion()
    friendly_shop_snapshot.current_state.add_recruit(recruit=r2, index=0)
    friendly_shop_snapshot.current_state.add_relic(relic=r)
    state_id = friendly_shop_snapshot.state_set.add_state(friendly_shop_snapshot.current_state)
    friendly_shop_snapshot.state_id = state_id

    r = Recruits.Arachnida.AsianForestScorpion()
    enemy_shop_snapshot.current_state.add_recruit(recruit=r, index=0)

    # Battle
    # battle_snapshot = GameEngine.reconcile_battle(friendly_shop_snapshot=friendly_shop_snapshot, enemy_shop_snapshot=enemy_shop_snapshot)
    # print(Debug.BattleSnapshotSerializer.print(battle_snapshot))
    # print(battle_snapshot.to_json())
    # print(len(json.dumps(battle_snapshot.to_json()).encode("utf-8")))
    
    # Shop Start of turn
    x1 = ShopSnapshotSerializer.from_json(friendly_shop_snapshot.to_json())
    battle_snapshot = GameEngine.reconcile_shop_user_input(
        shop_snapshot=friendly_shop_snapshot, user_input=ShopUserInput(op=GameConstants.Opcodes.Stack.shop_roll),
    )
    print(Debug.ShopSnapshotSerializer.print(friendly_shop_snapshot))
    x = ShopSnapshotSerializer.from_json(friendly_shop_snapshot.to_json())
    print(len(json.dumps(friendly_shop_snapshot.to_json()).encode("utf-8")))

    battle_snapshot = GameEngine.reconcile_shop_user_input(
        shop_snapshot=friendly_shop_snapshot, user_input=ShopUserInput(op=GameConstants.Opcodes.Stack.shop_roll),
    )
    print(Debug.ShopSnapshotSerializer.print(friendly_shop_snapshot))
    print(len(json.dumps(friendly_shop_snapshot.to_json()).encode("utf-8")))
    
    # Shop End of turn
    # GameEngine.reconcile_shop_user_input(
    #     shop_snapshot=friendly_shop_snapshot,
    #     user_input=ShopUserInput(op=GameConstants.Opcodes.Stack.shop_end_of_turn),
    # )
    # print(Debug.ShopSnapshotSerializer.print(friendly_shop_snapshot))
    # print(friendly_shop_snapshot.to_json())
    # print(len(json.dumps(friendly_shop_snapshot.to_json()).encode("utf-8")))
    # print(Debug.ShopSnapshotSerializer.print(friendly_shop_snapshot))

    # Shop Buy
    # GameEngine.reconcile_shop_user_input(
    #     shop_snapshot=friendly_shop_snapshot,
    #     user_input=ShopUserInput(op=GameConstants.Opcodes.Stack.shop_buy,
    #                              shop_object=friendly_shop_snapshot.current_state.shop[0],
    #                              team_object=friendly_shop_snapshot.current_state.friendly_recruits[1]),
    # )
    # print(Debug.ShopSnapshotSerializer.print(friendly_shop_snapshot))
    # print(friendly_shop_snapshot.to_json())
    # print(len(json.dumps(friendly_shop_snapshot.to_json()).encode("utf-8")))
    
    # Shop Sell
    # GameEngine.reconcile_shop_user_input(
    #     shop_snapshot=friendly_shop_snapshot,
    #     user_input=ShopUserInput(op=GameConstants.Opcodes.Stack.shop_sell,
    #                              team_object=friendly_shop_snapshot.current_state.friendly_recruits[0]),
    # )
    # print(Debug.ShopSnapshotSerializer.print(friendly_shop_snapshot))
    # print(friendly_shop_snapshot.to_json())
    # print(len(json.dumps(friendly_shop_snapshot.to_json()).encode("utf-8")))

    # Shop Set Objet Data
    # GameEngine.reconcile_shop_user_input(
    #     shop_snapshot=friendly_shop_snapshot,
    #     user_input=ShopUserInput(op=GameConstants.Opcodes.Shop.shop_set_object_data,
    #                              team_object=friendly_shop_snapshot.current_state.friendly_recruits[0],
    #                              target_object=friendly_shop_snapshot.current_state.friendly_recruits[0],
    #                              set_shop_object_data_opcode=GameConstants.Opcodes.ObjectData.shop_set_custom)
    # )
    # print(Debug.ShopSnapshotSerializer.print(friendly_shop_snapshot))
    # print(friendly_shop_snapshot.to_json())
    # print(len(json.dumps(friendly_shop_snapshot.to_json()).encode("utf-8")))


if __name__ == "__main__":
    asdf()
