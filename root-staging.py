#!/usr/bin/env python3

import sys, os, string

try:
    SYSTEM_ROOT_NAME = sys.argv[1]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <name of root>")

CURRENT_DIR = os.getcwd()
SYSTEM_ROOT_DIR = CURRENT_DIR + '/roots/' + SYSTEM_ROOT_NAME
OUTPUT_DIR = CURRENT_DIR + '/work/staging/' + SYSTEM_ROOT_NAME

os.system('umount ' + OUTPUT_DIR)
os.system('mount -t tmpfs tmpfs ' + OUTPUT_DIR)

if os.path.isfile(OUTPUT_DIR):
    raise SystemExit('Found file instead of directory at ' + OUTPUT_DIR)

if not os.path.isdir(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)


os.chdir(SYSTEM_ROOT_DIR)

os.system("rsync -aHXv --exclude 'proc/*' --exclude 'sys/*' --exclude 'dev/*' --exclude 'var/db/repos' --exclude 'var/db/pkg' --exclude 'var/cache/*' --exclude 'var/gentoo' --exclude 'var/lib/portage' --exclude 'usr/share/portage' --exclude 'root/*' --exclude 'home/*' --exclude 'var/tmp/*' --exclude 'tmp/*' --exclude 'etc/portage' --exclude 'var/log/*' --exclude 'var/lib/gentoo' --exclude '/usr/src'  . " +  OUTPUT_DIR)
