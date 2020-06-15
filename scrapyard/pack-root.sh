#!/bin/bash

if ["$#" -ne 1]; then
	echo "Use: $0 <name of root to pack>" > &2
	exit 1
fi

cleanup-chroot.py 
