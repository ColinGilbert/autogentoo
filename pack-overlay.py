#!/usr/bin/env python3

import sys, os, string

BASE_DIR = os.getcwd() + '/config/overlays'

try:
    OVERLAY_TYPE = sys.argv[1]
    if OVERLAY_TYPE == 'hw':
        BASE_DIR += '/hardware'
    elif OVERLAY_TYPE == 'user':
        BASE_DIR += '/userland'
    else:
        raise SystemExit('Must specify either \'hw\' or \'user\' as target. Got: ' + OVERLAY_TYPE)
    CONFIG_NAME = sys.argv[2]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <hw|user> <name>")

BASE_DIR += '/' + CONFIG_NAME

if not os.path.isdir(BASE_DIR):
    raise SystemExit("Nonexistent " + BASE_DIR)

OUTPUT_FILE = os.getcwd() + '/work/' + CONFIG_NAME + '-' + OVERLAY_TYPE + '.squash'

if os.path.isfile(OUTPUT_FILE):
    os.system('rm ' + OUTPUT_FILE)

os.system('mksquashfs ' + BASE_DIR + ' ' + OUTPUT_FILE)
