#!/bin/python3.12

import sys

from commons import Sniffer, as_bits, as_bytes, beautiful_bits, beautiful_print, from_file, to_bytes, unpack, unstuffed, wait_flag
from config import ADDRESS_LEN, FCS_SIZE, FLAG, JAM_LENGTH, MAX_DATA_LENGTH

with open(sys.argv[1], 'r') as f:
    while True:
        channal = from_file(f)
        wait_flag(channal, as_bits(FLAG))
        sniffed = Sniffer(channal)
        equippedChannal = unstuffed( sniffed.sequence(), as_bits(FLAG))
        packet = unpack(
            to_bytes(
                equippedChannal,
                2*ADDRESS_LEN + MAX_DATA_LENGTH + FCS_SIZE
            ),
            MAX_DATA_LENGTH
        )
        jam = to_bytes(equippedChannal, JAM_LENGTH)
        hasCollision = int.from_bytes(jam).bit_count() > (JAM_LENGTH / 2) * 8
        print(packet.data)
        beautiful_print('FCS Or', beautiful_bits(as_bits(packet.original_fcs)))
        beautiful_print('FCS Ca', beautiful_bits(as_bits(packet.calculated_fcs)))
        beautiful_print('RAW',  beautiful_bits(sniffed.buffer()))
        if hasCollision:
            print('\033[31;7mCollision!\033[0m')
            continue
        error_code = as_bytes([a != b for a, b in zip(as_bits(packet.original_fcs), as_bits(packet.calculated_fcs))])
        error_position = sum([2**i if b else 0 for i, b in enumerate(as_bits(error_code))]) - 1
        print('-' * (6 + 2*ADDRESS_LEN * 8),'-' * (error_position + 1),  '^', sep='')
        if error_position >= MAX_DATA_LENGTH * 8:
            print('Corrupted :(')
        elif error_position > -1:
            bits = as_bits(packet.data)
            bits[error_position] = not bits[error_position]
            print('Repaired:', as_bytes(bits))
        else:
            print('Ok')
        

