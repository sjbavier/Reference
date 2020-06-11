# Formatting and partitioning

## MBR partitions

Traditionally formatted into 512 byte sectors, the sectors on a disk platter can be read without moving the head constitute a track.  Disks usually have more than one platter and the collection of tracks on the various platters that can be read without moving the head is called a cylinder.

Limitations on the sizes of cylinders, heads and sectors used with DOS operating systems resulted in BIOS translating geometry values so that larger hard drives could be supported but this eventually these were insufficient.

More recent developments in disk technology have led to logical block addressing (LBA) and a more modern format GUID partitio table GPT is being used instead of MBR.

Displaying MBR partitions with fdisk and parted

```sh
fdisk -l /dev/<partition>
# example
fdisk -l /dev/sdb
# examples output
# Disk /dev/sdb: 232.9 GiB, 250059350016 bytes, 488397168 sectors
# Units: sectors of 1 * 512 = 512 bytes
# Sector size (logical/physical): 512 bytes / 512 bytes
# I/O size (minimum/optimal): 512 bytes / 512 bytes
# Disklabel type: dos
# Disk identifier: 0x000404d6
# 
# Device     Boot     Start       End   Sectors   Size Id Type
# /dev/sdb1              63    401624    401562 196.1M 83 Linux
# /dev/sdb2          401625 252786687 252385063 120.4G 83 Linux
# /dev/sdb3       252786688 375631871 122845184  58.6G 83 Linux
# /dev/sdb4       375647895 488392064 112744170  53.8G 83 Linux
parted /dev/sdb
# GNU Parted 3.2
# Using /dev/sdb
# Welcome to GNU Parted! Type 'help' to view a list of commands.
# (parted) help u
#  unit UNIT                                set the default unit to UNIT
#
#     UNIT is one of: s, B, kB, MB, GB, TB, compact, cyl, chs, %, kiB, MiB,
#         GiB, TiB
# (parted) u s
# (parted) p         
# Model: ATA HDT722525DLA380 (scsi)
# Disk /dev/sdb: 488397168s
# Sector size (logical/physical): 512B/512B
# Partition Table     : msdos
# Disk Flags: 
# 
# Number  Start       End         Size        Type     File system  Flags
#  1      63s         401624s     401562s     primary  ext3
#  2      401625s     252786687s  252385063s  primary  ext4
#  3      252786688s  375631871s  122845184s  primary  ext3
#  4      375647895s  488392064s  112744170s  primary  ext4
```


## GPT partitions

GPT supports up to 128 partitions by default. GPT disks do not have the concept of geometry as MBR disks do and were designed for use with a UEFI-based (Unified Extensible Firmware Interface) system rather than BIOS.

To display information on GPT

```sh
# to get information on all disks
parted -l
# example output
# Model: ATA SAMSUNG MZMTD512 (scsi)
# Disk /dev/sda: 512GB
# Sector size (logical/physical): 512B/512B
# Partition Table  : gpt
# Disk Flags: 
# 
# Number  Start   End     Size    File system  Name                          Flags
#  1      1049kB  1050MB  1049MB  ntfs         Basic data partition          hidden, diag
#  2      1050MB  1322MB  273MB   fat32        EFI system partition          boot, hidden, esp
#  3      1322MB  2371MB  1049MB  fat32        Basic data partition          hidden
#  4      2371MB  2505MB  134MB                Microsoft reserved partition  msftres
#  5      2505MB  470GB   467GB   ntfs         Basic data partition          msftdata
#  6      470GB   497GB   26.8GB  ntfs         Basic data partition          msftdata
#  7      497GB   512GB   15.5GB  ntfs         Basic data partition          hidden, diag
#
#
# Model:  USB DISK 2.0 (scsi)
# Disk /dev/sdb: 32.1GB
# Sector size (logical/physical): 512B/512B
# Partition Table  : gpt
# Disk Flags:
#
# Number  Start   End     Size    File system     Name  Flags
#  1      1049kB  316MB   315MB                         bios_grub
#  2      316MB   4510MB  4194MB  linux‑swap(v1)
#  3      4510MB  32.1GB  27.6GB  ext4
```

## Logical Volume Manager

With LVM as an abstract management of disk space a single filesystem can span multiple disks allowing easy manipulation of adding or removing space from filesystems

LVM manages disks using

* Physical Volumes (PVs) - either a whole drive or a partition
* Volume Groups (VGs) - a collection of 1 or more PVs - managed as one disk
* Logical Volumes (LVs) - analagous to a physical GPT or MBR partion as in a unit of space with a particular formatted filesystem (ext4, XFS ...) resides within a VG

**note** the default extent size is 4MB, be aware that all PVs in a VG must use the same extent size.


to format an exFAT partition use mkexfatfs / mkfs.exfat

```sh
mkfs.exfat /dev/sdc1
```

