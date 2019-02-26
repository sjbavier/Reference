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
```



