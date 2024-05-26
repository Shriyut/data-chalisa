from python.basic.epi.primitive_types import pt_util


def get_parity(num):
    """Parity of a binary word is 1 if the number of 1s in the word is odd"""
    binary_word = pt_util.get_binary(num)
    print(binary_word)
    parity = 0
    while num:
        parity ^= num & 1
        num >>= 1

    print(parity)


get_parity(10)
