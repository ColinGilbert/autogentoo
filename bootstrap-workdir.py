#!/usr/bin/env python3

import sys, os

CURRENT_DIR = os.getcwd()
WORK_DIR = CURRENT_DIR + '/work'
STAGING_DIR = WORK_DIR + '/staging'
CONFIG_DIR = CURRENT_DIR + '/config'
TEMP_DIR = WORK_DIR + '/temp'

if not os.path.isdir(WORK_DIR):
    os.mkdir(WORK_DIR)

os.system('umount ' + STAGING_DIR)
os.system('umount ' + CONFIG_DIR)
os.system('umount ' + TEMP_DIR)
#os.system('rm -rf ' + WORK_DIR + '/*')
os.system('rm -rf ' + CONFIG_DIR + '/*')

#if os.listdir(WORK_DIR): # If the working directory isn't empty...
#    raise SystemExit(WORK_DIR + " has things in it. It shouldn't. Please investigate. Cheers!")
if os.listdir(CONFIG_DIR): # Same. TODO: Turn into function or loop.
    raise SystemExit(CONFIG_DIR + " isn't empty. Please deal with it. Thanks!")
#os.mkdir(STAGING_DIR)
#os.mkdir(TEMP_DIR)

os.system('mount -t tmpfs -o size=10G tmpfs ' + STAGING_DIR)
os.system('mount -t tmpfs -o size=5G tmpfs ' + TEMP_DIR)
