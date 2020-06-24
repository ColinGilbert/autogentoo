#!/usr/bin/env python3

import sys, os, string, shutil

try:
    KERNEL_SRC = sys.argv[1]
    KERNEL_CONF = sys.argv[2]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <kernel sources> <kernel config>")

CURRENT_DIR = os.getcwd()
ROOTFS = 'boot'
SYSTEM_ROOT_DIR = CURRENT_DIR + '/roots/' + ROOTFS
OUTPUT_DIR = CURRENT_DIR + '/work'
#KCONFIG_FILE = CURRENT_DIR + '/config/kernel/' + KERNEL_CONF + '.kconfig'

#if not os.isfile(KCONFIG_FILE):
#    raise SystemExit('Could not find ' + KCONFIG_FILE)

os.system('./mount-kernel.py ' + ' ' + ROOTFS + ' ' + KERNEL_SRC + ' ' + KERNEL_CONF)

kernelSourcePath = '/usr/src/linux-autogentoo'

realRoot = os.open('/', os.O_PATH)
os.chdir(SYSTEM_ROOT_DIR)
os.chroot('.')
os.chdir(kernelSourcePath)
os.system('make -j4')
os.fchdir(realRoot)
os.chroot('.')
os.close(realRoot)
os.chdir(CURRENT_DIR)
shutil.copyfile(SYSTEM_ROOT_DIR + kernelSourcePath + '/arch/x86/boot/bzImage', OUTPUT_DIR + '/bzImage.' + KERNEL_SRC + '-' + KERNEL_CONF)# + '-' + INIT_CONF)
