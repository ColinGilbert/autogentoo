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
SYSTEM_ROOT_DIR = CURRENT_DIR + '/work/staging/' + SYSTEM_ROOT_NAME


# We have a rootfs as static as possible that we use to create an initramfs for early boot. We suitably call it "boot"
os.system('mksquashfs ' + SYSTEM_ROOT_DIR + ' ' +  SQUASHED_ROOTS_DIRECTORY + '/' + SYSTEM_ROOT_NAME + '.squash')
