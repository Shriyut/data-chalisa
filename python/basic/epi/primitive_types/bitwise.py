a = 11
b = 43


def decimal_to_binary(n):
    return bin(n).replace("0b", "")


print("AND returns 1 if both operand bits are 1 otherwise 0")
print("AND a & b =", a & b)
print(decimal_to_binary(a & b))
print("OR result bit 1 if any of the operand bit is 1 otherwise result bits 0")
print("OR a | b = ", a | b)
print(decimal_to_binary(a | b))
print("XOR result bit 1 if any operand is 1 otherwise 0")
print("XOR a ^ b = ", a ^ b)
print(decimal_to_binary(a ^ b))
print("NOT reverts individual bits")
print("NOT (~)a = ", ~a)
print(decimal_to_binary(~a))
print("NOT (~)b = ", ~b)
print(decimal_to_binary(~b))
print("SHifts the left operand by the amount specified by right operand towards its right(can be used for division "
      "not ideal)")
print("BItwise right shift a >> 1 = ", a >> 1)
print(decimal_to_binary(a >> 1))
print("SHifts the left operand to its left by the amount specified in right operand (can be used for multiplication"
      " << 1 = multiply by 2")
print("Bitwise left shift a << 1 = ", a << 1)
print(decimal_to_binary(a >> 1))
print(decimal_to_binary(a))
print(decimal_to_binary(b))

