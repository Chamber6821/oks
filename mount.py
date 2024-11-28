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
    make_bridge('0_out', '1_in'),
    make_bridge('1_out', '2_in'),
    make_bridge('2_out', '3_in'),
    make_bridge('3_out', '0_in'),
]

try:
    os.system(r'''
    tmux new "./station.py 0 master" \; \
    split -h "./station.py 2" \; \
    split -h "./station.py 3" \; \
    selectp -t 0 \; \
    split -h "./station.py 1" \; \
    selectp -t 0 \; \
    ''')
finally:
    for bridge in bridges:
        bridge.send_signal(signal.SIGINT)
    for bridge in bridges:
        bridge.wait()
