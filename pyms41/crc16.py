_POLYNOMIAL = 0xa001
_TABLE = []


for i in range(256):
    num = 0
    num2 = i
    for j in range(8):
        if (num2 ^ num) & 1 != 0:
            num = (num >> 1) ^ _POLYNOMIAL
        else:
            num = num >> 1
        num2 = num2 >> 1
    _TABLE.append(num)


def crc(buf: bytes, initial_value: int) -> int:
    sum = initial_value
    for byte in buf:
        index = (sum ^ byte) & 0xff
        sum = (sum >> 8) ^ _TABLE[index]
    return sum
