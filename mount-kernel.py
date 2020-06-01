#!/usr/bin/env python3

import sys, os, string

try:
    KERNEL_NAME = sys.argv[1]
    ROOT_NAME = sys.argv[2]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <name of kernel> <name of root>")

ztank = open('./config/build-env/ZFS').read()
ztank = ztank.translate({ord(c): None for c in string.whitespace})

dataset_name = ztank + '/' + KERNEL_NAME
kernel_folder_path = os.getcwd() + '/roots/' + ROOT_NAME + '/usr/src/linux'

os.system('zfs set mountpoint=\'' + kernel_folder_path + '\' ' + dataset_name)
os.system('zfs unmount ' + dataset_name)
os.system('zfs mount ' + dataset_name)
