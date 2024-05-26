def count_bits(num):
    """Counts the number of bits that are set to 1 in a non-negative integer"""
    num_bits = 0
    while num:
        print("Starting num_bits ", num_bits)
        print("BIt value of input being processed ", num)
        num_bits += num & 1
        print("NUm bits after AND operation ", num_bits)
        num >>= 1
        print("Bit after right shift on input ", num)
    return num_bits


def convert_to_binary(n):
    return bin(n).replace("0b", "")


if __name__ == "__main__":
    a = 29898
    print("Input in binary format is ", convert_to_binary(a))
    print(count_bits(a))
