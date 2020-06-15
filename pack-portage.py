#!/usr/bin/env python3

# TODO: Apply DRY (ie: Remove copy&paste code) for glory!

import sys, os, string

readonlyportage = True

try:
    SYSTEM_ROOT_NAME = sys.argv[1]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <name of system root, with portage synced>")

CURRENT_DIR = os.getcwd()
ROOT_DIR = CURRENT_DIR + '/roots/' + SYSTEM_ROOT_NAME
PORTAGE_DIR = ROOT_DIR + '/var/db/repos/gentoo'
PORTAGE_SQUASH = CURRENT_DIR  + "/work/portage.squash"

os.system('mksquashfs ' + PORTAGE_DIR + ' ' + PORTAGE_SQUASH)
