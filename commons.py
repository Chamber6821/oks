from typing import IO, Generator, List
from dataclasses import dataclass
import math
from functools import reduce
from random import random

from config import ADDRESS_LEN


Bitsequence = Generator[bool, None, None]


def as_bits(data: bytes) -> List[bool]:
    return [
        bit == '1'
        for bit in ''.join([
            f'{byte:08b}'
            for byte in data
        ])
    ]


def as_bytes(bits: List[bool]) -> bytes:
    return bytes([
        int(''.join([
            '01'[bit]
            for bit in (bits[i:i+8] + [False] * 8)[:8]]),
            base=2)
        for i in range(0, len(bits), 8)
    ])


def as_int(data: bytes):
    return int.from_bytes(data, byteorder='little')


def from_bytes(data: bytes) -> Bitsequence:
    for bit in as_bits(data):
        yield bit


def from_file(file: IO[str]) -> Bitsequence:
    while True:
        yield False if file.read(1) == '0' else True


def to_bytes(sequence: Bitsequence, length: int) -> bytes:
    bytes_acc = bytes()
    byte_acc = []
    for _ in range(length):
        for _, bit in zip(range(8), sequence):
            byte_acc.append(bit)
        bytes_acc += bytes([int(''.join(map(lambda x: '01'[x], byte_acc)), base=2)])
        byte_acc = []
    return bytes_acc


def to_file(file: IO[str], sequence: Bitsequence):
    for bit in sequence:
        file.write('1' if bit else '0')


def wait_flag(sequence: Bitsequence, flag: List[bool]):
    window = []
    for bit in sequence:
        window.append(bit)
        window = window[-len(flag):]
        if window == flag:
            return


def stuffed(sequence: Bitsequence, flag: List[bool]) -> Bitsequence:
    window = []
    for bit in sequence:
        window = window[-len(flag) + 1:]
        if window == flag[:-1]:
            window = [not flag[-1]]
            yield not flag[-1]
        window.append(bit)
        yield bit


def unstuffed(sequence: Bitsequence, flag: List[bool]) -> Bitsequence:
    window = []
    for bit in sequence:
        window = window[-len(flag) + 1:]
        if window == flag[:-1]:
            window = [not flag[-1]]
            continue
        window.append(bit)
        yield bit


def broken_pipe(sequence: Bitsequence, inversion_chance: float) -> Bitsequence:
    for bit in sequence:
        yield bit != (random() < inversion_chance)


def chain(*sequences: Bitsequence) -> Bitsequence:
    for seq in sequences:
        for bit in seq:
            yield bit


class Sniffer:
    def __init__(self, sequence: Bitsequence):
        self._sequence = sequence
        self._buffer = [] 

    def sequence(self) -> Bitsequence:
        for bit in self._sequence:
            self._buffer.append(bit)
            yield bit

    def reset(self):
        self._buffer = []

    def buffer(self):
        return self._buffer


def hamming_code(data: List[bool]) -> Generator[bool, None, None]:
    for power in range(0, math.ceil(math.log2(len(data) + 1))):
        step = 2**power
        yield reduce(
            lambda a, b: a != b,
            [
                data[i]
                for b in range(step - 1, len(data), step * 2)
                for i in range(b, min(b + step, len(data)))
            ]
        )


def pack(*, source_address: int, destination_address: int, data: bytes) -> bytes:
    return (source_address.to_bytes(ADDRESS_LEN, byteorder='little')
        + destination_address.to_bytes(ADDRESS_LEN, byteorder='little')
        + data
        + as_bytes(list(hamming_code(as_bits(data)))))


@dataclass
class Packet:
    source_address: int
    destination_address: int
    data: bytes
    original_fcs: bytes
    calculated_fcs: bytes


def unpack(packet: bytes, data_length: int) -> Packet:
    return Packet(
        source_address=as_int(packet[:ADDRESS_LEN - 1]),
        destination_address=as_int(packet[ADDRESS_LEN:2*ADDRESS_LEN - 1]),
        data=packet[2*ADDRESS_LEN:2*ADDRESS_LEN + data_length],
        original_fcs=packet[2*ADDRESS_LEN + data_length:],
        calculated_fcs=as_bytes(list(hamming_code(as_bits(packet[2*ADDRESS_LEN:2*ADDRESS_LEN + data_length]))))
    )


def beautiful_print(prefix, *args):
    print(f'\033[7m{(str(prefix) + " " * 999)[:6]}\033[0m', *args)


def beautiful_bits(bits: list[bool]) -> str:
    return ''.join(map(lambda x: '01'[x], bits))
    

