#!/usr/bin/env python3

import sys, os, string

try:
    SYSTEM_ROOT_NAME = sys.argv[1]
    TEMP_ROOT_PATH = sys.argv[2]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <name of original root> <temp root name>")

ZFS_ROOT_DATASET = open('./config/build-env/ZFS').read()
ZFS_ROOT_DATASET = ZFS_ROOT_DATASET.translate({ord(c): None for c in string.whitespace})
CURRENT_DIR = os.getcwd()

#os.system('zfs unmount ' + ZFS_ROOT_DATASET + '/distfiles')
#os.system('zfs unmount ' + ZFS_ROOT_DATASET + '/portage')
os.system('zfs unmount ' + ZFS_ROOT_DATASET + '/pkgdir-' + SYSTEM_ROOT_NAME)
#os.system('zfs unmount ' + ZFS_ROOT_DATASET + '/' + SYSTEM_ROOT_NAME)

os.system('zfs set mountpoint=\"' + CURRENT_DIR + '/work/' + TEMP_ROOT_PATH + '/var/db/pkg\" ' + ZFS_ROOT_DATASET + '/pkgdir-' + SYSTEM_ROOT_NAME)
os.system('zfs mount ' + ZFS_ROOT_DATASET + '/pkgdir-' + SYSTEM_ROOT_NAME)

os.system('mount -t squashfs ' + '/work/portage.squash ' + CURRENT_DIR + '/work/' + TEMP_ROOT_PATH + '/var/db/repos/gentoo') 
