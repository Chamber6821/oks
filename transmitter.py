#!/bin/python3.12

import sys
from commons import as_bits, from_bytes, pack, stuffed, to_file

MAX_DATA_LENGTH = 22 + 1
FLAG = (22).to_bytes(8, byteorder='little')

with open(sys.argv[1], 'w') as f:
    while True:
        message = input() + '\n'
        to_file(f, from_bytes(FLAG))
        to_file(f, stuffed(from_bytes(pack(
            source_address=0,
            destination_address=0,
            data=(message.encode() + bytes([0] * MAX_DATA_LENGTH))[:MAX_DATA_LENGTH]
        )), as_bits(FLAG)))
        f.flush()

