#!/bin/python3.12

from commons import as_bits, as_bytes, pack, unpack

MAX_DATA_LENGTH = 22 + 1
FLAG = (22).to_bytes(8, byteorder='little')
FLAG_BITS = as_bits(FLAG)

my_pack = pack(
    source_address=1,
    destination_address=3,
    data=bytes([1, 2, 3, 4])
)

print(my_pack)
print(as_bits(my_pack))
print(as_bytes(as_bits(my_pack)))
print(unpack(as_bytes(as_bits(my_pack)), data_length=4))

