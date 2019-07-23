# Formatting and partitioning

to format an exFAT partition use mkexfatfs / mkfs.exfat

```sh
mkfs.exfat /dev/sdc1
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
