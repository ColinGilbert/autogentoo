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

print(directory)

zmount_cmd = 'zfs set mountpoint=' + directory + ' ' + ztank + '/' + arg
print(zmount_cmd)
zmount_cmd = 'zfs mount ' + ztank + '/' + arg;
os.system(zmount_cmd)

zmount_cmd = 'zfs set mountpoint=' + directory + '/var/cache/distfiles ' + ztank + '/distfiles'
print(zmount_cmd)
os.system(zmount_cmd)
zmount_cmd = 'zfs mount ' + ztank + '/distfiles'
os.system(zmount_cmd)

zmount_cmd = 'zfs set mountpoint=' + directory + '/var/db/repos/gentoo ' + ztank + '/portage'
print(zmount_cmd)
os.system(zmount_cmd)
zmount_cmd = 'zfs mount ' + ztank + '/portage'
os.system(zmount_cmd)


zmount_cmd = 'zfs set mountpoint=' + directory + '/var/cache/binpkgs ' + ztank + '/pkgdir'
print(zmount_cmd)
os.system(zmount_cmd)
zmount_cmd = 'zfs mount ' + ztank + '/pkgdir'
