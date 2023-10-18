def sign_extend(value, bit_count):
        """
        Sign extend the given value from bit_count bits to 32 bits.
        """
        # Create a mask for the sign bit
        mask = 1 << (bit_count - 1)
        if value & mask:
            # If sign bit is set, fill with ones to the left
            return value | (~((1 << bit_count) - 1))
        # If sign bit is not set, no change is required
        return value

    # ... other parser functions ...

# Usage
literal = 0b1000000000000001  # A negative number in 16-bit two's complement format
extended_literal = sign_extend(literal, 16)
print(bin(extended_literal))



def sign_extend_to_16(value):
    """
    Sign extend the given value to 16 bits.
    """
    # Convert the value to binary and remove the '0b' prefix
    binary_repr = bin(value & 0xFFFF)[2:]

    # Ensure the literal does not exceed 16 bits
    assert len(binary_repr) <= 16, "Literal exceeds 16-bit limit"

    # Identify the bit width by finding the sign change position
    for i in range(len(binary_repr) - 1, 0, -1):
        if binary_repr[i] != binary_repr[i-1]:
            bit_width = i + 1
            break
    else:
        bit_width = 1  # This is the case when all bits are the same

    # Sign extend the value
    msb = binary_repr[0]
    while len(binary_repr) < 16:
        binary_repr = msb + binary_repr

    return int(binary_repr, 2)

# Testing
literal = -5  # example value
extended_value = sign_extend_to_16(literal)
print(bin(extended_value))