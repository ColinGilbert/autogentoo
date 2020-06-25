#!/usr/bin/env python3

import sys, os, string

#noConsole = False
try:
    SYSTEM_ROOT_NAME = sys.argv[1]
    HW_CONFIG_NAME = sys.argv[2]
    SECRETSAUCE_NAME = sys.argv[3]
    # USERS_CONFIG_NAME = sys.argv[4]
    #try:
    #    NO_CONSOLE_TEXT = sys.argv[5]
    #    if NO_CONSOLE_TEXT == 'noconsole':
    #        noConsole = True
    #except IndexError:
    #    # We cool. Do nothing.
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <hw> <secret sauce>")

#ZFS_ROOT_DATASET = open('./config/build-env/ZFS').read()
#ZFS_ROOT_DATASET = ZFS_ROOT_DATASET.translate({ord(c): None for c in string.whitespace})
#ZFS_SQUASHED_ROOTFS_DATASET = ZFS_ROOT_DATASET + '/squashed-roots'
#SQUASHED_ROOTS_DIRECTORY = '/' + ZFS_SQUASHED_ROOTFS_DATASET

CURRENT_DIR = os.getcwd()
INITRAMFS = CURRENT_DIR + '/work/initramfs.cpio.gz'
# SYSTEM_ROOT_DIR = CURRENT_DIR + '/work/staging'
CONFIG_DIR = CURRENT_DIR + '/config'
HW_CONFIG_DIR = CONFIG_DIR + '/overlays/hardware/' + HW_CONFIG_NAME
SECRETSAUCE_CONFIG_DIR = CONFIG_DIR + '/overlays/secret-sauce/' + SECRETSAUCE_NAME

if not os.path.exists(HW_CONFIG_DIR):
    raise SystemExit('Nonexistent directory: ' + HW_CONFIG_DIR)
if not os.path.exists(SECRETSAUCE_CONFIG_DIR):
    raise SystemExit('Nonexistent directory: ' + SECRETSAUCE_CONFIG_DIR)

TEMP_NAME =  SYSTEM_ROOT_NAME + '-' + HW_CONFIG_NAME + '-' + SECRETSAUCE_NAME
TEMPDIR = CURRENT_DIR + '/work/temp/' + TEMP_NAME
TEMPDIR_FINAL = CURRENT_DIR + '/work/temp/' + TEMP_NAME + '-final'

if os.path.exists(TEMPDIR):
   os.system('rm -rf ' + TEMPDIR)

try:
   os.mkdir(TEMPDIR)
except OSError:
   raise SystemExit('Could not create temporary directory at ' + TEMPDIR + '. This is a problem with the underlying environment. Will not proceed any further.')

try:
    os.mkdir(TEMPDIR_FINAL)
except OSError:
    raise SystemExit('Could not create temp directory a ' + TEMPDIR_FINAL)

#os.system('mount -t tmpfs tmpfs ' + TEMPDIR)
os.system('mount -t tmpfs tmpfs ' + TEMPDIR_FINAL)

os.system('cp -R ' + HW_CONFIG_DIR + '/* ' + TEMPDIR)
os.system('cp -R ' + SECRETSAUCE_CONFIG_DIR + '/* ' + TEMPDIR)

# Without this we cannot login to a console. This is because the initramfs doesn't create a console itself by default - even with devtmpfs enabled in-kernel.
#if noConsole == True:
if not os.path.exists(TEMPDIR + '/dev'):
    os.system('mkdir ' + TEMPDIR + '/dev')

#os.system('cd ' + TEMPDIR + '/dev')
if not os.path.exists(TEMPDIR + '/dev/console'):
    os.system('mknod -m 600 ' + TEMPDIR + '/dev/console c 5 1')

# Now, we overlay
os.system('mount -t overlay overlay -o lowerdir=' + CURRENT_DIR + '/work/staging:' + TEMPDIR + ' ' + TEMPDIR_FINAL)

if os.path.exists(INITRAMFS):
    os.system('rm ' + INITRAMFS)

# We pack the initramfs .cpio.gz archive
os.system('cd ' + TEMPDIR_FINAL)

os.system('find . -print0 | cpio --null --create --verbose --format=newc | pigz -9 > ' + INITRAMFS)

# And we now finally unmount our overlay fs and delete the temporary folders

#for folderName in tempDirs:
#    if os.path.exists(folderName):
#        os.system('rm -rf ' + folderName)

os.system('umount ' + TEMPDIR_FINAL)
os.system('rm -rf  ' + TEMPDIR_FINAL)
os.system('rm -rf ' + TEMPDIR)
