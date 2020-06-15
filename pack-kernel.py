#!/usr/bin/env python3

import sys, os, string

try:
    SYSTEM_ROOT_NAME = sys.argv[1]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <name of kernel> <name of root>")

CURRENT_DIR = os.getcwd()
SYSTEM_ROOT_DIR = CURRENT_DIR + '/work/' + SYSTEM_ROOT_NAME
OUTPUT_DIR = CURRENT_DIR + '/work'

# Mount the squashed rootfs via ZFS
# os.system('zfs set mountpoint=\"' +  + '\" ' + ' ')

# Chroot into our chosen, existing root ((to ensure our kernel and userspace compiler versions match up!)
