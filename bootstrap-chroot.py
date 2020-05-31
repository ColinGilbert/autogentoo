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

root_dir = os.getcwd() + '/roots/' + arg

#print(root_dir)

zmount_cmd = 'zfs set mountpoint=' + root_dir + ' ' + ztank + '/' + arg
#print(zmount_cmd)
os.system(zmount_cmd)
zmount_cmd = 'zfs mount ' + ztank + '/' + arg;
os.system(zmount_cmd)

zmount_cmd = 'zfs set mountpoint=' + root_dir + '/var/cache/distfiles ' + ztank + '/distfiles'
#print(zmount_cmd)
os.system(zmount_cmd)
zmount_cmd = 'zfs mount ' + ztank + '/distfiles'
os.system(zmount_cmd)

zmount_cmd = 'zfs set mountpoint=' + root_dir + '/var/db/repos/gentoo ' + ztank + '/portage'
#print(zmount_cmd)
os.system(zmount_cmd)
zmount_cmd = 'zfs mount ' + ztank + '/portage'
os.system(zmount_cmd)

zmount_cmd = 'zfs set mountpoint=' + root_dir + '/var/cache/binpkgs ' + ztank + '/pkgdir'
#print(zmount_cmd)
os.system(zmount_cmd)
zmount_cmd = 'zfs mount ' + ztank + '/pkgdir'
os.system(zmount_cmd)


os.system('mount --rbind --make-rslave /dev ' + root_dir + '/dev')
os.system('mount -t proc /proc ' + root_dir + '/proc')
os.system('mount --rbind --make-rslave /sys ' + root_dir + '/sys')
os.system('mount --rbind --make-rslave /tmp ' + root_dir + '/tmp')


#TODO: Move to root-bootstrap.py
#os.system('cp -R ./config/common/etc/resolv.conf ' + root_dir + '/etc')
#config_dir = './config/roots/' + arg
#os.system('cp -R ' + config_dir + '/* ' + root_dir)
#os.system('cat config/common/etc/portage/make.conf ' + config_dir + '/etc/portage/make.conf > ' + root_dir + '/etc/portage/make.conf')

