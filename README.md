# Welcome to the Autogentoo environment.

These scripts should make your life easier without being too intrusive...

## Dependencies
A basic understanding of Linux and most specifically the Gentoo meta-distribution. A modern Linux environment with ZFS. Other storage backends are forthcoming due to ZFS being stuck in a rather iffy copyright/patent(?) quagmire. At present I have found Alpine and Ubuntu the easiest to use as bootstrap hosts. Furthermore we use Python 3, rsync, cpio, pigz, and of course some Gentoo stage3's... It creates efi stub kernels for fastest loading.

## Design
These tools are used alongside the usual Gentoo workflow and currently generate EFI stub kernels with a rootfs packed into initramfs. At present there is some handcruft involved in setting up stages and kernels: This will change soon as this toolset becomes more sophisticated. I can also guarantee scripts to bootstrap fresh stages and kernels, and another to update a kernel config for use with our toolchain.

A bit of a drag is that as per Gentoo's own recommendations/requirements we end up having to run our scripts as root. I am currently considering a number of tools to ease this security burden. It is strongly recommended to use appropriate network security techniques and computer hygiene.

This thing is made to be scripted, with consistent arguments being used throughout. Feel free to use the ones listed below.

Future plans include using a proper relational database to store information, as well as a task queuer for massively-parallel builds. Currently we rely upon Gentoo's built-in *binpkg-multi-instance* feature-flag but this doesn't scale well to multiple build hosts, multiple toolchains, and multiple architectures. My eventual goal is to establish a RESTful API for doing such work scalably and securely. Also, a manner of generating, automatically disposing of, securely storing, and integrating one-time keys, or possibly even leveraging LDAP+Kerberos are things worth investigating.

We might also choose to port this whole thing to Exherbo and see how things go. The basic message here is to love that this thing exists but not to get too attached to any specifics!

## Details

### Site-specific configuration
```
./config/build-env
- Used to give values to the build-scripts.

./config/common/*
- Gets copied into all roots at packing time.

./config/overlays/hardware/your-system
./config/overlays/secret-sauce/your-apps
- The content of each of these named directories gets copied into their respective roots once made to do so by our scripts.

./config/kernel/your-kernel.kconfig
- These named configs are used to kick off a build. Note that there are a few kernel options that need setting. For example we need to enable an initramfs (compressed with pigz, a faster version of gzip) and the initramfs source should be 'root/init/initramfs.cpio.gz'.
```

### The scripts
```
./bootstrap-workdir.py
- You'll want to call this one at the beginning of your day's work/

./bootstrap-chroot.py
- Called once per read-write root when setting it up. It is also currently used to remount distfiles, packages, and portage directories into an existing root

./cleanup-root.py
- Allows us to unmount a root. Note: Due the the non-determinism inherent in umounting filesystems across any given running Linux kernel, this script must sometimes be called more than once in order to ensure that everything has been done to completion.

./pack-portage.py
- This turns the currently active portage directory of a given active stage3 root and turns it into a SquashFS archive, ready for extra-efficient in-memory read-only mounting.

./mount-kernel.py
- Mounts a kernel sourcedir to a given rootfs, bind-mounts the directory holding initramfs and copies a kernel config into the kernel source-dir.

./pack-root.py
- This more or less does what it says on the tin. It turns your completed stage3 and some included files into a gzipped initramfs, ready for the kernel packer to cheerfully scoop it up.

./pack-kernel.py
- This script gets routinely called by your build system. Again, you get a kernel packed with an initramfs.
```
