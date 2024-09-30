from typing import IO, Generator, List


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


def pack(*, source_address: int, destination_address: int, data: bytes) -> bytes:
    fcs = 0
    return (source_address.to_bytes(4, byteorder='little')
        + destination_address.to_bytes(4, byteorder='little')
        + data
        + fcs.to_bytes())


def unpack(packet: bytes, data_length: int):
    return {
        'source_address': as_int(packet[0:3]),
        'destination_address': as_int(packet[4:7]),
        'data': packet[8:8 + data_length]
    }

