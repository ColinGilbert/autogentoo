#!/bin/bash
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <name of system image>" >&2
  exit 1
fi

chroot ./roots/${1} /bin/bash
#env-update
. /etc/profile
export PS1="(chroot) $PS1"
