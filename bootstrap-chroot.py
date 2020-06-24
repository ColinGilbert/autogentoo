#!/usr/bin/env python3

# TODO: Apply DRY (ie: Remove copy&paste code) for glory!

import sys, os, string

readonlyportage = True

try:
    SYSTEM_ROOT_NAME = sys.argv[1]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <name of system image> [rw]")

try:
    r = sys.argv[2]
    if r == 'rw':
            readonlyportage = False
except IndexError:
    # Do nothing!
    print('Mounting portage in squashfs')

ZFS_ROOT_DATASET = open('./config/build-env/ZFS').read()
ZFS_ROOT_DATASET = ZFS_ROOT_DATASET.translate({ord(c): None for c in string.whitespace})

os.system('zfs unmount ' + ZFS_ROOT_DATASET + '/distfiles')
os.system('zfs unmount ' + ZFS_ROOT_DATASET + '/portage')
os.system('zfs unmount ' + ZFS_ROOT_DATASET + '/pkgdir')
os.system('zfs unmount ' + ZFS_ROOT_DATASET + '/' + SYSTEM_ROOT_NAME)

CURRENT_DIR = os.getcwd()
ROOT_DIR = CURRENT_DIR + '/roots/' + SYSTEM_ROOT_NAME
PORTAGE_DIR = ROOT_DIR + '/var/db/repos/gentoo'
PORTAGE_SQUASH = CURRENT_DIR  + "/work/portage.squash"

ZMOUNT_COMMAND = 'zfs set mountpoint=' + ROOT_DIR + ' ' + ZFS_ROOT_DATASET + '/' + SYSTEM_ROOT_NAME
#print(ZMOUNT_COMMAND)
os.system(ZMOUNT_COMMAND)
ZMOUNT_COMMAND = 'zfs mount ' + ZFS_ROOT_DATASET + '/' + SYSTEM_ROOT_NAME;
os.system(ZMOUNT_COMMAND)

ZMOUNT_COMMAND = 'zfs set mountpoint=' + ROOT_DIR + '/var/cache/distfiles ' + ZFS_ROOT_DATASET + '/distfiles'
#print(ZMOUNT_COMMAND)
os.system(ZMOUNT_COMMAND)
ZMOUNT_COMMAND = 'zfs mount ' + ZFS_ROOT_DATASET + '/distfiles'
os.system(ZMOUNT_COMMAND)

if readonlyportage:
    os.system('mount -t squashfs -o loop,nodev,noexec ' + PORTAGE_SQUASH + ' ' + PORTAGE_DIR)
else:
    ZMOUNT_COMMAND = 'zfs set mountpoint=' + PORTAGE_DIR + ' ' + ZFS_ROOT_DATASET + '/portage'
    #print(ZMOUNT_COMMAND)
    os.system(ZMOUNT_COMMAND)
    ZMOUNT_COMMAND = 'zfs mount ' + ZFS_ROOT_DATASET + '/portage'
    os.system(ZMOUNT_COMMAND)

ZMOUNT_COMMAND = 'zfs set mountpoint=' + ROOT_DIR + '/var/cache/binpkgs ' + ZFS_ROOT_DATASET + '/pkgdir'
#print(ZMOUNT_COMMAND)
os.system(ZMOUNT_COMMAND)
ZMOUNT_COMMAND = 'zfs mount ' + ZFS_ROOT_DATASET + '/pkgdir'
os.system(ZMOUNT_COMMAND)


os.system('mount --rbind --make-rslave /dev ' + ROOT_DIR + '/dev')
os.system('mount -t proc /proc ' + ROOT_DIR + '/proc')
os.system('mount --rbind --make-rslave /sys ' + ROOT_DIR + '/sys')
os.system('mount --rbind --make-rslave /tmp ' + ROOT_DIR + '/tmp')

#os.system('cp ' + SYSTEM_ROOT_DIR + '/bin/busybox ' + INIT_FILE_DIR)
