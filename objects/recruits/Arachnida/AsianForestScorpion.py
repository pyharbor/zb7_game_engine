from typing import List

from collections import deque        
from zb7_game_engine.runtime.objects.statuses.Statuses import Statuses
from zb7_game_engine.serialization.animation_events.G.Group import Group
from zb7_game_engine.immutable_data.ImmutableData import ImmutableData
from zb7_game_engine.runtime.misc.BinomialNomenclature import BinomialNomenclature
from zb7_game_engine.runtime.objects.base.BaseRecruit import BaseRecruit
from zb7_game_engine.runtime.objects.base.BaseStatus import BaseStatus
from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.StateSet import StateSet
from typing import List, TYPE_CHECKING, Union
from zb7_game_engine.runtime.core.StackItem import StackItem
from zb7_game_engine.serialization.animation_events.Animations import Animations
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.core.Listeners import Listeners
from zb7_game_engine.runtime.core.RandomEngine import random_engine
from zb7_game_engine.serialization.EmptySlotSerializer import EmptySlotSerializer
from zb7_game_engine.serialization.shared.custom_data.ShopIDTarget import ShopIDTarget
from zb7_game_engine.serialization.shared.custom_data.Uint8ArrayOfScientificNomenclature import Uint8ArrayOfScientificNomenclature
from zb7_game_engine.serialization.shared.custom_data.Uint8Counter import Uint8Counter
from zb7_game_engine.serialization.shared.custom_data.Uint16Counter import Uint16Counter
from zb7_game_engine.runtime.objects.relics.Relics import Relics
from zb7_game_engine.serialization.shared.custom_data.CarpenterAntCD import CarpenterAntCD
from zb7_game_engine.serialization.shared.custom_data.SeaOtterCD import SeaOtterCD


if TYPE_CHECKING:
    from zb7_game_engine.serialization.ShopStateSerializer import ShopStateSerializer
    from zb7_game_engine.serialization.BattleStateSerializer import BattleStateSerializer
    from zb7_game_engine.runtime.core.StackItem import StackItem
    from zb7_game_engine.runtime.core.StateSet import StateSet
    from zb7_game_engine.runtime.core.shop_opcodes.ShopUserInput import ShopUserInput
    from zb7_game_engine.serialization.BattleSnapshotSerializer import BattleSnapshotSerializer
    from zb7_game_engine.serialization.ShopSnapshotSerializer import ShopSnapshotSerializer
    from zb7_game_engine.serialization.RelicSerializer import RelicSerializer
    from zb7_game_engine.serialization.RecruitSerializer import RecruitSerializer
    from zb7_game_engine.serialization.StatusSerializer import StatusSerializer


