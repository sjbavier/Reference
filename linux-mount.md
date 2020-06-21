# Working with mount

View mounted devices

```sh
mount
cat /proc/mounts
cat /etc/mtab
```

To mount a device you must first create the mount point

```sh
mkdir /tmp/
mount -t vfat /dev/sda3 /tmp # mount automatically detects filesystem type, but you may need to specify on occassion using -t
```

If you moqqunt a device over an existing directory the existing files are not lost but cannot be seen until the device is unmounted

Mount options can be specified using -o.  Remounting commands will not be successful if any processes or files/directories are open

```sh
# to remount a device as read-only -ro, either specify the mount point or device both is not necessary
mount -o remount,ro /tmp # multiple options fed to -o are comma separated ','
# and back to rw
mount -o remount,rw /tmp
```
