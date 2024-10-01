#!/bin/python3.12

import sys
from commons import as_bits, from_bytes, pack, stuffed, to_file
from config import FLAG, MAX_DATA_LENGTH


with open(sys.argv[1], 'w') as f:
    while True:
        message = input() + '\n'
        message_bytes = message.encode()
        print('Message length:', len(message_bytes))
        for i in range(0, len(message), MAX_DATA_LENGTH):
            print('Message offset:', i)
            message_part = (message_bytes[i:i+MAX_DATA_LENGTH] + bytes([0] * MAX_DATA_LENGTH))[:MAX_DATA_LENGTH]
            to_file(f, from_bytes(FLAG))
            to_file(f, stuffed(from_bytes(pack(
                source_address=0,
                destination_address=0,
                data=message_part
            )), as_bits(FLAG)))
            f.flush()
