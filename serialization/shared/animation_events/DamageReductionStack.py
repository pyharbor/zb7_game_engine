class DamageReductionStack:
    @staticmethod
    def to_bytes(self) -> bytearray:
        _bytes = bytearray()
        animation_type_bytes = self.animation_type_as_int.to_bytes(1, byteorder="big")
        state_id_bytes = self.state_id.to_bytes(2, byteorder="big")
        shop_id_bytes = self.shop_id.to_bytes(length=1, byteorder="big")
        if self.battle_id is None:
            battle_id_bytes = int(0).to_bytes(1, byteorder="big")
        else:
            battle_id_bytes = self.battle_id.to_bytes(1, byteorder="big")
        damage_reduction_stack_bytes = bytearray()
        for x in self.damage_reduction_stack:
            amount = max(x["amount"], 0)
            sub_type_as_int = x["sub_type_as_int"]
            amount_bytes = amount.to_bytes(length=2, byteorder="big")
            sub_type_as_int_bytes = sub_type_as_int.to_bytes(length=1, byteorder="big")
            damage_reduction_stack_bytes.extend(amount_bytes)
            damage_reduction_stack_bytes.extend(sub_type_as_int_bytes)

        damage_reduction_stack_bytes_length = len(damage_reduction_stack_bytes).to_bytes(length=2, byteorder="big")

        damage_after_modifications_bytes = self.damage_after_modifications.to_bytes(length=2, byteorder="big")
        damage_before_modifications_bytes = self.damage_before_modifications.to_bytes(length=2, byteorder="big")

        _bytes.extend(animation_type_bytes)
        _bytes.extend(state_id_bytes)
        _bytes.extend(shop_id_bytes)
        _bytes.extend(battle_id_bytes)
        _bytes.extend(damage_after_modifications_bytes)
        _bytes.extend(damage_before_modifications_bytes)
        _bytes.extend(damage_reduction_stack_bytes_length)
        _bytes.extend(damage_reduction_stack_bytes)
        return _bytes

    @staticmethod
    def from_bytes(cls, _bytes: bytes):
        current_index = 0
        animation_type_as_int = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        state_id = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 1

        shop_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1
        battle_id = int.from_bytes(_bytes[current_index:current_index + 1], byteorder="big")
        current_index += 1

        damage_after_modifications = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 2
        damage_before_modifications = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 2

        damage_reduction_stack_bytes_length = int.from_bytes(_bytes[current_index:current_index + 2], byteorder="big")
        current_index += 2
        damage_reduction_stack_bytes = _bytes[current_index:current_index + damage_reduction_stack_bytes_length]
        current_index += damage_reduction_stack_bytes_length

        damage_reduction_stack = []
        for x in range(0, len(damage_reduction_stack_bytes), 3):
            amount = int.from_bytes(damage_reduction_stack_bytes[x:x + 2], byteorder="big")
            sub_type_as_int = int.from_bytes(damage_reduction_stack_bytes[x + 2:x + 3], byteorder="big")
            damage_reduction_stack.append({
                "amount": amount,
                "sub_type_as_int": sub_type_as_int
            })

        return cls(state_id=state_id, damage_reduction_stack=damage_reduction_stack,
                   damage_after_modifications=damage_after_modifications,
                   damage_before_modifications=damage_before_modifications,
                   battle_id=battle_id, shop_id=shop_id)
