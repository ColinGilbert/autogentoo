#!/usr/bin/env python3

import sys, os

try:
    arg = sys.argv[1]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <name of system image>")

dir = './roots/' + arg
cmd = 'umount -fl '

os.system(cmd + dir + '/dev')
os.system(cmd + dir + '/sys')
os.system(cmd + dir + '/proc')
os.system(cmd + dir + '/tmp')
