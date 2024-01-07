from zb7_game_engine.runtime.core.AnimationEventSequence import AnimationEventSequence
from zb7_game_engine.runtime.core.GameConstants import GameConstants
from zb7_game_engine.runtime.objects.base.BaseListener import BaseListener
from typing import TYPE_CHECKING, Union

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


class BasicArmor(BaseListener):
    def __init__(self,
                 listener_target: Union["RecruitSerializer", "RelicSerializer", "BaseRecruit", "BaseRelic"] = None):
        self.listener_target = listener_target
        self.stack_order_number = 0

    def lt_battle_receive_damage(self, damage: int,
                                 battle_state: "BattleStateSerializer",
                                 enemy: "BaseRecruit",
                                 state_set: "StateSet",
                                 recruit: "RecruitSerializer",
                                 animation_event_sequence: AnimationEventSequence,
                                 origin: str = "melee",
                                 original_shop_state: "ShopStateSerializer" = None,
                                 damage_reduction_stack: list[dict] = None
                                 ) -> list[int, bool]:
        if self.listener_target.armor > 0:
            if damage_reduction_stack is not None:
                damage_reduction_stack.append(
                    dict(amount=self.listener_target.armor,
                         sub_type_as_int=GameConstants.DamageReductionStack.BasicArmor))
            overkill = damage - self.listener_target.armor
            return [overkill, False]
        else:
            return [damage, False]

    def lt_shop_receive_damage(self, damage: int,
                               shop_state: "ShopStateSerializer",
                               enemy: "BaseRecruit",
                               state_set: "StateSet",
                               recruit: "RecruitSerializer",
                               animation_event_sequence: AnimationEventSequence,
                               origin: str = "melee",
                               original_shop_state: "ShopStateSerializer" = None,
                               damage_reduction_stack: list[dict] = None
                               ) -> list[int, bool]:
        if self.listener_target.armor > 0:
            if damage_reduction_stack is not None:
                damage_reduction_stack.append(
                    dict(amount=self.listener_target.armor,
                         sub_type_as_int=GameConstants.DamageReductionStack.BasicArmor))
            overkill = damage - self.listener_target.armor
            return [overkill, False]
        else:
            return [damage, False]
