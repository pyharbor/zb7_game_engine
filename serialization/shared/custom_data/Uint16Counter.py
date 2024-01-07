class Uint16Counter:

    @staticmethod
    def custom_data_to_bytes(self, key: str) -> bytes:
        counter = self.custom_data[key]
        counter_bytes = counter.to_bytes(2, byteorder="big")
        return counter_bytes

    @staticmethod
    def bytes_to_custom_data(_bytes: bytes, current_index: int, key: str) -> dict:
        counter = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 2
        return {key: counter}