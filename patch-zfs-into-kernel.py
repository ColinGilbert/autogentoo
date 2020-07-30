#!/usr/bin/env python3

import os, sys, fileinput

try:
    ROOTFS = sys.argv[1]
    ZFS_VERSION = sys.argv[2]
except IndexError:
    raise SystemExit("Usage: {sys.argv[0]}  <name-of-root> <zfs-version>")


CURRENT_DIR = os.getcwd()
CHROOT_DIR = CURRENT_DIR + '/roots/' + ROOTFS
SYSTEM_ROOT_DIR = os.open('/', os.O_PATH)
#CONFIG_FILE_PATH = '/usr/src/linux-autogentoo/.config'
os.system('mount --bind ./chroot-scripts ./roots/' + ROOTFS) 
os.chdir(CHROOT_DIR)
os.chroot('.')


os.system('./patch-zfs-into-kernel.sh ' + ROOTFS + ' ' + ZFS_VERSION)


#os.system('emerge --fetchonly zfs-kmod')


#CONFIG_MODULES_OPTION_ORIGINAL_TEXT = '# CONFIG_MODULES is not set'
#CONFIG_MODULES_OPTION_YES_TEXT = 'CONFIG_MODULES=y'

# We search and replace within the init file
#with fileinput.FileInput(CONFIG_FILE_PATH, inplace = True) as file:
#    for line in file:
#        print(line.replace(CONFIG_MODULES_OPTION_ORIGINAL_TEXT, CONFIG_MODULES_OPTION_YES_TEXT), end = '')
#os.environ['EXTRA_ECONF'] = '--with-linux=/usr/src/linux-autogentoo --enable-linux-builtin'
#os.system("ebuild /var/db/repos/gentoo/sys-fs/zfs-kmod/zfs-kmod-" + ZFS_VERSION + ".ebuild clean configure")
#os.system("(cd /var/tmp/portage/sys-fs/zfs-kmod-" + ZFS_VERSION + "/work/zfs-kmod-" + ZFS_VERSION + "/ && ./copy-builtin /usr/src/linux-autogentoo)")
#os.environ.pop('EXTRA_ECONF')
# We undo our changes
#with fileinput.FileInput(CONFIG_FILE_PATH, inplace = True) as file:
#    for line in file:
#        print(line.replace(CONFIG_MODULES_OPTION_YES_TEXT, CONFIG_MODULES_OPTION_ORIGINAL_TEXT), end = '')






os.fchdir(SYSTEM_ROOT_DIR)
os.chroot('.')
os.close(SYSTEM_ROOT_DIR)
os.chdir(CURRENT_DIR)
