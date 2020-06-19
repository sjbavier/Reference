# Take caution with dd operations (disk destroyer)

To make an exact image of one mount to another

```sh
dd if=/dev/sda of=/dev/sdb # if = source file of = destination file
```

To create an image

```sh
dd if=/dev/sda of=/home/garbo.img bs=4096 # bs bytes to copy at a single time
dd if=/dev/sda of=/dev/sdb status=progress bs=64K conv=noerror,sync
# byte size 64Kb no error for error safety with status
```

Restoring from image is simply the reverse

```sh
dd if=/home/garbo.img of=/dev/sda
```

Wiping disks with dd

```sh
dd if=/dev/zero of=/dev/sda1 # fills entire partition with 0s

dd if=/dev/urandom of=/dev/sda1 # fills partition with random characters
```