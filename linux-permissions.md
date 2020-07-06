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

## SUID, SGID and Sticky

- 4   -   SUID
- 2   -   SGID
- 1   -   Sticky

### SUID

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

Sticky bit is used for keeping users from removing other peoples files/directories for multiple user directories

Check if Sticky bit is set

```sh
# example
-rwxr-xr-t. 1  user  group  43243 Aug   2  2017  /home/example
#                      ^----------- user executes as group owner screen
#  t - sticky bit is set
#  T - sticky bit is unset
```
