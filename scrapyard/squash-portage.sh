#! /bin/sh

# Adapted from:  https://www.github.com/nrdvana/squash-portage
# TODO: Replace /var/tmp hardcoded with a variable. That should do it.

SQUASHFS_DIR=/usr
dt=`date +%Y%m%d`
overlay_mounted=0;

die() {
	echo "Script failed: $@";
	umount /var/tmp/oldportage 2>/dev/null;
	umount /var/tmp/newportage 2>/dev/null;
	[ "$overlay_mounted" ] && umount /usr/portage;
	exit 1;
}

which mksquashfs >/dev/null || die "mksquashfs command not found";

umount /var/tmp/oldportage 2>/dev/null
umount /var/tmp/newportage 2>/dev/null
mkdir -p /var/tmp/newportage /var/tmp/oldportage

mount -t tmpfs none /var/tmp/newportage || die "Can't mount tmpfs at /var/tmp/newportage";
mkdir /var/tmp/newportage/rw /var/tmp/newportage/work

if [ -e "$SQUASHFS_DIR/portage.sqsh" ]; then
	mount -o loop,ro "$SQUASHFS_DIR/portage.sqsh" /var/tmp/oldportage || die "Can't mount portage squashfile at /var/tmp/oldportage";
else
	echo "Warning: no $SQUASHFS_DIR/portage.sqsh, using current /usr/portage as-is.";
	mount --bind /usr/portage /var/tmp/oldportage || die "Can't bind-mount /usr/portage to /var/tmp/oldportage";
fi

if grep unionfs /proc/filesystems >/dev/null; then
	mount -t unionfs -o dirs=/var/tmp/newportage/rw=rw:/usr/portage=ro none /usr/portage || die "Can't create overlay on /usr/portage";
elif grep overlayfs /proc/filesystems >/dev/null; then
	mount -t overlayfs -o lowerdir=/var/tmp/oldportage,upperdir=/var/tmp/newportage/rw none /usr/portage || die "Can't create overlay on /usr/portage";
elif grep overlay /proc/filesystems >/dev/null; then
	mount -t overlay -o lowerdir=/var/tmp/oldportage,upperdir=/var/tmp/newportage/rw,workdir=/var/tmp/newportage/work none /usr/portage || die "Can't create overlay on /usr/portage";
else
	die "Require unionfs or overlayfs, and neither listed in /proc/filesystems";
fi
overlay_mounted=1;

emerge --sync || die "Emerge --sync failed";

if [ -f "$SQUASHFS_DIR/portage-${dt}.sqsh" ]; then
	echo "Warning: $SQUASHFS_DIR/portage-${dt}.sqsh already exists!";
	mv "$SQUASHFS_DIR/portage-${dt}.sqsh" "$SQUASHFS_DIR/portage-${dt}.sqsh.old" || die "Failed to move $SQUASHFS_DIR/portage-${dt}.sqsh";
	echo "Moved to $SQUASHFS_DIR/portage-${dt}.sqsh.old";
fi
mksquashfs /usr/portage "$SQUASHFS_DIR/portage-${dt}.sqsh" || die "mksquashfs failed";
chmod 444 "$SQUASHFS_DIR/portage-${dt}.sqsh"
ln -sf "portage-${dt}.sqsh" "$SQUASHFS_DIR/portage.sqsh" || die "Can't create symlink for portage.sqsh";

umount /usr/portage || die "Can't unmount /usr/portage";
overlay_mounted=0;
umount /var/tmp/oldportage || die "Can't unmount /var/tmp/oldportage";
umount /var/tmp/newportage || die "Can't unmount /var/tmp/newportage";

umount /usr/portage 2>/dev/null
mount "$SQUASHFS_DIR/portage.sqsh" /usr/portage || die "Can't mount new portage.sqsh"
