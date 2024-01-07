from typing import List

from zb7_game_engine.runtime.objects.base.BaseListener import BaseListener


class Listeners:
    class Hooks:
        shop_bought = "shop_bought"
        shop_sold = "shop_sold"
        shop_rolled = "shop_rolled"
        shop_level_up = "shop_level_up"
        battle_level_up = "battle_level_up"
        shop_set_object_data = "shop_set_object_data"
        shop_gain_experience = "shop_gain_experience"
        battle_gain_experience = "battle_gain_experience"
        battle_receive_status_damage = "battle_receive_status_damage"
        battle_before_everything = "battle_before_everything"
        shop_start_of_turn = "shop_start_of_turn"
        shop_end_of_turn = "shop_end_of_turn"
        battle_heal = "battle_heal"
        shop_receive_damage = "shop_receive_damage"
        battle_receive_damage = "battle_receive_damage"
        shop_receive_unblockable_damage = "shop_receive_unblockable_damage"
        battle_receive_unblockable_damage = "battle_receive_unblockable_damage"
        battle_debuff_stats = "battle_debuff_stats"
        shop_debuff_stats = "shop_debuff_stats"
        battle_buff_stats = "battle_buff_stats"
        shop_buff_stats = "shop_buff_stats"
        shop_attack_with_range = "shop_attack_with_range"
        battle_attack_with_range = "battle_attack_with_range"
        shop_revive = "shop_revive"
        battle_revive = "battle_revive"
        shop_attack_with_melee = "shop_attack_with_melee"
        battle_attack_with_melee = "battle_attack_with_melee"
        shop_faint = "shop_faint"
        battle_faint = "battle_faint"
        passive_battle_ability = "passive_battle_ability"
        start_of_battle = "start_of_battle"
        battle_friendly_recruit_faints = "battle_friendly_recruit_faints"
        battle_friendly_recruit_summoned = "battle_friendly_recruit_summoned"
        shop_friendly_recruit_faints = "shop_friendly_recruit_faints"
        shop_friendly_recruit_summoned = "shop_friendly_recruit_summoned"
        add_status = "add_status"

    def __init__(self):
        self._default_list = []
        self.listeners: dict[str, List[BaseListener]] = {
            Listeners.Hooks.shop_bought: self._default_list,
            Listeners.Hooks.shop_sold: self._default_list,
            Listeners.Hooks.shop_rolled: self._default_list,
            Listeners.Hooks.shop_level_up: self._default_list,
            Listeners.Hooks.battle_level_up: self._default_list,
            Listeners.Hooks.shop_set_object_data: self._default_list,
            Listeners.Hooks.shop_gain_experience: self._default_list,
            Listeners.Hooks.battle_gain_experience: self._default_list,
            Listeners.Hooks.battle_receive_status_damage: self._default_list,
            Listeners.Hooks.battle_before_everything: self._default_list,
            Listeners.Hooks.shop_start_of_turn: self._default_list,
            Listeners.Hooks.shop_end_of_turn: self._default_list,
            Listeners.Hooks.battle_heal: self._default_list,
            Listeners.Hooks.shop_receive_damage: self._default_list,
            Listeners.Hooks.battle_receive_damage: self._default_list,
            Listeners.Hooks.shop_receive_unblockable_damage: self._default_list,
            Listeners.Hooks.battle_receive_unblockable_damage: self._default_list,
            Listeners.Hooks.battle_debuff_stats: self._default_list,
            Listeners.Hooks.shop_debuff_stats: self._default_list,
            Listeners.Hooks.battle_buff_stats: self._default_list,
            Listeners.Hooks.shop_buff_stats: self._default_list,
            Listeners.Hooks.shop_attack_with_range: self._default_list,
            Listeners.Hooks.battle_attack_with_range: self._default_list,
            Listeners.Hooks.shop_revive: self._default_list,
            Listeners.Hooks.battle_revive: self._default_list,
            Listeners.Hooks.shop_attack_with_melee: self._default_list,
            Listeners.Hooks.battle_attack_with_melee: self._default_list,
            Listeners.Hooks.shop_faint: self._default_list,
            Listeners.Hooks.battle_faint: self._default_list,
            Listeners.Hooks.passive_battle_ability: self._default_list,
            Listeners.Hooks.start_of_battle: self._default_list,
            Listeners.Hooks.battle_friendly_recruit_faints: self._default_list,
            Listeners.Hooks.battle_friendly_recruit_summoned: self._default_list,
            Listeners.Hooks.shop_friendly_recruit_faints: self._default_list,
            Listeners.Hooks.shop_friendly_recruit_summoned: self._default_list,
            Listeners.Hooks.add_status: self._default_list
        }

    def add_listener(self, hook: str, listener: BaseListener):
        if hook not in self.listeners:
            raise Exception(f"Hook {hook} does not exist")
        if self.listeners[hook] == self._default_list:
            self.listeners[hook] = []
        self.listeners[hook].append(listener)
        self.listeners[hook].sort(key=lambda x: x.stack_order_number, reverse=True)

    def remove_listener(self, hook: str, listener):
        if hook not in self.listeners:
            raise Exception(f"Hook {hook} does not exist")
        if self.listeners[hook] == self._default_list:
            return
        self.listeners[hook] = [x for x in self.listeners[hook] if x != listener]

    def get_listeners(self, hook: str) -> List[BaseListener]:
        if hook not in self.listeners:
            raise Exception(f"Hook {hook} does not exist")
        return self.listeners[hook]
