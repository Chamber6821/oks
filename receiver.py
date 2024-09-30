#!/bin/python3.12

import sys

from commons import as_bits, from_file, to_bytes, unpack, unstuffed

MAX_DATA_LENGTH = 22 + 1
FLAG = (22).to_bytes(8, byteorder='little')

with open(sys.argv[1], 'r') as f:
    while True:
        flag = to_bytes(from_file(f), 8)
        packet = unpack(to_bytes(unstuffed(from_file(f), as_bits(FLAG)), 9 + MAX_DATA_LENGTH), MAX_DATA_LENGTH)
        print(packet.data.decode(), end='')

