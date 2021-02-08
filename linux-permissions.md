# Standard Linux Permissions

- Users can belong to multiple groups
- Files belong to one user owner
- Files belong to one group owner
- Permissions can be set for the user, group or other
- Users can read, write or execute files
- Users can list, create new files and traverse directories
- Permissions support privilege escalation
- Permissions support group owner inheritance
- Supports default file permissions

| permission | file                                | directory                                                  |
|------------|-------------------------------------|------------------------------------------------------------|
| read       | can open and read content of a file | can list files present in a directory but cannot read file |
| write      | user can modify contents of a file  | user can add or delete files in directory                  |
| execute    | user can run executable files       | user can use 'cd' command to traverse the directory        |

## Basic Permissions Commands

Changing file permissions [owner-group-everybody] r=4, w=2, x=1

```sh
chmod 644 <directory>
```

Changing file ownership

```sh
# -R for recursive
chown -R <user>:<group> <fileORdirectory>
```

## Set Default Permissions

using umask

```sh
# view default
umask
# in symbolic notation
umask -S
# temp change umask
umask 022 # only will work for current session
# for a more permanent change, consider adding to .bashrc
```

For system wide umask changes modify /etc/profile.d/umask.sh

```sh
# condition for root and regular users
if [ "$UID" -ge 1000 ] ;then # if user id is greater than or equal to
   umask 022
fi
```

To calculate the umask subtract the umask from **Maximum Initial Permissions**

For directories

- rwxrwxrwx 777

For files
**note: no execute permissions**

- rw-rw-rw 666

Example Directory evaluation

```sh
umask
## sample output
0002
#  777 = maximum initial directory permissions
# -002 = umask value
# =   775 = default directory permissions
#  666 = maximum initial file permissions
# -002
# =   664 = default file permissions
```

## Using ACLs

Access Control Lists are a kernel feature that allow more fine-grained access rights to files or directories than the ugo/rwx permissions.

To check if your filesystem supports ACLs (XFS does by default)

```sh
tune2fs -l /dev/<block-device> | grep "Default mount options:"
# Default mount options: user_xattr acl 
```

There are two types of ACLs: access ACLs which are applied to files or directories and default (optional) ACLs which can only be applied to a directory.

To see current ACL settings in a directory

```sh
getfacl <directory-or-file>
```

To add a permission to a file for a specific user:

```sh
setfacl -m u:<user>:rw <file>
# -m for modify and rw for read/write permissions
```

To set a default ACL for a directory in this case 'read' for 'others'

```sh
setfacl -m d:o:r <directory>
# -m for modify, d: directory, o: other, r read
```

To remove a specific ACL you can simply replace the -m for an -x

```sh
setfacl -x d:o <directory>
# remove directory access to others
```

To remove all ACLs at once

```sh
setfacl -b <directory>
```

## SUID, SGID and Sticky

- 4   -   SUID
- 2   -   SGID
- 1   -   Sticky

| id     | file                                                       | directory                                                       |
|--------|------------------------------------------------------------|-----------------------------------------------------------------|
| SUID   | run program as the owner of the file                       | -                                                               |
| SGID   | assign authority to run program as group owner of the file | all files created beneath the directory inherit group ownership |
| Sticky | -                                                          | only file owner can delete the file                             |

### SUID

**note:** you are never recommended to use SUID in routine administration

Check if SUID is set

```sh
# example
-rwsr-xr-x. 1  root  root  32072 Aug   2  2017  /usr/bin/su
#               ^----------------- user executes as root
#  s - means that the owner Execute SUID bit is set
-rwSr-xr-x. 1  root  root  32072 Aug   2  2017  /usr/bin/su
#  S - means that the owner Execute SUID bit is not set
```

When the SUID bit is set that means a regular user executing the su command runs the command as the User Owner 'root'

```sh
chmod 4755 <file>
#     ^------- 4 SUID
# or
chmod u+s <file>
```

Find all SUID set files

```sh
find / -perm -4000
```

### SGID

Files created under a directory with a SGID bit will inherit group owner

Check if SGID is set

```sh
# example
-rwxr-sr-x. 1  root  screen  43243 Aug   2  2017  /usr/bin/screen
#                      ^----------- user executes as group owner screen
#  s - means that the owner Execute SUID bit is set
```

**note:** when an "l" appears in the groups execute field it indicates that the setgid bit is on and the execute permission is denied

When SGID bit is set the user executes the command as the group owner

```sh
chmod 2755 <file>
#     ^------- 2 SGID
# or
chmod g+s <file>
```

Find all SGID set files

```sh
find / -perm -2000
```

### Sticky bit

Sticky bit is used for keeping users from removing other peoples files/directories for multiple user directories.  Even if the directory has a permission 777 and the sticky bit is set, other users cannot delete files.

Check if Sticky bit is set

```sh
# example
-rwxr-xr-t. 1  user  group  43243 Aug   2  2017  /home/example
#        ^----------- t - users can execute
#  t - sticky bit is set (users can execute)
#  T - sticky bit is unset (users cannot execute)
```

```sh
chmod 1755 <directory>
#     ^---------1 Sticky bit
# or
chmod o+t <directory>
```
