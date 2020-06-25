#!/usr/bin/env python3

import sys, os

CURRENT_DIR = os.getcwd()
WORK_DIR = CURRENT_DIR + '/work'
STAGING_DIR = WORK_DIR + '/staging'

if not os.path.isdir(WORK_DIR):
    os.mkdir(WORK_DIR)

os.system('umount ' + WORK_DIR)

if os.listdir(WORK_DIR): # If the working directory isn't empty...
    raise SystemExit(WORK_DIR + " has things in it. It shouldn't. Please investigate. Cheers!")

os.system('mount -t tmpfs tmpfs ' + WORK_DIR)

os.mkdir(STAGING_DIR)
