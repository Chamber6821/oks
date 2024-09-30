#!/bin/python3.12
import sys, os
os.system(f'socat -d -d pty,raw,echo=0,link={sys.argv[1]} pty,raw,echo=0,link={sys.argv[2]}')

