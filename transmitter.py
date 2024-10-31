#!/bin/python3.12

import sys
from commons import Sniffer, as_bits, beautiful_bits, beautiful_print, broken_pipe, from_bytes, pack, stuffed, to_file
from config import FLAG, MAX_DATA_LENGTH, MESSAGE_SIZE


with open(sys.argv[1], 'w') as f:
    while True:
        message = input('Message: ') + '\n'
        message_bytes = message.encode()
        beautiful_print('LENGTH', len(message_bytes))
        for i in range(0, len(message), MAX_DATA_LENGTH):
            message_part = (message_bytes[i:i+MAX_DATA_LENGTH] + bytes([0] * MAX_DATA_LENGTH))[:MAX_DATA_LENGTH]
            sniffer = Sniffer(stuffed(from_bytes(pack(
                source_address=0,
                destination_address=0,
                data=message_part
            )), as_bits(FLAG)))
            to_file(f, from_bytes(FLAG))
            to_file(f, broken_pipe(sniffer.sequence(), 0.6 / (MESSAGE_SIZE * 8)))
            f.flush()
            print(message_part)
            beautiful_print('RAW', beautiful_bits(sniffer.buffer()))
