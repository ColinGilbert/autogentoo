#!/usr/bin/env python3

import sys, os, string
from datetime import datetime

ztank = open('./config/build-env/ZFS').read()
ztank = ztank.translate({ord(c): None for c in string.whitespace})

os.system('zfs snapshot ' + ztank + '/distfiles' + '@' + datetime.now().strftime("%Y:%m:%d-%H:%M:%S"))
