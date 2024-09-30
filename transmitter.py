#!/bin/python3.12
from io import TextIOWrapper
import sys, os
from typing import IO, Generator, List

MAX_DATA_LENGTH = 22 + 1
FLAG = 22

def as_bits(data: bytes) -> str:
    return ''.join(['{:08b}'.format(byte) for byte in data])

def as_bytes(bits: str) -> bytes:
    return bytes([int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)])

def as_int(data: bytes):
    return int.from_bytes(data, byteorder='little')

# stuffing = 5
# 11111 -> 111110
# 00000 -> 000001
# 111110000 -> 11111000001

Bitsequence = Generator[bool, None, None]

def from_bytes(data: bytes) -> Bitsequence:
    for bit in as_bits(data):
        yield False if bit == '0' else True

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

class Packet:
    def source(self) -> bytes: raise NotImplemented
    def destination(self) -> bytes: raise NotImplemented
    def data(self) -> bytes: raise NotImplemented
    def as_bits(self) -> str: raise NotImplemented

class MemoryPacket(Packet):
    def __init__(self, source: bytes, destination: bytes, data: bytes):
        if len(source) != 4: raise RuntimeError(f'Source address must have length 4, but got {len(source)}')
        if len(destination) != 4: raise RuntimeError(f'Destination address must have length 4, but got {len(destination)}')
        if len(data) > MAX_DATA_LENGTH: raise RuntimeError(f'Data address must have length not more than {MAX_DATA_LENGTH}, but got {len(data)}')
        self._source = source
        self._destination = destination
        self._data = (data + bytes([0] * MAX_DATA_LENGTH))[:MAX_DATA_LENGTH]
    def source(self) -> bytes: return self._source
    def destination(self) -> bytes: return self._destination
    def data(self) -> bytes: return self._data


def pack(*, source_address: int, destination_address: int, data: bytes) -> bytes:
    if len(data) > MAX_DATA_LENGTH:
        raise RuntimeError(f'Expected data length not more than {MAX_DATA_LENGTH}, but got {len(data)}')
    flag = FLAG.to_bytes(8, byteorder='little')
    fcs = 0
    return (flag 
        + source_address.to_bytes(4, byteorder='little')
        + destination_address.to_bytes(4, byteorder='little')
        + (data + bytes([0] * MAX_DATA_LENGTH))[:MAX_DATA_LENGTH] 
        + fcs.to_bytes())

def unpack(packet: bytes):
    return {
        'source_address': as_int(packet[8:12]),
        'destination_address': as_int(packet[12:16]),
        'data': packet[16:16 + MAX_DATA_LENGTH]
    }


data = bytes([0x1, 0x3, 0x7])
flag = [False, False, False]
def pr(seq: Bitsequence): print(''.join(map(lambda x: '01'[x], seq)))
print(data)
pr(from_bytes(data))
print(to_bytes(from_bytes(data), 3))
pr(stuffed(from_bytes(data), flag))
pr(unstuffed(stuffed(from_bytes(data), flag), flag))

my_pack = pack(
    source_address=0,
    destination_address=0,
    data=bytes([1, 2, 3, 4])
)

print(my_pack)
print(as_bits(my_pack))
print(as_bytes(as_bits(my_pack)))
print(unpack(as_bytes(as_bits(my_pack))))


# os.system(f'cat > {sys.argv[1]}')

