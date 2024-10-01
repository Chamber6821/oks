#!/bin/python3.12
import os
os.system('''
tmux new "./bridge.py SIDE1 SIDE2; tmux kill-session" \\; \\
split -l '70%' "echo Send to SIDE1 && ./transmitter.py SIDE1; tmux kill-session" \\; \\
split -h "echo Send to SIDE2 && ./transmitter.py SIDE2; tmux kill-session" \\; \\
split "echo Read from SIDE2 && ./receiver.py SIDE2; tmux kill-session" \\; \\
selectp -t 1 \\; \\
split "echo Read from SIDE1 && ./receiver.py SIDE1; tmux kill-session" \\; \\
selectp -t 1
''')
