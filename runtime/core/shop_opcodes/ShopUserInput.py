from zb7_game_engine.runtime.core.ObjectParser import ObjectParser


class ShopUserInput:
    def __init__(self, op: str, shop_object=None, team_object=None, team_object_1=None, team_object_2=None,
                 target_object=None, player_decision_choice=None, set_shop_object_data_opcode=None):
        self.op = op
        self.shop_object = shop_object
        self.team_object = team_object
        self.team_object_1 = team_object_1
        self.team_object_2 = team_object_2
        self.target_object = target_object
        self.player_decision_choice = player_decision_choice
        self.set_shop_object_data_opcode = set_shop_object_data_opcode

    def to_json(self):
        return {
            "op": self.op,
            "shop_object": self.shop_object.to_json() if self.shop_object else None,
            "team_object": self.team_object.to_json() if self.team_object else None,
            "team_object_1": self.team_object_1.to_json() if self.team_object_1 else None,
            "team_object_2": self.team_object_2.to_json() if self.team_object_2 else None,
            "target_object": self.target_object.to_json() if self.target_object else None,
            "player_decision_choice": self.player_decision_choice if self.player_decision_choice else None,
            "set_shop_object_data_opcode": self.set_shop_object_data_opcode
        }
    @staticmethod
    def from_json(_json):
        shop_object = _json.get("shop_object", None)
        team_object = _json.get("team_object", None)
        team_object_1 = _json.get("team_object_1", None)
        team_object_2 = _json.get("team_object_2", None)
        target_object = _json.get("target_object", None)
        player_decision_choice = _json.get("player_decision_choice", None)
        set_shop_object_data_opcode = _json.get("set_shop_object_data_opcode", None)
        if shop_object:
            # inject the immutable data into the shop object here
            shop_object = ObjectParser.from_base64_text_minimal(shop_object)

        if team_object:
            # inject the immutable data into the team object here
            team_object = ObjectParser.from_base64_text(team_object)

        if team_object_1:
            # inject the immutable data into the team object here
            team_object_1 = ObjectParser.from_base64_text(team_object_1)

        if team_object_2:
            team_object_2 = ObjectParser.from_base64_text(team_object_2)

        if isinstance(target_object, dict):
            target_object = ObjectParser.from_base64_text(target_object)

        elif isinstance(target_object, str) or isinstance(target_object, int) or isinstance(target_object, float):
            target_object = target_object
        elif target_object is None:
            pass
        else:
            raise ValueError("target_object must be either a dict or a primitive type (str, int, float)")

        return ShopUserInput(
            op=_json["op"],
            shop_object=shop_object,
            team_object=team_object,
            team_object_1=team_object_1,
            team_object_2=team_object_2,
            target_object=target_object,
            player_decision_choice=player_decision_choice,
            set_shop_object_data_opcode=set_shop_object_data_opcode
        )