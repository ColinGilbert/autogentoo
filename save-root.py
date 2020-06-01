#!/usr/bin/env python3

import sys, os, string
from datetime import datetime

try:
    arg = sys.argv[1]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <name of system image>")

ztank = open('./config/build-env/ZFS').read()
ztank = ztank.translate({ord(c): None for c in string.whitespace})

os.system('./cleanup-chroot.py ' + arg)
os.system('zfs snapshot ' + ztank + '/' + arg + '@' + datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
