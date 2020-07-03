# Working with disks

## Checking directory sizes

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

## Evaluating disk integrity

**note:** the systemboot process uses fsck -A upon startup to check the root filesystem

Using fsck

```sh
ls /sbin/fsck
# /sbin/btrfsck  /sbin/fsck         /sbin/fsck.ext3     /sbin/fsck.msdos
# /sbin/dosfsck  /sbin/fsck.cramfs  /sbin/fsck.ext4     /sbin/fsck.vfat
# /sbin/e2fsck   /sbin/fsck.ext2    /sbin/fsck.ext4dev  /sbin/fsck.xfs
```


