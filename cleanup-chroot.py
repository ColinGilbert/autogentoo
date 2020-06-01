#!/usr/bin/env python3

import sys, os, string

try:
    arg = sys.argv[1]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <name of system image>")




ztank = open('./config/build-env/ZFS').read()

ztank = ztank.translate({ord(c): None for c in string.whitespace})


os.system('zfs unmount ' + ztank + '/distfiles')
os.system('zfs unmount ' + ztank + '/pkgdir')

directory = os.getcwd() + '/roots/' + arg


cmd = 'umount -fl '

os.system(cmd + directory + '/dev')
os.system(cmd + directory + '/sys')
os.system(cmd + directory + '/proc')
os.system(cmd + directory + '/tmp')
os.system(cmd + directory + '/var/db/repos/gentoo')
os.system(cmd + directory + '/usr/src/linux')
os.system(cmd + directory)

#os.system('zfs unmount ' + ztank + '/' + arg)

#os.system('rm -rf ' + directory + '/*')

