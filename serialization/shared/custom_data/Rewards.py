from zb7_game_engine.runtime.core.ObjectParser import ObjectParser


class Rewards:

    @staticmethod
    def bytes_to_custom_data(_bytes: bytes, current_index: int) -> dict:
        rewards = []
        len_rewards = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        for x in range(0, len_rewards, 4):
            reward = ObjectParser.from_bytes_minimal(_bytes[current_index: current_index + 4])
            current_index += 4
            rewards.append(reward)
        return {"rewards": rewards}

    @staticmethod
    def custom_data_to_bytes(self) -> bytes:
        _bytes = bytearray()
        reward_bytes = b""
        for x in self.custom_data["rewards"]:
            reward_bytes += x.to_bytes_minimal()
        len_rewards_bytes = len(reward_bytes).to_bytes(1, byteorder="big")
        _bytes.extend(len_rewards_bytes)
        _bytes.extend(reward_bytes)
        return _bytes