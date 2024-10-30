#!/bin/python3.12
import os, sys, subprocess, signal
bridge = subprocess.Popen(
    ['socat', 'pty,raw,echo=0,link=SIDE1', 'pty,raw,echo=0,link=SIDE2'],
    stdin=sys.stdin,
    stdout=sys.stdout,
    stderr=sys.stderr
)
try:
    os.system(r'''
    tmux new "./transmitter.py SIDE1" \; \
    split "./receiver.py SIDE2" \; \
    selectp -t 0
    ''')
finally:
    bridge.send_signal(signal.SIGINT)
    bridge.wait()
