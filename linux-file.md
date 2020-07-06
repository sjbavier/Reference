# Working with files

## File Types

```sh
# example
ls -al
# -l long format -a all files including hidden
drwxr-xr-x     5 <user-owner>  <group-owner>        160 Nov  7  2019 <directory>
# first character 'd' for directory other types are
-   regular file
d   directory
b   block device
c   character device
l   symbolic link
p   named pipe
s   socket
```

## Basic file commands

Display detailed information about a file

```sh
stat <file>
```

Matching a partial filename [matches file1, file2, ... file9 but not file10]

```sh
mv file? /some/other/directory
```

Matching a partial with wildcard * [all files that start with `file`]

```sh
cp file* /some/other/directory
```

Test if a file exists

```sh
test -f <file>
```

Compare two files

```sh
cmp -s <file1> <file2>
```

Unix file program, insider file information

```sh
file /sbin/int

    /sbin/init: symbolic link to /lib/systemd/systemd
```

Find top file sizes only

```sh
find -type f -exec du -Sh {} + | sort -rh | head -n 5

   # du command: Estimate file space usage.
   # -h : Print sizes in human readable format (e.g., 10MB).
   # -S : Do not include size of subdirectories.
   # -s : Display only a total for each argument.
   # sort command : sort lines of text files.
   # -r : Reverse the result of comparisons.
   # -h : Compare human readable numbers (e.g., 2K, 1G).
   # head : Output the first part of files.

```

## Extended Attribute Types

- security
- system
- user

### Security attributes

Get the SELinux security attributes

```sh
ls -Z
# or recursive
ls -RZ
```

#### Access control lists

Set an ACL

```sh
setfacl -m <user>:<group>:rwx <file>
```

Get an ACL

```sh
getfacl -t <file>
```

### User attributes

Change user attributes

```sh
chattr +i <file>
```

View extended user attributes

```sh
lsattr <file>
```

