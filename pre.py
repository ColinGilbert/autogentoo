#!/usr/bin/env python3

import sys, os

try:
    arg = sys.argv[1]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <name of system image>")

dir = './roots/' + arg

# Right out the Gentoo manual. :)
os.system('mount --rbind /dev ' + dir + '/dev')
#os.system('mount --make-rslave ' + dir + '/dev')
os.system('mount -t proc /proc ' + dir + '/proc')
os.system('mount --rbind /sys ' + dir + '/sys')
#os.system('mount --make-rslave ' + dir + '/sys')
os.system('mount --rbind /tmp ' + dir + '/tmp')
os.system('cat configs/user/common/etc/portage/make.conf ' + dir + '/etc/portage/make.conf.local > ' + dir + '/etc/portage/make.conf')
