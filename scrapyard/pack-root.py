#!/usr/bin/env python3

import sys, os, string

try:
    SYSTEM_ROOT_NAME = sys.argv[1]
    PORTAGE_CONFIG_NAME = sys.argv[2]
    USER_INSTALLED_FILES_CONFIG_NAME = sys.argv[3]
    #HOOKS_CONFIG_NAME = sys.argv[4]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <root> <portage config>")

CURRENT_DIR = os.getcwd()

# Check for presence of required configs

ORIGINAL_ROOT_DIR = CURRENT_DIR + '/roots/' + SYSTEM_ROOT_NAME
PORTAGE_CONFIG_DIR = CURRENT_DIR + '/config/portages/' + PORTAGE_CONFIG_NAME
USER_INSTALLED_FILES_CONFIG_DIR = CURRENT_DIR + '/config/user-files/' + USER_INSTALLED_FILES_CONFIG_NAME
#HOOKS_CONFIG_DIR = CURRENT_DIR + '/config/hooks/' + HOOKS_CONFIG_NAME

ERROR_MSG = 'Nonexistent configuration directory for'

if (!os.path.isdir(ORIGINAL_ROOT_DIR))
    raise SystemExit(ERROR_MSG + ' system root.')
if (!os.path.isdir(PORTAGE_CONFIG_DIR))
    raise SystemExit(ERROR_MSG + ' portage.')
if (!os.path.isdir(USER_INSTALLED_FILES_CONFIG_DIR))
    raise SystemExit(ERROR_MSG + ' user-installed files.')
if (!os.path.isdir(HOOKS_CONFIG_DIR))
    raise SystemExit(ERROR_MSG + ' hooks.')

# Now we setup, using the good old ZFS
CLONE_NAME =  PORTAGE_CONFIG_NAME + '-' + USER_INSTALLED_FILES_CONFIG_NAME + '-' + HOOKS_CONFIG_NAME
CLONE_DIR = CURRENT_DIR + '/work/' + CLONE_NAME
PORTAGE_DIR = '/var/db/repos/gentoo'
PKG_DIR = '/var/db/pkg'

os.system('mkdir -p ' + CLONE_DIR)

ZFS_ROOT_DATASET = open('./config/build-env/ZFS').read()
ZFS_ROOT_DATASET = ZFS_ROOT_DATASET.translate({ord(c): None for c in string.whitespace})

ZFS_SNAPSHOT = ZFS_ROOT_DATASET + '/' + SYSTEM_ROOT_NAME + '@' + CLONE_NAME
ZFS_CLONE = ZFS_ROOT_DATASET + '/' + CLONE_NAME + '-clone'

os.system('zfs snapshot ' + ZFS_SNAPSHOT)
os.system('zfs clone ' + ZFS_SNAPSHOT + ' ' + ZFS_CLONE)
os.system('zfs set mountpoint=\"' + CLONE_DIR + '\" ' + ZFS_CLONE)
os.system('zfs mount ' + ZFS_CLONE)


# Collect the install-uninstall information into lists
toInstall = open(PORTAGE_CONFIGS_DIR + '/packages.install').readlines()
toRemove = open(PORTAGE_CONFIGS_DIR + '/packages.remove').readlines()

REAL_OS_ROOT = os.open('/', os.O_RDONLY)

# Chroot into our temp root and install/deinstall whichever stuff we need
os.chroot(CLONE_DIR)
if (toInstall.len() > 0)
    os.system('emerge -qv ' + ' '.join(toInstall))

if (toRemove.len() > 0)
    os.system('emerge --unmerge --rage-clean ' + ' '.join(toRemove))

os.system('emerge --depclean --with-bdeps=y --rage-clean')


# Unchroot, upgrade the clone to a fresh dataset, cleanup the script-related ZFS datasets and remount. Now the user can do cool things to it on her own!
os.fchdir(REAL_OS_ROOT)
os.chroot('.')
os.system('cp -R ' + USER_INSTALLED_FILES_CONFIG_DIR + '/* ' + CLONE_DIR)


ZFS_FRESH_ROOT = ZFS_ROOT_DATASET + '/' + CLONE_NAME
os.system('zfs create ' + ZFS_FRESH_ROOT)
os.system('zfs send ' + ZFS_CLONE + ' | zfs recv ' + ZFS_FRESH_ROOT)
# Destroy the clone, and its snapshot
os.system('zfs unmount ' + ZFS_CLONE)
os.system('zfs destroy ' + ZFS_CLONE)
os.system('zfs destroy ' + ZFS_SNAPSHOT)
os.system('zfs set mountpoint=\"' + CLONE_DIR + '\" ' + ZFS_FRESH_ROOT)
os.system('zfs mount ' + ZFS_FRESH_ROOT)
