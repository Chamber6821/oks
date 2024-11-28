#!/bin/python3.12
import os, sys, subprocess, signal


def make_bridge(side1: str, side2: str):
    return subprocess.Popen(
        ['socat', f'pty,raw,echo=0,link={side1}', f'pty,raw,echo=0,link={side2}'],
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr
    )


bridges = [
    make_bridge('from_1', 'to_2'),
    make_bridge('from_2', 'to_3'),
    make_bridge('from_3', 'to_1'),
]

try:
    os.system(r'''
    tmux new "./transmitter.py from_1" \; \
    split -h -p 67 "./transmitter.py from_2" \; \
    split -h "./transmitter.py from_3" \; \
    selectp -t 0 \; \
    split "./receiver.py to_1" \; \
    selectp -t 2 \; \
    split "./receiver.py to_2" \; \
    selectp -t 4 \; \
    split "./receiver.py to_3" \; \
    selectp -t 0 \; \
    ''')
finally:
    for bridge in bridges:
        bridge.send_signal(signal.SIGINT)
    for bridge in bridges:
        bridge.wait()
