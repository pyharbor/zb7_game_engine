import itertools
import textwrap

from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.core.AnimationEvent import AnimationEvent
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.StateSet import StateSet
from zb7_game_engine.serialization.AnimationEventSerializer import AnimationEventSerializer
from zb7_game_engine.serialization.BattleSnapshotSerializer import BattleSnapshotSerializer
from zb7_game_engine.serialization.BattleStateSerializer import BattleStateSerializer
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.serialization.RelicSerializer import RelicSerializer
from zb7_game_engine.serialization.ShopSnapshotSerializer import ShopSnapshotSerializer
from zb7_game_engine.serialization.ShopStateSerializer import ShopStateSerializer
from zb7_game_engine.serialization.StatusSerializer import StatusSerializer
from zb7_game_engine.serialization.animation_events.Animations import Animations
from zb7_game_engine.serialization.animation_events.G.Group import Group


class Debug:
    class ShopStateSerializer:
        @staticmethod
        def print(x: ShopStateSerializer):
            info = f"wins: {x.wins}"
            info += f", health: {x.health}"
            info += f", money: {x.money}"
            info += f", turn: {x.turn}\n"
            info += f"friendly_relics: {len(x.friendly_relics)}\n"
            for e in x.friendly_relics:
                info += f"    {e}\n"
            info += f"friendly_recruits: {len(x.friendly_recruits)}\n"
            for e in x.friendly_recruits:
                info += f"    {e}\n"
            info += f"shop: {len(x.shop)}\n"
            for e in x.shop:
                if e.type == "Recruit":
                    info += f"    {e.sub_type_as_text.ljust(30)} {e.shop_id}\n"
                elif e.type == "Relic":
                    info += f"    {e.sub_type_as_text.ljust(30)} {e.shop_id}\n"
            return info

    class BattleStateSerializer:
        @staticmethod
        def print(x: BattleStateSerializer, friendly_username: str = None, enemy_username: str = None) -> str:
            info = "\tbattle_turn: " + str(x.battle_turn) + "\n"
            info += f"\t{friendly_username}".ljust(69) + f"{enemy_username}\n"
            for e in x.friendly_relics:
                info += f"      {e}\n"


            for e1, e2 in  itertools.zip_longest(x.friendly_recruits, x.enemy_recruits):
                info += f"\t{Debug.RecruitSerializer.battle_info(e1)}      {Debug.RecruitSerializer.battle_info(e2)}\n"
            return info

    class BattleSnapshotSerializer:
        @staticmethod
        def print(x: BattleSnapshotSerializer):
            info = f"BattleSnapshot\n"
            info += f"sub_type: {x.snapshot_sub_type_as_text}\n"
            # info = f"friendly_uuid: {x.friendly_uuid}\n"
            # info += f"friendly_username: {x.friendly_username}\n"
            # info += f"friendly_wins: {x.friendly_wins}\n"
            # info += f"friendly_health: {x.friendly_health}\n"
            # info += f"friendly_money: {x.friendly_money}\n"
            # info += f"friendly_turn: {x.friendly_turn}\n"
            # info += f"friendly_utc_date_str: {x.friendly_utc_date_str}\n"
            # info += f"friendly_run_status_as_int: {x.friendly_run_status_as_int}\n"
            # info += f"friendly_run_status_as_text: {x.friendly_run_status_as_text}\n"
            #
            # info += f"enemy_uuid: {x.enemy_uuid}\n"
            # info += f"enemy_username: {x.enemy_username}\n"
            # info += f"enemy_wins: {x.enemy_wins}\n"
            # info += f"enemy_health: {x.enemy_health}\n"
            # info += f"enemy_money: {x.enemy_money}\n"
            # info += f"enemy_turn: {x.enemy_turn}\n"
            # info += f"enemy_utc_date_str: {x.enemy_utc_date_str}\n"
            # info += f"enemy_run_status_as_int: {x.enemy_run_status_as_int}\n"
            # info += f"enemy_run_status_as_text: {x.enemy_run_status_as_text}\n"
            #
            # info += f"vs_mode_as_int: {x.vs_mode_as_int}\n"
            # info += f"vs_mode_as_text: {x.vs_mode_as_text}\n"
            #
            # info += f"operation_count: {x.operation_count}\n"
            # info += f"previous_luuid: {x.previous_luuid}\n"
            # info += f"luuid: {x.luuid}\n"
            # info += f"animation_event_sequence: {len(x.animation_event_sequence)}\n"
            # info += f"battle_result_as_int: {x.battle_result_as_int}\n"

            state_set = x.state_set
            for ae in x.animation_event_sequence:
                state = state_set.get_state_by_state_id(state_id=ae.state_id, _type="BattleSnapshot")
                info += f"animation_event: {ae.animation_type_as_text}\n"
                info += f"    {Debug.BattleAnimationEvent.print(event=ae, state=state)}\n"
                info += f"    state_id: {ae.state_id}\n"
                if isinstance(ae, Group):
                    for ae2 in ae.animation_events:
                        info += f"    {Debug.BattleAnimationEvent.print(event=ae2, state=state)}\n"
                info += Debug.BattleStateSerializer.print(state, friendly_username=x.friendly_username, enemy_username=x.enemy_username)
                info += "\n"

            return info

    class ShopAnimationEvent:
        @staticmethod
        def print(event: AnimationEventSerializer, state):
            if isinstance(event, Animations.MeleeAttack):
                attacker = state.get_object_from_shop_id(event.shop_id)
                defender = state.get_object_from_shop_id(event.target_shop_id)
                return f"{attacker.sub_type_as_text}({attacker.shop_id}) attacked (melee) {defender.sub_type_as_text}({defender.shop_id}) for {event.amount} damage"
            elif isinstance(event, Animations.RangedAttack):
                attacker = state.get_object_from_shop_id(event.shop_id)
                defender = state.get_object_from_shop_id(event.target_shop_id)
                return f"{attacker.sub_type_as_text}({attacker.shop_id}) attacked (range) {defender.sub_type_as_text}({defender.shop_id}) for {event.amount} damage"
            elif isinstance(event, Animations.FullBlock):
                x = state.get_object_from_shop_id(event.shop_id)
                info = f"{x.sub_type_as_text}({x.shop_id}) before={event.damage_before_modifications} after={event.damage_after_modifications}"
                for a in event.damage_reduction_stack:
                    sub_type = GameConstants.DamageReductionStack.from_int(a['sub_type_as_int'])
                    amount = a['amount']
                    info += f" {sub_type}({amount})"
                    return info
            elif isinstance(event, Animations.ReceiveDamage):
                x = state.get_object_from_shop_id(event.shop_id)
                return f"{x.sub_type_as_text}({x.shop_id}) before={event.damage_before_modifications} after={event.damage_after_modifications}"
            elif isinstance(event, Animations.Faint):
                x = state.get_object_from_shop_id(event.shop_id)
                return f"{x.sub_type_as_text}({x.shop_id}) fainted"
            elif isinstance(event, Animations.GenericAbilityNotification):
                x = state.get_object_from_shop_id(event.shop_id)
                return f"{x.sub_type_as_text}({x.shop_id}) {event.description}"
            elif isinstance(event, Animations.BuffStats):
                x = state.get_object_from_shop_id(event.shop_id)
                return f"{x.sub_type_as_text}({x.shop_id}) buffed +{event.melee}/+{event.ranged}/+{event.armor}/+{event.health}/+{event.max_health}/+{event.initiative}"
            elif isinstance(event, Animations.DebuffStats):
                x = state.get_object_from_shop_id(event.shop_id)
                return f"{x.sub_type_as_text}({x.shop_id}) debuffed -{event.melee}/-{event.ranged}/-{event.armor}/-{event.health}/-{event.max_health}/-{event.initiative}"
            elif isinstance(event, Animations.ReceiveStatusDamage):
                x = state.get_object_from_shop_id(event.shop_id)
                immutable_data = ImmutableData.Subtype.from_int(event.status_sub_type_as_int)
                return f"{x.sub_type_as_text}({x.shop_id}) {immutable_data['sub_type_as_text']} for {event.amount} damage"
            elif isinstance(event, Animations.AddStatus):
                x = state.get_object_from_shop_id(event.shop_id)
                immutable_data = ImmutableData.Subtype.from_int(event.status_sub_type_as_int)
                return f"{x.sub_type_as_text}({x.shop_id}) {immutable_data['sub_type_as_text']} added {event.amount} counters"
            elif isinstance(event, Animations.AddSpecies):
                x = state.get_object_from_shop_id(event.shop_id)
                immutable_data = ImmutableData.ScientificNomenclature.from_int(event.species_as_int)
                return f"{x.sub_type_as_text}({x.shop_id}) added  species {immutable_data}"
            elif isinstance(event, Animations.AddHabitat):
                x = state.get_object_from_shop_id(event.shop_id)
                immutable_data = ImmutableData.Habitats.from_int(event.habitat_as_int)
                return f"{x.sub_type_as_text}({x.shop_id}) added  habitat {immutable_data}"
            elif isinstance(event, Animations.Group):
                return event.animation_events[0].animation_type_as_text
            else:
                return f"AnimationEvent({event.animation_type_as_text})"

    class BattleAnimationEvent:
        @staticmethod
        def print(event: AnimationEventSerializer, state):
            if isinstance(event, Animations.MeleeAttack):
                attacker = state.get_object_from_battle_id(event.battle_id)
                defender = state.get_object_from_battle_id(event.target_battle_id)
                return f"{attacker.sub_type_as_text}({attacker.battle_id}) attacked (melee) {defender.sub_type_as_text}({defender.battle_id}) for {event.amount} damage"
            elif isinstance(event, Animations.RangedAttack):
                attacker = state.get_object_from_battle_id(event.battle_id)
                defender = state.get_object_from_battle_id(event.target_battle_id)
                return f"{attacker.sub_type_as_text}({attacker.battle_id}) attacked (range) {defender.sub_type_as_text}({defender.battle_id}) for {event.amount} damage"
            elif isinstance(event, Animations.FullBlock):
                x = state.get_object_from_battle_id(event.battle_id)
                info = f"{x.sub_type_as_text}({x.shop_id}) before={event.damage_before_modifications} after={event.damage_after_modifications}\n"
                for a in event.damage_reduction_stack:
                    sub_type = GameConstants.DamageReductionStack.from_int(a['sub_type_as_int'])
                    amount = a['amount']
                    info += f"\t{sub_type}({amount})\n"
                return info
            elif isinstance(event, Animations.ReceiveDamage):
                x = state.get_object_from_battle_id(event.battle_id)
                info = f"{x.sub_type_as_text}({x.battle_id}) before={event.damage_before_modifications} after={event.damage_after_modifications}\n"
                for a in event.damage_reduction_stack:
                    sub_type = GameConstants.DamageReductionStack.from_int(a['sub_type_as_int'])
                    amount = a['amount']
                    info += f"\t{sub_type}({amount})\n"
                return info
            elif isinstance(event, Animations.Faint):
                x = state.get_object_from_battle_id(event.battle_id)
                return f"{x.sub_type_as_text}({x.battle_id}) fainted"
            elif isinstance(event, Animations.GenericAbilityNotification):
                x = state.get_object_from_battle_id(event.battle_id)
                return f"{x.sub_type_as_text}({x.battle_id}) {event.description}"
            elif isinstance(event, Animations.BuffStats):
                x = state.get_object_from_battle_id(event.battle_id)
                return f"{x.sub_type_as_text}({x.battle_id}) buffed +{event.melee}/+{event.ranged}/+{event.armor}/+{event.health}/+{event.max_health}/+{event.initiative}"
            elif isinstance(event, Animations.ReceiveStatusDamage):
                x = state.get_object_from_battle_id(event.battle_id)
                immutable_data = ImmutableData.Subtype.from_int(event.status_sub_type_as_int)
                return f"{x.sub_type_as_text}({x.battle_id}) {immutable_data['sub_type_as_text']} for {event.amount} damage"
            elif isinstance(event, Animations.AddStatus):
                x = state.get_object_from_battle_id(event.battle_id)
                immutable_data = ImmutableData.Subtype.from_int(event.status_sub_type_as_int)
                return f"{x.sub_type_as_text}({x.battle_id}) {immutable_data['sub_type_as_text']} added {event.amount} counters"
            elif isinstance(event, Animations.Group):
                return event.animation_events[0].animation_type_as_text
            else:
                return f"AnimationEvent({event.animation_type_as_text})"

    class ShopSnapshotSerializer:
        @staticmethod
        def print(x: ShopSnapshotSerializer):
            info = ""
            info += f"ShopSnapshotSerializer({x.uuid})\n"
            info += f"sub_type: {x.snapshot_sub_type_as_text}\n"
            info += f"    animation_event_sequence: {len(x.animation_event_sequence)}\n"
            state_set = x.state_set
            for ae in x.animation_event_sequence:
                state = state_set.get_state_by_state_id(state_id=ae.state_id)
                info += f"animation_event: {ae.animation_type_as_text}\n"
                info += f"    {Debug.ShopAnimationEvent.print(event=ae, state=state)}\n"
                info += f"    state_id: {ae.state_id}\n"
                if isinstance(ae, Group):
                    for ae2 in ae.animation_events:
                        info += f"    {Debug.ShopAnimationEvent.print(event=ae2, state=state)}\n"
                info += Debug.ShopStateSerializer.print(state)
                info += "\n"
            return info

    class RecruitSerializer:
        @staticmethod
        def print(x: RecruitSerializer):
            print(f"{x.__class__.__name__}({x.name})")

        @staticmethod
        def battle_info(x: RecruitSerializer) -> str:
            if x is None:
                return "None".ljust(62)
            sub_type_justify = 30
            stats_justify = 25
            initiative_justify = 5
            total_length = sub_type_justify + stats_justify + initiative_justify
            sub_type = f"{x.sub_type_as_text}({x.battle_id})".ljust(sub_type_justify)
            stats = f"{x.melee_attack}/{x.ranged_attack}/{x.armor}/{x.health}/{x.max_health}".ljust(stats_justify)
            stats += f" {str(x.initiative).ljust(initiative_justify)}"
            info = f"{sub_type} {stats}"
            return info

        @staticmethod
        def study_info(x: RecruitSerializer) -> str:
            sub_type_justify = 30
            stats_justify = 25
            initiative_justify = 5
            total_length = sub_type_justify + stats_justify + initiative_justify
            sub_type = x.sub_type_as_text.ljust(sub_type_justify)
            stats = f"{x.melee_attack}/{x.ranged_attack}/{x.armor}/{x.health}/{x.max_health}".ljust(stats_justify)
            stats += f" {str(x.initiative).ljust(initiative_justify)}"
            cost = f"{x.cost}".ljust(5)
            rarity = f"{x.rarity}".ljust(10)
            main_species = f"{x.main_species}".ljust(20)
            habitats = f"{x.habitats}".ljust(30)
            info = f"{sub_type} {main_species} {rarity} {cost} {stats} {habitats}"
            return info

        @staticmethod
        def study_info_abilities(x: RecruitSerializer) -> str:
            sub_type_justify = 30
            stats_justify = 25
            initiative_justify = 5
            total_length = sub_type_justify + stats_justify + initiative_justify
            sub_type = x.sub_type_as_text.ljust(sub_type_justify)
            rarity = f"{x.rarity}".ljust(10)
            main_species = f"{x.main_species}".ljust(20)
            ability = f"{x.ability[0].description}"
            length = len("25  GreatHammerheadShark           ['CoralReef', 'Coastline', 'OpenOcean']                       ")
            justify = '\n'.ljust(length)
            ability = justify.join(textwrap.wrap(ability, width=50))
            habitats = f"{x.habitats}".ljust(60)
            info = f"{sub_type} {habitats} {ability}\n"
            return info


    class RelicSerializer:
        @staticmethod
        def print(x: RelicSerializer):
            print(f"{x.__class__.__name__}")

        @staticmethod
        def study_info_abilities(x: RelicSerializer) -> str:
            sub_type_justify = 30
            stats_justify = 25
            initiative_justify = 5
            total_length = sub_type_justify + stats_justify + initiative_justify
            sub_type = x.sub_type_as_text.ljust(sub_type_justify)
            rarity = f"{x.rarity}".ljust(10)
            cost = f"{x.cost}".ljust(5)
            ability = f"{x.ability[0]['description']}"
            length = len(
                "3   CrystalBall                    Uncommon   23     ")
            justify = '\n'.ljust(length)
            ability = justify.join(textwrap.wrap(ability, width=50))
            info = f"{sub_type} {rarity} {cost} {ability}\n"
            return info

    class StatusSerializer:

        @staticmethod
        def study_info_abilities(x: StatusSerializer) -> str:
            sub_type_justify = 30
            sub_type = x.sub_type_as_text.ljust(sub_type_justify)
            ability = f"{x.ability}"
            length = len(
                "3   HymenopteraDurability           ")
            justify = '\n'.ljust(length)
            ability = justify.join(textwrap.wrap(ability, width=50))
            info = f"{sub_type} {ability}\n"
            return info