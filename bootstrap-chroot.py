#!/usr/bin/env python3

import sys, os, string

readonlyportage = True

try:
    arg = sys.argv[1]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <name of system image> [rw]")

try:
    r = sys.argv[2]
    if r == 'rw':
            readonlyportage = False
except IndexError:
    # Do nothing!
    print('Mounting portage in squashfs')

ztank = open('./config/build-env/ZFS').read()
ztank = ztank.translate({ord(c): None for c in string.whitespace})

os.system('zfs unmount ' + ztank + '/distfiles')
os.system('zfs unmount ' + ztank + '/portage')
os.system('zfs unmount ' + ztank + '/pkgdir')
os.system('zfs unmount ' + ztank + '/' + arg)

CURRENT_DIR = os.getcwd()
ROOT_DIR = CURRENT_DIR + '/roots/' + arg
PORTAGE_DIR = ROOT_DIR + '/var/db/repos/gentoo'
PORTAGE_SQUASH = CURRENT_DIR  + "/work/portage.squash"

zmount_cmd = 'zfs set mountpoint=' + ROOT_DIR + ' ' + ztank + '/' + arg
#print(zmount_cmd)
os.system(zmount_cmd)
zmount_cmd = 'zfs mount ' + ztank + '/' + arg;
os.system(zmount_cmd)

zmount_cmd = 'zfs set mountpoint=' + ROOT_DIR + '/var/cache/distfiles ' + ztank + '/distfiles'
#print(zmount_cmd)
os.system(zmount_cmd)
zmount_cmd = 'zfs mount ' + ztank + '/distfiles'
os.system(zmount_cmd)

if readonlyportage:
    os.system('mount -t squashfs -o loop,nodev,noexec ' + PORTAGE_SQUASH + ' ' + PORTAGE_DIR)
else:
    zmount_cmd = 'zfs set mountpoint=' + PORTAGE_DIR + ' ' + ztank + '/portage'
    #print(zmount_cmd)
    os.system(zmount_cmd)
    zmount_cmd = 'zfs mount ' + ztank + '/portage'
    os.system(zmount_cmd)

zmount_cmd = 'zfs set mountpoint=' + ROOT_DIR + '/var/cache/binpkgs ' + ztank + '/pkgdir'
#print(zmount_cmd)
os.system(zmount_cmd)
zmount_cmd = 'zfs mount ' + ztank + '/pkgdir'
os.system(zmount_cmd)


os.system('mount --rbind --make-rslave /dev ' + ROOT_DIR + '/dev')
os.system('mount -t proc /proc ' + ROOT_DIR + '/proc')
os.system('mount --rbind --make-rslave /sys ' + ROOT_DIR + '/sys')
os.system('mount --rbind --make-rslave /tmp ' + ROOT_DIR + '/tmp')


#TODO: Move to root-bootstrap.py
#os.system('cp -R ./config/common/etc/resolv.conf ' + ROOT_DIR + '/etc')
#config_dir = './config/roots/' + arg
#os.system('cp -R ' + config_dir + '/* ' + ROOT_DIR)
#os.system('cat config/common/etc/portage/make.conf ' + config_dir + '/etc/portage/make.conf > ' + ROOT_DIR + '/etc/portage/make.conf')

