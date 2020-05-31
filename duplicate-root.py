#!/usr/bin/env python3

import sys, os, string

try:
    arg = sys.argv[2]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <name of initial system image> <name of new system image>")

ztank = open('./config/build-env/ZFS').read()
ztank = ztank.translate({ord(c): None for c in string.whitespace})

os.system('zfs unmount ' + ztank + '/distfiles')
os.system('zfs unmount ' + ztank + '/portage')
os.system('zfs unmount ' + ztank + '/pkgdir')
os.system('zfs unmount ' + ztank + '/' + arg)


snapname = ztank + '/' + arg + '@' + arg[1]
os.system('zfs snapshot ' + snapname)
os.system('zfs clone ' + snapname + ' tank/' + arg[1])
