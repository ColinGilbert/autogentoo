#!/usr/bin/env python3

import sys, os, string

try:
    ROOT_FS_NAME = sys.argv[1]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <name of system image>")


ZFS_ROOT_DATASET = open('./config/build-env/ZFS').read()

ZFS_ROOT_DATASET = ZFS_ROOT_DATASET.translate({ord(c): None for c in string.whitespace})


os.system('zfs unmount ' + ZFS_ROOT_DATASET + '/distfiles')
os.system('zfs unmount ' + ZFS_ROOT_DATASET + '/pkgdir')

DIRECTORY = os.getcwd() + '/roots/' + ROOT_FS_NAME


UMOUNT_COMMAND = 'umount -fl '

os.system(UMOUNT_COMMAND + DIRECTORY + '/dev')
os.system(UMOUNT_COMMAND + DIRECTORY + '/sys')
os.system(UMOUNT_COMMAND + DIRECTORY + '/proc')
os.system(UMOUNT_COMMAND + DIRECTORY + '/tmp')
os.system(UMOUNT_COMMAND + DIRECTORY + '/var/db/pkg')
os.system(UMOUNT_COMMAND + DIRECTORY + '/var/db/repos/gentoo')
os.system(UMOUNT_COMMAND + DIRECTORY + '/usr/src/linux')
os.system(UMOUNT_COMMAND + DIRECTORY)

os.system('zfs unmount ' + ZFS_ROOT_DATASET + '/' + ROOT_FS_NAME)

#os.system('rm -rf ' + DIRECTORY + '/*')

