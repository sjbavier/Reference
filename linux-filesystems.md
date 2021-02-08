# Working with filesystems in Linux

**inodes:** describes a filesystem object that stores either a directory or file, each inode stores the attributes and disk block locations of the object's data

**superblocks:** describes the filesystem metadata

```sh
# filesystem must be unmounted
# display metadata about filesystem
mke2fs -n /dev/sda3
```

## Using mkfs and mkswap for creating filesystems

mkfs comes with many different filesystem specific commands

```sh
ls /sbin/mk*
# /sbin/mkdosfs     /sbin/mkfs.cramfs   /sbin/mkfs.msdos        /sbin/mksquashfs
# /sbin/mkdumprd    /sbin/mkfs.ext2     /sbin/mkfs.vfat         /sbin/mkswap
# /sbin/mke2fs      /sbin/mkfs.ext3     /sbin/mkfs.xfs
# /sbin/mkfs        /sbin/mkfs.ext4     /sbin/mkhomedir_helper
# /sbin/mkfs.btrfs  /sbin/mkfs.ext4dev  /sbin/mkinitrd
```

To create an exfat filesystem

```sh

mkfs.exfat /dev/sdc1
# or
mkfs -t exfat /dev/sdc1
```

To create an ext4

```sh
mkfs -t ext4 /dev/sda1
# or
mkfs.ext4 /dev/sda1
```

For extensions ext2, ext3, and ext4 you can use the -L option to label the partition (max 16 chars)

```sh
mkfs.ext4 -L <name> /dev/sda1
```

**note:** a journal is created, if you wish to add a journal to an existing ext2, ext3 or ext4 system use **tune2fs -j**

Using mkfs to create an **XFS** filesystem.  If you are using SELinux you should specifylarger inodes than the default 256 using -i to the recommended 512 needed for SELinux XATTR

```sh
mkfs -t xfs -i size=512 /dev/sdc2
# to relabel an existing XFS system with
# on XFS the maximum is 12 characters
# xfs_admin with the -L option and
# xfs_admin -l to list the existing label

### Universally unique identifier or UUID
```

mkswap for creating a swap space

```sh
mkswap /dev/sdc2
# swap partitions aren't mounted
# instead they use swapon
```

---

## Fixing filesystems

**note:** filesystems should be unmounted while checking
running the inappropriate checker for filesystem type will lead to corruption!

using **fsck** to check filesystems

```sh
# check all filesystems
fsck -A
# check all filesystems except root
fsck -AR
# checks filesystems even if they are clean
fsck -f
# fix safe problems automatically
fsck -a
# answers yes to all questions
fsck -y
# answers no, just displays results
fsck -n
```

---

## fstab

Enables mounting options upon boot: **/etc/fstab**

```sh
# filesystem              mount point                               type    options      dump pass
# UUID=2f60a3b4‑ef6c‑4d4c‑9ef4‑50d7f75124a2 /                       ext3    defaults        1 1
# UUID=3c3de27e‑779a‑44d5‑ad7a‑61c5fd03d9e7 /grubfile               ext3    defaults        1 2
# tmpfs                                     /dev/shm                tmpfs   defaults        0 0
# devpts                                    /dev/pts                devpts  gid=5,mode=620  0 0
# sysfs                                     /sys                    sysfs   defaults        0 0
# proc                                      /proc                   proc    defaults        0 0

# <f1=block-device:UUID or Label>   <f2=mount-point>  <f3=file-system-type> <f4=options>  <f5=dump? 0=false 1=true>  <f6=passno? fsck root=1 other=2 n/a=0>
```

Additional info on **fstab**

- f1 Block Device:
  - nfs mounts format: host:dir
  - UUID format: UUID=UUID
  - Label format: LABEL=label
- f2 Mount:
  - swap partitions should be specified as 'none'
  - spaces need escaping as '\040'
- f3 FS type:
  - see /proc/filesystems for all supported types
- f4 Options:
  - A comma separated list of options see **mount** or **swapon**
  - defaults: rw, suid, dev, exec, auto, nouser, async
  - noauto: do not mount when 'mount -a' is given
  - user: allow user to mount
  - owner: allow device owner to mount
  - comment: or x-<name> for fstab-maintaining programs
  - nofail: do not report errors if this device does not exist
