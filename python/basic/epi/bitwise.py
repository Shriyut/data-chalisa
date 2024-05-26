a = 11
b = 43


def decimal_to_binary(n):
    return bin(n).replace("0b", "")


print("AND a & b =", a & b)
print("OR a | b = ", a | b)
print("XOR a ^ b = ", a ^ b)
print("NOT (~)a = ", ~a)
print("NOT (~)b = ", ~b)
print("BItwise right shift a >> 1 = ", a >> 1)
print("SHifts the left operand by the amount specified by right operand towards its right(can be used for division "
      "not ideal)")
print("Bitwise left shift a << 1 = ", a << 2)
print("SHifts the left operand to its left by the amount specified in right operand (can be used for multiplication"
      " << 1 = multiply by 2")
print(decimal_to_binary(a))
print(decimal_to_binary(b))

