import math

MAX_DATA_LENGTH = 5 # 22 + 1
FLAG = (22).to_bytes(1, byteorder='little')
ADDRESS_LEN = 1
FCS_SIZE = math.ceil(math.log2(8 * MAX_DATA_LENGTH + 1) / 8)
MESSAGE_SIZE = 2*ADDRESS_LEN + MAX_DATA_LENGTH + FCS_SIZE
JAM_LENGTH = 2
COLLISION_PROBABILITY = 0.1

FLAG_MESSAGE  = 0x00
FLAG_TOKEN    = 0x01
FLAG_RECEIVED = 0x80
