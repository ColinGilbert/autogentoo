#!/usr/bin/env python3

import sys, os, string, shutil, fileinput

try:
    CONFIG_NAME = sys.argv[1]
    FILESERVER_URL = sys.argv[2]
    CLIENT_IP = sys.argv[3]
    NIC_LIST = []
    for a in sys.argv[4:]:
        NIC_LIST.append(a)
except IndexError:
    raise SystemExit("Usage: {sys.argv[0]} <config name> <server url> <client IP> <nic 0> ... <nic N>")

if len(NIC_LIST) == 0:
    raise SystemExit("At least one NIC name needed...")

CURRENT_DIR = os.getcwd()
INIT_FILE_DIR = CURRENT_DIR + '/config/init'
INIT_FILE_PATH = INIT_FILE_DIR + '/init.' + CONFIG_NAME
INIT_LIST_PATH = INIT_FILE_DIR + '/initramfs_list.' + CONFIG_NAME

shutil.copyfile(INIT_FILE_DIR + '/init.template', INIT_FILE_PATH)
shutil.copyfile(INIT_FILE_DIR + '/initramfs_list.template' , INIT_LIST_PATH)

nics_to_use = ''
counter = 0
for n in NIC_LIST:
    nics_to_use += n
    counter += 1
    if counter < len(NIC_LIST):
        nics_to_use += ' '

# We search and replace within the init file
with fileinput.FileInput(INIT_FILE_PATH, inplace = True) as file:
    for line in file:
        print(line.replace('SERVER_URL=', 'SERVER_URL=\"' + FILESERVER_URL + '\"'), end = '')

with fileinput.FileInput(INIT_FILE_PATH, inplace = True) as file:
    for line in file:
         print(line.replace('ETHS=', 'ETHS=\"' + nics_to_use + '\"'), end = '')

with fileinput.FileInput(INIT_FILE_PATH, inplace = True) as file:
    for line in file:
        print(line.replace('CLIENT_IP=', 'CLIENT_IP=\"' + CLIENT_IP + '\"'), end = '')

# Now we replace within the initlist
with fileinput.FileInput(INIT_LIST_PATH, inplace = True) as file:
    for line in file:
        print(line.replace('INIT', 'init.' + CONFIG_NAME), end = '')
