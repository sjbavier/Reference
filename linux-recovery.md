# Recovery options

## Rescue mode Centos and Ubuntu

Locate command-line rescue tools on Ubuntu

```sh
locate recovery-mode

/lib/recovery-mode
/lib/recovery-mode/l10n.sh # The ``0n.sh script sets appropriate environment variables for the menu.
/lib/recovery-mode/options
/lib/recovery-mode/recovery-menu # The recovery-menu script file
/lib/recovery-mode/options/apt-snapshots
/lib/recovery-mode/options/clean # The script for reducing disk usage
/lib/recovery-mode/options/dpkg
/lib/recovery-mode/options/failsafeX
/lib/recovery-mode/options/fsck
/lib/recovery-mode/options/grub
/lib/recovery-mode/options/network
/lib/recovery-mode/options/root
/lib/recovery-mode/options/system-summary
```

The [/lib/recovery-mode/options] fsck will check and fix, if possible, any broken file systems

```sh
. /lib/recovery-mode/options/fsck
```

Boot-repair for Ubuntu checks GRUB settings [https://help.ubuntu.com/community/Boot-Repair]
GParted Live tool helps fix corrupted partitions
SystemRescueCD is another lightweight recovery tools system

## To create a live boot drive on a USB or CD/DVD you'll need to add a MBR [master-boot-record] to the [.iso] so that the [BIOS] and [UEFI] firmware will know what to do

Use syslinux-utils isohybrid to add MBR to [.iso]

```sh
apt install syslinux-utils

isohybrid <.iso-file> # creates MBR for .iso

df -h # use this to view USB
Filesystem Size Used Avail Use% Mounted on
udev        3.5G    0 3.5G 0%   /dev
tmpfs       724M 1.5M 722M 1%   /run
/dev/sda2   910G 183G 681G 22%  /                       # this is the root filesystem DO NOT OVERWRITE
tmpfs       3.6G 214M 3.4G 6%   /dev/shm
tmpfs       5.0M 4.0K 5.0M 1%   /run/lock
tmpfs       3.6G    0 3.6G 0%   /sys/fs/cgroup
/dev/sda1   511M 3.4M 508M 1%   /boot/efi
tmpfs       724M 92K  724M 1%   /run/user/1000
/dev/sdb1   15G  16K   15G 1%   /media/myname/KINGSTON  # This is the removable USB media drive

lsblk # use list block devices to find a CD/DVD

NAME    MAJ:MIN RM  SIZE    RO  TYPE MOUNTPOINT
sda     8:0     0   931.5G  0   disk
sda1    8:1     0   512M    0   part /boot/efi
sda2    8:2     0   923.8G  0   part /
sda3    8:3     0   7.2G    0   part [SWAP]
sdb     8:16    1   14.4G   0   disk
sdb1    8:17    1   14.4G   0   part /media/myname/KINGSTON
sr0     11:0    1   1024M   0   rom # DVD

umount /dev/sdb # unmount the device
# CAREFUL! writing to USB in this case
dd bs=4M if=<.iso-file> of=/dev/sdb && sync # added sync command ensures all cached data is immediately written to target disk
```

## Recovering files from a damaged file system

If a partition is not accessible because it is unmounted

```sh
mkdir /run/temp-directory
mount /dev/sdc1 /run/temp-directory  # you can try to grab the files /run/temp-directory
```

For fixing an ext2, ext3, ext4 file system

```sh
e2fsck -f -b 32768 -y <device>

: <<'END'
-f     Force checking even if the file system seems clean.
-b superblock
       Instead  of  using  the  normal superblock, use an alternative superblock specified by superblock.
       This option is normally used when the primary superblock has been corrupted.  The location of  the
       backup superblock is dependent on the filesystem's blocksize.  For filesystems with 1k blocksizes,
       a backup superblock can be found at block 8193; for  filesystems  with  2k  blocksizes,  at  block
       16384; and for 4k blocksizes, at block 32768.

       Additional backup superblocks can be determined by using the mke2fs program using the -n option to
       print out where the superblocks were created.   The -b option to mke2fs, which specifies blocksize
       of  the filesystem must be specified in order for the superblock locations that are printed out to
       be accurate.

       If an alternative superblock is specified and the filesystem is not opened read-only, e2fsck  will
       make  sure  that the primary superblock is updated appropriately upon completion of the filesystem
       check.
-y     Assume an answer of `yes' to all questions; allows e2fsck  to  be  used  non-interactively.   This
       option may not be specified at the same time as the -n or -p options.
END
```

Also can try fsck

```sh
fsck /dev/sdc1
```

To list the partition table use fdisk -l

```sh
fdisk -l
```