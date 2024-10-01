#!/bin/python3.12

import sys

from commons import Sniffer, as_bits, from_file, to_bytes, unpack, unstuffed
from config import FLAG, MAX_DATA_LENGTH


with open(sys.argv[1], 'r') as f:
    while True:
        sniffed = Sniffer(from_file(f))
        flag = to_bytes(sniffed.sequence(), len(FLAG))
        packet = unpack(to_bytes(unstuffed(sniffed.sequence(), as_bits(FLAG)), 9 + MAX_DATA_LENGTH), MAX_DATA_LENGTH)
        message_part = ''.join(filter(lambda x: ord(x) != 0, packet.data.decode()))
        print(''.join(map(lambda x: '01'[x], sniffed.buffer())))
        print(f'[{len(message_part)}]{message_part}')

