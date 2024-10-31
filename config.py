import math

MAX_DATA_LENGTH = 5 # 22 + 1
FLAG = (22).to_bytes(1, byteorder='little')
ADDRESS_LEN = 0
FCS_SIZE = math.ceil(math.log2(MAX_DATA_LENGTH + 1) / 8)
MESSAGE_SIZE = 2*ADDRESS_LEN + MAX_DATA_LENGTH + FCS_SIZE