class AsianForestScorpion(RecruitSerializer):
    def __init__(self, **kwargs):
        kwargs.pop("sub_type_as_int", None)
        kwargs.pop("sub_type_as_text", None)
        super().__init__(sub_type_as_int=7,
                         sub_type_as_text="AsianForestScorpion", 
                         **kwargs)
                         
        # ------ Protect Below from Code Templating ------

        
    def battle_faint(self, battle_state: "BattleStateSerializer",
                     state_set: StateSet,
                     stack_item: "StackItem",
                     animation_event_sequence: AnimationEventSequence,
                     original_shop_state: "ShopStateSerializer" = None):
        if self.experience < GameConstants.Levels.level_4:
            random_enemy = self.get_completely_random_enemy(battle_state)
            if random_enemy is not None:
                e = Animations.ScorpionSting(
                    battle_id=self.battle_id,
                    shop_id=self.shop_id,
                    target_battle_id=random_enemy.battle_id,
                    target_shop_id=random_enemy.shop_id,
                    amount=self.melee_attack,
                    state_id=state_set.add_state(battle_state)
                )
                animation_event_sequence.append(e)

                random_enemy.battle_receive_damage(
                    battle_state=battle_state,
                    state_set=state_set,
                    enemy=self,
                    animation_event_sequence=animation_event_sequence,
                    damage=self.melee_attack,
                    origin="melee",
                    original_shop_state=original_shop_state)
        else:
            for i in range(2):
                random_enemy = self.get_completely_random_enemy(battle_state)
                if random_enemy is not None:
                    e = Animations.ScorpionSting(
                        battle_id=self.battle_id,
                        shop_id=self.shop_id,
                        target_battle_id=random_enemy.battle_id,
                        target_shop_id=random_enemy.shop_id,
                        amount=self.melee_attack,
                        state_id=state_set.add_state(battle_state)
                    )
                    animation_event_sequence.append(e)

                    random_enemy.battle_receive_damage(
                        battle_state=battle_state,
                        state_set=state_set,
                        enemy=self,
                        animation_event_sequence=animation_event_sequence,
                        damage=self.melee_attack,
                        origin="melee",
                        original_shop_state=original_shop_state)
        e = Animations.Faint(
            state_id=state_set.add_state(state=battle_state),
            shop_id=self.shop_id,
            battle_id=self.battle_id,
        )
        animation_event_sequence.append(e)
        # this is handled here to make sure that hive durabi.ity works correctly with ASianForestScorpion
        for x in self.listeners.get_listeners(hook=Listeners.Hooks.battle_faint):
            # basically we allow arbitrary other objects to affect the 'fainting' of a unit
            # if that unit is revived it doesn't actually need to faint and thus returns immediately
            should_return = x.lt_battle_faint(
                battle_state=battle_state,
                state_set=state_set,
                stack_item=stack_item,
                animation_event_sequence=animation_event_sequence,
                original_shop_state=original_shop_state
            )
            if should_return:
                return
        battle_info = battle_state.get_battle_info(battle_id=self.battle_id)
        objects = battle_info.friendly_recruits + battle_info.friendly_relics
        objects = [x for x in objects if x.battle_id != self.battle_id]
        battle_state.queue_ability_for(trigger=GameConstants.Opcodes.Stack.battle_friendly_recruit_faints,
                                       objects=objects,
                                       context={"target": self})

        battle_state.remove_recruit_from_battle(self)
        battle_state.stack = deque([x for x in battle_state.stack if x.object.battle_id != self.battle_id])

    def shop_start_of_turn(self, shop_state: "ShopStateSerializer", state_set: "StateSet", stack_item: "StackItem",
                           animation_event_sequence: AnimationEventSequence,
                           shop_snapshot: "ShopSnapshotSerializer" = None):
        self.generic_ability_notification(
            state=shop_state,
            state_set=state_set,
            description="seket blessing",
            animation_event_sequence=animation_event_sequence)
        choices = ["melee", "ranged", "health", "armor", "initiative"]
        random_stat = random_engine.choice(_list=choices, seed=shop_snapshot.uuid, snapshot=shop_snapshot)
        recruit_choices = []
        for x in shop_snapshot.friendly_recruits:
            for h in GameConstants.Habitats.TropicalForests:
                if h in x.binomial_nomenclature:
                    recruit_choices.append(x)
                break
        if len(recruit_choices) > 0:
            random_recruit: RecruitSerializer = random_engine.choice(_list=recruit_choices, seed=shop_snapshot.uuid, snapshot=shop_snapshot)
            if random_stat == "melee":
                random_recruit.shop_buff_stats(
                    shop_state=shop_state,
                    state_set=state_set,
                    stack_item=stack_item,
                    animation_event_sequence=animation_event_sequence,
                    melee=5,
                )
            elif random_stat == "ranged":
                random_recruit.shop_buff_stats(
                    shop_state=shop_state,
                    state_set=state_set,
                    stack_item=stack_item,
                    animation_event_sequence=animation_event_sequence,
                    ranged=5,
                )
            elif random_stat == "health":
                random_recruit.shop_buff_stats(
                    shop_state=shop_state,
                    state_set=state_set,
                    stack_item=stack_item,
                    animation_event_sequence=animation_event_sequence,
                    health=5,
                    max_health=5,
                )
            elif random_stat == "armor":
                random_recruit.shop_buff_stats(
                    shop_state=shop_state,
                    state_set=state_set,
                    stack_item=stack_item,
                    animation_event_sequence=animation_event_sequence,
                    armor=5,
                )
            elif random_stat == "initiative":
                random_recruit.shop_buff_stats(
                    shop_state=shop_state,
                    state_set=state_set,
                    stack_item=stack_item,
                    animation_event_sequence=animation_event_sequence,
                    initiative=5,
                )

