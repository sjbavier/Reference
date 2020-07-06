# Reference for managing users and related groups

## Users

Adding users

```sh
useradd -m <user> # -m makes user a home directory
```

Deleting users

```sh
userdel <user>
userdel -f <user> # force
userdel -r <user> # delete the <user> directory and all of the contents
```

Create or password for user [sudo]

```sh
passwd <user>
```

Get status of user

```sh
# this includes password locked info
passwd -S <user>
```

Unlock user password

```sh
passwd -u <user>
```

Append a user group

```sh
usermod -aG <group> <user>
# Add user to sudoers
usermod -aG wheel <user> # users in group wheel can run sudo commands
# or on Centos edit /etc/sudoers using visudo
visudo
```

Show password expiration details

```sh
chage -l <user>
```

Lock a user

```sh
chage -E 0 <user>
```

Unlock a user

```sh
chage  -E -1 <user>
```

## Groups

What groups is a user in

```sh
groups <user>
```

Add a group

```sh
groupadd <group>
```

## Etc User and Group locations

The /etc/group file contains basic information about existing system and user groups

```sh
sudo cat /etc/group
```

To see encrypted passwords of users

```sh
sudo cat /etc/shadow
```

To see encrypted group passwords

```sh
sudo cat /etc/gshadow
```