- f5 Dump:
  - determine which filesystems need to be **dump** 0=false 1=true
- f6 Passno:
  - determine which filesystems are checked at boot
  - root should be specified as '1'
  - other filesystems as '2'
  - no field present is assumed as '0' meaning no checking with fsck

## Autofs

The downside of mounting NFS is the system has to allocate necessary resources to keep the share mounted always.  Autofs was created to only mount the system 'on-demand' and unmount after a period of inactivity

Autofs reads /etc/auto.master which contains the following format

```conf
# example /etc/auto.master
<mount-point>       <map-file>
# example
/media/nfs          /etc/auto.nfs-share     --timeout=60
```

Continuing the example above, /etc/auto.master points to a file /etc/auto.nfs-share:

```conf
# this mounts the writeable fs to /media/nfs
writeable_share -fstype=rw  192.168.0.10:/
# this read-only share will be mounted to /media/nfs/read-only-dir
non_writeable_share -fstype=ro  192.168.0.10:/read-only-dir
```


## Creating backup of ext filesystem

using **dump**

```sh
dump -0uf /path-of-backup/<file.dump> /dev/<logical-group>/<logical-volume>
# or pipe to remote server
dump -0uf /path-of-backup/<file.dump> /dev/<logical-group>/<logical-volume> | ssh <user>@<host> "dd of=<file.dump>"
```

**restore** the backup

```sh
# make sure the ext4 volume is formatted to the proper filesystem
mkfs -t ext4 /dev/<logical-group>/<logical-volume>
# mount
mount /dev/<logical-group>/<logical-volume> /media/restore
# run restore
restore -rf /path-of-backup/<file.dump> /media/restore
# you may have to edit /etc/fstab to match the logical volume before rebooting
```

---

## Displaying usage information

**df** command

```sh
# display filesystem information including -T type
df -T
# display information in human readable -h
df -Th
# for information about inodes
df -i
```

**du** disk usage

```sh
# summary includes .hidden files
du -s <directory>
# for multiple directories -c total, -h human readable
du -ch *
# -s summary, -c total, -h human readable
du -chs .
```

To view largest directories on system

```sh
du -a | sort -n -r | head -n 5

   # du command: Estimate file space usage.
   # a : Displays all files and folders.
   # sort command : Sort lines of text files.
   # -n : Compare according to string numerical value.
   # -r : Reverse the result of comparisons.
   # head : Output the first part of files.
   # -n : Print the first ‘n’ lines. (In our case, We displayed first 5 lines).

du -hs * | sort -rh | head -5

   # du command: Estimate file space usage.
   # -h : Print sizes in human readable format (e.g., 10MB).
   # -S : Do not include size of subdirectories.
   # -s : Display only a total for each argument.
   # sort command : sort lines of text files.
   # -r : Reverse the result of comparisons.
   # -h : Compare human readable numbers (e.g., 2K, 1G).
   # head : Output the first part of files.

du -Sh | sort -rh | head -5
```

---

### Tools for ext2, ext3 and ext4

**tune2fs** for ext filesystems

Display filesystem info including block count and whether it is journaled

```sh
# -l for list
tune2fs -l /dev/sdc4
```

**tune2fs**
Adjusts parameters on ext2 and ext3 filesystems. Use this to add a journal to an ext2 system, making it an ext3 system, as well as display or set the maximum number of mounts before a check is forced. You can also assign a label and set or disable various optional features.

**dumpe2fs**
Prints the super block and block group descriptor information for an ext2 or ext3 filesystem.

**debugfs**
Is an interactive filesystem debugger. Use it to examine or change the state of an ext2 or ext3 filesystem.

### Tools for XFS

**xfs_info** for XFS

Display filesystem information

```sh
xfs_info /dev/sdc5
```

**xfs_info**
Displays XFS filesystem information.

**xfs_growfs**
Expands an XFS filesystem (assuming another partition is available).

**xfs_admin**
Changes the parameters of an XFS filesystem.

**xfs_repair**
Repairs an XFS filesystem when the mount checks are not sufficient to repair the system.

**xfs_db**
Examines or debugs an XFS filesystem.
