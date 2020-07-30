#!/bin/bash
	
if ![ -z "$2" ]
  then
    env EXTRA_ECONF='--with-linux=/usr/src/linux-autogentoo --enable-linux-builtin' ebuild /var/db/repos/gentoo/sys-fs/zfs-kmod/zfs-kmod-$2.ebuild clean configure
    cd /var/tmp/portage/sys-fs/zfs-kmod-$2/work/zfs-kmod-$2/ && ./copy-builtin /usr/src/linux-autogentoo
fi
