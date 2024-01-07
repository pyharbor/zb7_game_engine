class ShopIDTarget:

    @staticmethod
    def custom_data_to_bytes(self) -> bytes:
        _bytes = bytearray()
        len_target_bytes = int(0).to_bytes(1, byteorder="big")
        target_bytes = b""
        if self.target is not None:
            target_bytes = self.target.to_bytes(1, byteorder="big")
            len_target_bytes = len(target_bytes).to_bytes(1, byteorder="big")
        _bytes.extend(len_target_bytes)
        _bytes.extend(target_bytes)
        return _bytes

    @staticmethod
    def bytes_to_custom_data(_bytes: bytes, current_index: int) -> dict:
        len_target = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        if len_target > 0:
            target = int.from_bytes(_bytes[current_index:current_index + len_target], byteorder="big")
        else:
            target = None
        return {"target": target}