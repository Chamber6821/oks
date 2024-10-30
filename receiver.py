#!/bin/python3.12

import sys

from commons import Sniffer, as_bits, beautiful_bits, beautiful_print, from_file, to_bytes, unpack, unstuffed
from config import ADDRESS_LEN, FCS_SIZE, FLAG, MAX_DATA_LENGTH

with open(sys.argv[1], 'r') as f:
    while True:
        sniffed = Sniffer(from_file(f))
        flag = to_bytes(sniffed.sequence(), len(FLAG))
        packet = unpack(
            to_bytes(
                unstuffed(
                    sniffed.sequence(),
                    as_bits(FLAG)
                ),
                2*ADDRESS_LEN + MAX_DATA_LENGTH + FCS_SIZE
            ),
            MAX_DATA_LENGTH
        )
        print(packet.data)
        beautiful_print('RAW',  beautiful_bits(sniffed.buffer()))
        beautiful_print('FCS Or', beautiful_bits(as_bits(packet.original_fcs)))
        beautiful_print('FCS Ca', beautiful_bits(as_bits(packet.calculated_fcs)))

