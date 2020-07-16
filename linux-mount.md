# Working with mount

View mounted devices

```sh
mount
cat /proc/mounts
cat /etc/mtab
```

To mount a device you must first create the mount point

```sh
# mount format
mount <resource> <mount-point>

# first make the mount point
mkdir /tmp

# example
mount -t vfat /dev/sda3 /tmp # mount automatically detects filesystem type, but you may need to specify on occassion using -t
```

**note:** If you moqqunt a device over an existing directory the existing files are not lost but cannot be seen until the device is unmounted-

---

## Mount options

Mount options can be specified using -o.  Remounting commands will not be successful if any processes or files/directories are open

```sh
# to remount a device as read-only
# -ro, either specify the mount point or device both is not necessary
mount -o remount,ro /tmp # multiple options fed to -o are comma separated ','
# and back to rw
mount -o remount,rw /tmp
```

Mount using labels or UUIDs

```sh
mkdir /mnt/mnt1 /mnt/mnt2
blkid /dev/sdc1
# sample output
# /dev/sdc1: UUID="2f60a3b4‑ef6c‑4d4c‑9ef4‑50d7f75124a2" TYPE="ext3" LABEL="CentOS 7"
mount LABEL="CentOS 7" /mnt/mnt1
mount UUID="2f60a3b4‑ef6c‑4d4c‑9ef4‑50d7f75124a2" /mnt/mnt2
```

## Unmounting

**umount** Specify either the device name or the mount point

```sh
# the mount point
umount /mnt/mnt1
# or the device
umount /dev/sdc1
```

**note:** check for open files

**lsof** or **fuser**

```sh
# using mounting point
# -w option for avoiding Gnome Virtual Filesytem (gvfs) warning messages
lsof -w /mnt
# or device name
lsof -w /dev/sdc1
# with the mount point
fuser -m /mnt
# with the device name
fuser -m /dev/sdc1
```

Lazy unmount detaches the filesystem immediately and then cleans the filesystem references when it is no longer busy

**note:** always unmount removable media before disconnecting (ie: usb, dvd, floppy disks)

```sh
umount -l /mnt
```
