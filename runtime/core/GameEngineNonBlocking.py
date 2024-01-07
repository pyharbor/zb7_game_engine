import asyncio
from typing import List, Tuple, Union

from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.ObjectParser import ObjectParser
from zb7_game_engine.runtime.core.StackItem import StackItem
from zb7_game_engine.runtime.core.StateSet import StateSet
from zb7_game_engine.runtime.core.shop_opcodes import Buy, Roll, Sell, Move, EndOfTurn, StartOfTurn, SetObjectData
from zb7_game_engine.runtime.core.shop_opcodes.ShopUserInput import ShopUserInput
from zb7_game_engine.runtime.core.shop_opcodes.player_decision import PlayerDecision
from zb7_game_engine.serialization.BattleSnapshotSerializer import BattleSnapshotSerializer
from zb7_game_engine.serialization.BattleStateSerializer import BattleStateSerializer
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer
from zb7_game_engine.serialization.ShopSnapshotSerializer import ShopSnapshotSerializer
from zb7_game_engine.serialization.animation_events.Animations import Animations


class GameEngineNonBlocking:

    @staticmethod
    async def reconcile_shop_user_input(shop_snapshot: ShopSnapshotSerializer, user_input: ShopUserInput):
        # these are copies so its ok to mutate them in ways that deviate from the run sequence
        animation_event_sequence: AnimationEventSequence = AnimationEventSequence()
        shop_state = shop_snapshot.current_state
        state_set = StateSet()

        shop_state.stack.appendleft(StackItem(op=user_input.op, object=None, context=user_input))

        match user_input.op:
            case GameConstants.Opcodes.Shop.shop_buy:
                shop_snapshot.snapshot_sub_type_as_text = GameConstants.SnapshotSubTypes.String.buy
                shop_snapshot.snapshot_sub_type_as_int = GameConstants.SnapshotSubTypes.Int.buy

            case GameConstants.Opcodes.Shop.shop_roll:
                shop_snapshot.snapshot_sub_type_as_text = GameConstants.SnapshotSubTypes.String.roll
                shop_snapshot.snapshot_sub_type_as_int = GameConstants.SnapshotSubTypes.Int.roll

            case GameConstants.Opcodes.Shop.shop_sell:
                shop_snapshot.snapshot_sub_type_as_text = GameConstants.SnapshotSubTypes.String.sell
                shop_snapshot.snapshot_sub_type_as_int = GameConstants.SnapshotSubTypes.Int.sell

            case GameConstants.Opcodes.Shop.shop_move:
                shop_snapshot.snapshot_sub_type_as_text = GameConstants.SnapshotSubTypes.String.move
                shop_snapshot.snapshot_sub_type_as_int = GameConstants.SnapshotSubTypes.Int.move

            case GameConstants.Opcodes.Shop.shop_end_of_turn:
                shop_snapshot.snapshot_sub_type_as_text = GameConstants.SnapshotSubTypes.String.end_of_turn
                shop_snapshot.snapshot_sub_type_as_int = GameConstants.SnapshotSubTypes.Int.end_of_turn

            case GameConstants.Opcodes.Shop.shop_start_of_turn:
                shop_snapshot.snapshot_sub_type_as_text = GameConstants.SnapshotSubTypes.String.start_of_turn
                shop_snapshot.snapshot_sub_type_as_int = GameConstants.SnapshotSubTypes.Int.start_of_turn

            case GameConstants.Opcodes.Shop.shop_set_object_data:
                match user_input.set_shop_object_data_opcode:
                    case "set_name":
                        shop_snapshot.snapshot_sub_type_as_text = GameConstants.SnapshotSubTypes.String.custom
                        shop_snapshot.snapshot_sub_type_as_int = GameConstants.SnapshotSubTypes.Int.custom
                    case "set_custom":
                        shop_snapshot.snapshot_sub_type_as_text = GameConstants.SnapshotSubTypes.String.custom
                        shop_snapshot.snapshot_sub_type_as_int = GameConstants.SnapshotSubTypes.Int.custom
                    case "set_aaid":
                        shop_snapshot.snapshot_sub_type_as_text = GameConstants.SnapshotSubTypes.String.custom
                        shop_snapshot.snapshot_sub_type_as_int = GameConstants.SnapshotSubTypes.Int.custom

        while len(shop_state.stack) > 0:
            await asyncio.sleep(0)
            stack_item = shop_state.stack.popleft()
            if stack_item.object is not None:
                stack_item.object.update_shop_state(shop_state=shop_state, stack_item=stack_item,
                                                    state_set=state_set,
                                                    animation_event_sequence=animation_event_sequence,
                                                    shop_snapshot=shop_snapshot)
            elif stack_item.op == GameConstants.Opcodes.Shop.shop_buy:
                Buy.update_shop_state(shop_state=shop_state, stack_item=stack_item,
                                      animation_event_sequence=animation_event_sequence,
                                      state_set=state_set)
            elif stack_item.op == GameConstants.Opcodes.Shop.shop_roll:
                Roll.update_shop_state(shop_state=shop_state, stack_item=stack_item,
                                       animation_event_sequence=animation_event_sequence,
                                       shop_snapshot=shop_snapshot,
                                       state_set=state_set)
            elif stack_item.op == GameConstants.Opcodes.Shop.shop_sell:
                Sell.update_shop_state(shop_state=shop_state, stack_item=stack_item,
                                       animation_event_sequence=animation_event_sequence,
                                       state_set=state_set)
            elif stack_item.op == GameConstants.Opcodes.Shop.shop_move:
                Move.update_shop_state(shop_state=shop_state, stack_item=stack_item,
                                       state_set=state_set,
                                       animation_event_sequence=animation_event_sequence)
            elif stack_item.op == GameConstants.Opcodes.Shop.shop_end_of_turn:
                EndOfTurn.update_shop_state(shop_state=shop_state, stack_item=stack_item,
                                            state_set=state_set,
                                            animation_event_sequence=animation_event_sequence)
            elif stack_item.op == GameConstants.Opcodes.Shop.shop_start_of_turn:
                StartOfTurn.update_shop_state(shop_state=shop_state, stack_item=stack_item,
                                              animation_event_sequence=animation_event_sequence,
                                              shop_snapshot=shop_snapshot,
                                              state_set=state_set)
            elif stack_item.op == GameConstants.Opcodes.Shop.shop_set_object_data:
                SetObjectData.update_shop_state(shop_state=shop_state, stack_item=stack_item,
                                                animation_event_sequence=animation_event_sequence,
                                                state_set=state_set,
                                                original_shop_snapshot=shop_snapshot)
            elif stack_item.op == GameConstants.Opcodes.Shop.shop_player_decision:
                PlayerDecision.update_shop_state(shop_state=shop_state, stack_item=stack_item,
                                                 animation_event_sequence=animation_event_sequence,
                                                 state_set=state_set,
                                                 original_run_snapshot=shop_snapshot)
        shop_snapshot.state_set = state_set
        state_id = shop_snapshot.state_set.add_state(shop_state)
        shop_snapshot.state_id = state_id
        shop_snapshot.animation_event_sequence = animation_event_sequence

    @staticmethod
    async def reconcile_battle(friendly_shop_snapshot: ShopSnapshotSerializer,
                               enemy_shop_snapshot: ShopSnapshotSerializer,
                               simulation: bool = False
                               ) -> BattleSnapshotSerializer:
        # we copy them here to prevent permanent changes, however we keep the original
        # to simultaneously allow permanent changes
        animation_event_sequence: AnimationEventSequence = AnimationEventSequence()
        state_set = StateSet()
        friendly_recruits_copy = [ObjectParser.from_base64_text(x.to_base64()) for x in
                                  friendly_shop_snapshot.current_state.friendly_recruits]
        friendly_relics_copy = [ObjectParser.from_base64_text(x.to_base64()) for x in
                                friendly_shop_snapshot.current_state.friendly_relics]
        enemy_recruits_copy = [ObjectParser.from_base64_text(x.to_base64()) for x in
                               enemy_shop_snapshot.current_state.friendly_recruits]
        enemy_relics_copy = [ObjectParser.from_base64_text(x.to_base64()) for x in
                             enemy_shop_snapshot.current_state.friendly_relics]

        battle_state = BattleStateSerializer(
            friendly_uuid=friendly_shop_snapshot.uuid,
            friendly_recruits=friendly_recruits_copy,
            friendly_relics=friendly_relics_copy,
            enemy_uuid=enemy_shop_snapshot.uuid,
            enemy_recruits=enemy_recruits_copy,
            enemy_relics=enemy_relics_copy,
            shop_turn=friendly_shop_snapshot.current_state.turn,
            original_shop_state=friendly_shop_snapshot.current_state,
            simulate=simulation
        )
        if simulation:
            battle_state.original_shop_state = None
        e = Animations.BattleStart(state_id=state_set.add_state(battle_state))
        animation_event_sequence.append(e)

        # things will always be queued in order of initiative
        battle_state.queue_ability_for_all_objects(trigger="battle_before_everything")
        battle_state.queue_ability_for_all_objects(trigger="start_of_battle")
        while battle_state.is_unresolved():
            await asyncio.sleep(0)
            # recruits individually handle whether they can
            # melee_attack, ranged_attack, or have an ability during the battle loop
            if len(battle_state.stack) == 0:
                # protect against true infinite loops
                if battle_state.battle_turn > 35:
                    break
                if battle_state.battle_turn > 20:
                    # start the end game sequence, by just bosting the shit out everyones attack
                    for x in battle_state.friendly_recruits:
                        if x.melee_attack == 0:
                            x.melee_attack = 1
                        if x.ranged_attack == 0:
                            x.ranged_attack = 1
                        x.melee_attack = min(x.melee_attack * 2, 10_000)
                        x.ranged_attack = min(x.ranged_attack * 2, 10_000)
                    for x in battle_state.enemy_recruits:
                        if x.melee_attack == 0:
                            x.melee_attack = 1
                        if x.ranged_attack == 0:
                            x.ranged_attack = 1
                        x.melee_attack = min(x.melee_attack * 2, 10_000)
                        x.ranged_attack = min(x.ranged_attack * 2, 10_000)
                    e = Animations.SuddenDeath(state_id=state_set.add_state(battle_state))
                    animation_event_sequence.append(e)
                battle_state.battle_turn += 1
                # this represents another round of battle
                battle_state.queue_default_for_all_objects(battle_state=battle_state,
                                                           state_set=state_set,
                                                           animation_event_sequence=animation_event_sequence)
                battle_state.queue_ability_for_all_objects(trigger=GameConstants.Opcodes.Stack.status_effect)
            stack = battle_state.stack
            stack_item = battle_state.stack.popleft()
            if simulation:
                stack_item.object.update_battle_state(battle_state=battle_state,
                                                      state_set=state_set,
                                                      stack_item=stack_item,
                                                      animation_event_sequence=animation_event_sequence,
                                                      original_shop_state=None)
            else:
                stack_item.object.update_battle_state(battle_state=battle_state,
                                                      state_set=state_set,
                                                      stack_item=stack_item,
                                                      animation_event_sequence=animation_event_sequence,
                                                      original_shop_state=friendly_shop_snapshot.current_state)
        # calculate the winner
        battle_state.queue_ability_for_all_objects(trigger="battle_after_everything")
        battle_result = battle_state.calculate_winner()

        e = None
        if battle_result == GameConstants.Battle.won:
            e = Animations.BattleWon(state_id=state_set.add_state(battle_state))
        elif battle_result == GameConstants.Battle.lost:
            e = Animations.BattleLost(state_id=state_set.add_state(battle_state))
        elif battle_result == GameConstants.Battle.draw:
            e = Animations.BattleDraw(state_id=state_set.add_state(battle_state))

        animation_event_sequence.append(e)
        battle_snapshot = BattleSnapshotSerializer(
            friendly_uuid=friendly_shop_snapshot.uuid,
            friendly_deck=friendly_shop_snapshot.deck,
            friendly_username=friendly_shop_snapshot.username,
            friendly_wins=friendly_shop_snapshot.wins,
            friendly_health=friendly_shop_snapshot.health,
            friendly_money=friendly_shop_snapshot.money,
            friendly_turn=friendly_shop_snapshot.turn,
            friendly_utc_date_str=friendly_shop_snapshot.utc_date_str,
            friendly_run_status_as_int=friendly_shop_snapshot.run_status_as_int,
            friendly_run_status_as_text=friendly_shop_snapshot.run_status_as_text,
            enemy_uuid=enemy_shop_snapshot.uuid,
            enemy_deck=enemy_shop_snapshot.deck,
            enemy_username=enemy_shop_snapshot.username,
            enemy_wins=enemy_shop_snapshot.wins,
            enemy_health=enemy_shop_snapshot.health,
            enemy_money=enemy_shop_snapshot.money,
            enemy_turn=enemy_shop_snapshot.turn,
            enemy_utc_date_str=enemy_shop_snapshot.utc_date_str,
            enemy_run_status_as_int=enemy_shop_snapshot.run_status_as_int,
            enemy_run_status_as_text=enemy_shop_snapshot.run_status_as_text,
            vs_mode_as_int=friendly_shop_snapshot.vs_mode_as_int,
            vs_mode_as_text=friendly_shop_snapshot.vs_mode_as_text,
            state_set=state_set,
            animation_event_sequence=animation_event_sequence,
            original_shop_state=friendly_shop_snapshot.current_state,
            operation_count=friendly_shop_snapshot.operation_count,
            battle_result_as_int=battle_result,
            snapshot_sub_type_as_int=GameConstants.SnapshotSubTypes.Int.battle,
            snapshot_sub_type_as_text=GameConstants.SnapshotSubTypes.String.battle,
        )
        return battle_snapshot
