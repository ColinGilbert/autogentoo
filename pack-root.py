#!/usr/bin/env python3

import sys, os, string

try:
    SYSTEM_ROOT_NAME = sys.argv[1]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <name of root>")

ZFS_ROOT_DATASET = open('./config/build-env/ZFS').read()
ZFS_ROOT_DATASET = ZFS_ROOT_DATASET.translate({ord(c): None for c in string.whitespace})
ZFS_SQUASHED_ROOTFS_DATASET = ZFS_ROOT_DATASET + '/squashed-roots'
SQUASHED_ROOTS_DIRECTORY = '/' + ZFS_SQUASHED_ROOTFS_DATASET

CURRENT_DIR = os.getcwd()
SYSTEM_ROOT_DIR = CURRENT_DIR + '/work/staging'


os.system('cd ' + SYSTEM_ROOT_DIR + '/dev')
os.system('mknod -m 600 console c 5 1') # Without this we cannot login to a console. This is because the initramfs doesn't create a console itself by default - even with devtmpfs enabled in-kernel.  TODO: Make optional
os.system('cd ..')
os.system('find . -print0 | cpio --null --create --verbose --format=newc | gzip  -9 > ' + SQUASHED_ROOTS_DIRECTORY  + '/initramfs-' + SYSTEM_ROOT_NAME + '.cpio.gz')
