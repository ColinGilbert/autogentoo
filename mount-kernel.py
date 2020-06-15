#!/usr/bin/env python3

import sys, os, string

try:
    ROOT_NAME = sys.argv[1]
    KERNEL_SRC_NAME = sys.argv[2]
    KERNEL_CONFIG_NAME = sys.argv[3]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <name of root> <name of kernel sources> <name of kconfig>")

CURRENT_DIR = os.getcwd()
ZFS_ROOT_DATASET = open('./config/build-env/ZFS').read()
ZFS_ROOT_DATASET = ZFS_ROOT_DATASET.translate({ord(c): None for c in string.whitespace})

KERNEL_CONFIG_FILE = CURRENT_DIR + '/config/kernels/' + KERNEL_CONFIG_NAME + '.kconfig'

if not os.path.isfile(KERNEL_CONFIG_FILE):
    raise SystemExit("Could not find kernel configuration file of name " + KERNEL_CONFIG_NAME + ".kconfig")

KERNEL_DATASET_NAME = ZFS_ROOT_DATASET + '/' + KERNEL_SRC_NAME
KERNEL_FOLDER_PATH = os.getcwd() + '/roots/' + ROOT_NAME + '/usr/src/linux-autogentoo'

os.system('zfs set mountpoint=\'' + KERNEL_FOLDER_PATH + '\' ' + KERNEL_DATASET_NAME)
os.system('zfs unmount ' + KERNEL_DATASET_NAME)
os.system('zfs mount ' + KERNEL_DATASET_NAME)

#os.system('mount -t overlayfs ' + KERNEL_FOLDER_PATH)
os.system('cp ' + KERNEL_CONFIG_FILE + ' ' + KERNEL_FOLDER_PATH + '/.config')
