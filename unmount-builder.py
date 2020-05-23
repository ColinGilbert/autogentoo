#!/usr/bin/env python3

import sys, os, string

try:
    arg = sys.argv[1]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <name of system image>")

ztank = open('./config/build-env/ZFS').read()

ztank = ztank.translate({ord(c): None for c in string.whitespace})


os.system('zfs unmount ' + ztank + '/distfiles')
os.system('zfs unmount ' + ztank + '/portage')
os.system('zfs unmount ' + ztank + '/pkgdir')
os.system('zfs unmount ' + ztank + '/' + arg)

directory = os.getcwd() + '/roots/' + arg

os.system('rm -rf ' + directory + '/*')
