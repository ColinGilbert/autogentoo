#!/usr/bin/env python3

import sys, os, string

try:
    SYSTEM_ROOT_NAME = sys.argv[1]
    HW_CONFIG_NAME = sys.argv[2]
    SECRET_SAUCE_NAME = sys.argv[3]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <name of root> <hw> <secret-sauce>")

CURRENT_DIR = os.getcwd()
SYSTEM_ROOT_DIR = CURRENT_DIR + '/roots/' + SYSTEM_ROOT_NAME
STAGING_DIR = CURRENT_DIR + '/work/staging/'
INITRAMFS = CURRENT_DIR + '/work/initramfs.cpio.gz'
CONFIG_DIR = CURRENT_DIR + '/config'
HW_CONFIG_DIR = CONFIG_DIR + '/overlays/hardware/' + HW_CONFIG_NAME
SECRET_SAUCE_CONFIG_DIR = CONFIG_DIR + '/overlays/secret-sauce/' + SECRET_SAUCE_NAME
TEMP_CPIO_FILE = CURRENT_DIR + '/work/temp/temp.cpio' # We do not pipe, as pigz has some issues with that.

if not os.path.exists(HW_CONFIG_DIR):
    raise SystemExit('Nonexistent directory: ' + HW_CONFIG_DIR)
if not os.path.exists(SECRET_SAUCE_CONFIG_DIR):
    raise SystemExit('Nonexistent directory: ' + SECRET_SAUCE_CONFIG_DIR)
if os.path.isfile(STAGING_DIR):
    raise SystemExit('Found file instead of directory at ' + STAGING_DIR)
if not os.path.isdir(STAGING_DIR):
    os.mkdir(STAGING_DIR)

os.system('umount ' + STAGING_DIR)
os.system('mount -t tmpfs tmpfs ' + STAGING_DIR)

os.chdir(SYSTEM_ROOT_DIR)
os.system("rsync -aHX --exclude 'proc/*' --exclude 'sys/*' --exclude 'dev/*' --exclude 'var/db/repos' --exclude 'var/db/pkg' --exclude 'var/cache/*' --exclude 'var/gentoo' --exclude 'var/lib/portage' --exclude 'usr/share/portage' --exclude 'root/*' --exclude 'home/*' --exclude 'var/tmp/*' --exclude 'tmp/*' --exclude 'etc/portage' --exclude 'var/log/*' --exclude 'var/lib/gentoo' --exclude '/usr/src' --exclude '/usr/share/doc/*' --exclude '/usr/share/man/*' . " +  STAGING_DIR)

os.system('cp -R ' + HW_CONFIG_DIR + '/* ' + STAGING_DIR)
os.system('cp -R ' + SECRET_SAUCE_CONFIG_DIR + '/* ' + STAGING_DIR)

if not os.path.exists(STAGING_DIR + '/dev'):
    os.system('mkdir ' + STAGING_DIR + '/dev')
if not os.path.exists(STAGING_DIR + '/dev/console'):
    os.system('mknod -m 600 ' + STAGING_DIR + '/dev/console c 5 1')
if not os.path.exists(INITRAMFS):
    os.system('rm ' + INITRAMFS)

# TODO: Remove portage user and group, and emerge-related binaries

os.chdir(STAGING_DIR)

if os.path.isfile(TEMP_CPIO_FILE):
    os.system('rm ' + TEMP_CPIO_FILE)

if os.path.isfile(INITRAMFS):
    os.system('rm ' + INITRAMFS)

os.system('find . -print0 | cpio --null --create --verbose --format=newc  > ' + TEMP_CPIO_FILE)
os.system('pigz -9 ' + TEMP_CPIO_FILE)
os.system('mv ' + TEMP_CPIO_FILE + '.gz ' + INITRAMFS)
