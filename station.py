#!/bin/python3.12 -u

import sys
from commons import Packet, Sniffer, as_bits, beautiful_bits, chain, from_bytes, from_file, stuffed, to_bytes, to_file, unpack, unstuffed, wait_flag
from config import ADDRESS_LEN, COLLISION_PROBABILITY, FCS_SIZE, FLAG, FLAG_MESSAGE, FLAG_RECEIVED, FLAG_TOKEN, JAM_LENGTH, MAX_DATA_LENGTH
from random import random
from threading import Thread
from time import sleep
from collections import defaultdict


self_address = int(sys.argv[1])
in_channel = open(f'{self_address}_in', 'r')
out_channel = open(f'{self_address}_out', 'w')

log_window = sys.stdout #open(f'{self_address}_log', 'w')
message_window = sys.stdout #open(f'{self_address}_message', 'w')


def pprint(prefix, *args, **kwargs):
    print(f'\033[7m{prefix}\033[0m', *args, **kwargs)


packets: dict[int, list[Packet]] = defaultdict(lambda: [], {})
def user_interface():
    print('Station', self_address)
    while True:
        try:
            destination = int(input('Destination: '))
            priority = int(input('Priority: '))
            message = input('Message: ') + '\n'
            length = MAX_DATA_LENGTH - 1
            message_bytes = message.encode()
            for i in range(0, len(message_bytes), length):
                message_part = bytes([FLAG_MESSAGE]) + (message_bytes[i:i+length] + bytes([0] * length))[:length]
                packets[priority].append(Packet(
                    source_address=self_address,
                    destination_address=destination,
                    data=message_part
                ))
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        except Exception as e:
            print('Stupid user!', e)


def token_source_interface():
    print('Master', self_address)
    while True:
        sleep(0.5)
        try:
            destination = int(input('Destination: '))
            priority = int(input('Priority: '))
            transmit(Packet(
                source_address=self_address,
                destination_address=destination,
                data=bytes([FLAG_TOKEN, priority])
            ))
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        except Exception as e:
            print('Stupid user!', e)


def receive():
    while True:
        channal = from_file(in_channel)
        wait_flag(channal, as_bits(FLAG))
        sniffed = Sniffer(channal)
        equippedChannal = sniffed.sequence()
        packet = unpack(to_bytes(
            equippedChannal,
            2*ADDRESS_LEN + MAX_DATA_LENGTH + FCS_SIZE
        ))
        jam = to_bytes(equippedChannal, JAM_LENGTH)
        pprint('RECEIVE', beautiful_bits(sniffed.buffer()), file=log_window)
        if int.from_bytes(jam).bit_count() > (JAM_LENGTH / 2) * 8:
            print('\033[31;7mCollision!\033[0m', file=log_window)
            continue
        return packet


def transmit(packet: Packet):
    while True:
        hasCollision = random() < COLLISION_PROBABILITY
        sniffer = Sniffer(chain(
            from_bytes(packet.as_bytes()),
            from_bytes(bytes([0xff if hasCollision else 0x00] * JAM_LENGTH))
        ))
        to_file(out_channel, from_bytes(FLAG))
        to_file(out_channel, sniffer.sequence())
        out_channel.flush()
        pprint('TRANSMIT', beautiful_bits(sniffer.buffer()), file=log_window)
        if not hasCollision: break


def station():
    while True:
        packet = receive()
        if packet.source_address == self_address:
            if packet.data[0] & FLAG_RECEIVED:
                print(f'\033[32;7mPackage received by {packet.destination_address}\033[0m', file=log_window)
            else:
                print(f'\033[31;7mPackage not received by {packet.destination_address}\033[0m', file=log_window)
            continue
        if packet.destination_address != self_address:
            transmit(packet)
            continue
        packet.data = bytes([packet.data[0] | FLAG_RECEIVED]) + packet.data[1:]
        transmit(packet)
        if packet.data[0] & FLAG_TOKEN:
            pprint('GOT TOKEN', file=log_window)
            token_priority = packet.data[1]
            for ppriority, packs in packets.items():
                if ppriority < token_priority: continue
                for p in packs:
                    transmit(p)
        else:
            print('Message:', packet.data[1:].decode(), file=message_window)


if __name__ == "__main__":
    station_daemon = Thread(target=station, daemon=True)
    station_daemon.start()
    if len(sys.argv) <= 2:
        user_interface()
    else:
        token_source_interface()
