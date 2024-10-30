import math

MAX_DATA_LENGTH = 5 # 22 + 1
FLAG = (22).to_bytes(1, byteorder='little')
ADDRESS_LEN = 1
FCS_SIZE = math.ceil(math.log2(MAX_DATA_LENGTH + 1) / 8)
