# Working with filesystems in Linux

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

## Fixing filesystems

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
