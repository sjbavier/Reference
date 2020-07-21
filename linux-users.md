# Reference for managing users and related groups

## Users

Adding users

```sh
useradd -m <user> # -m makes user a home directory
```

---

### userdel

Deleting users

```sh
userdel <user>
userdel -f <user> # force
userdel -r <user> # delete the <user> directory and all of the contents
```

---

### passwd

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

---

### usermod

```sh
usermod -d, --home <directory> # specify user's home directory
usermod -g <group-id> / -u <user-id> # changes primary group or user ID
usermod -G <groups> # specify supplemental groups
usermod -a # combined with -G appends users to group list
usermod -l <login-name> # changes user's login name
usermod -L # lock account
usermod -U # unlock account
usermod -m # moves home directory
usermod -s <shell> # specifies shell
```

Lock a user account

```sh
# lock and account, just locked the password, not ssh keys
usermod -L <user> # look in /etc/shadow
usermod -s /sbin/nologin <user> # to further lock the login shell, verify in /etc/passwd
# unlock user
usermod -U <user>
usermod -s /bin/bash <user> # change shell back to bash
```

Append a user group

```sh
# append a group
usermod -aG <group> <user>
# Add user to sudoers
usermod -aG wheel <user> # users in group wheel can run sudo commands
# or on Centos edit /etc/sudoers using visudo
visudo
```

---

### chage

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

Force user to change password upon next login

```sh
chage -d 0 <user>
```

Set unlimited password expiration, with password changes anytime

```sh
# -I -1 inactive to never, -m 0 password change anytime, -M max days 99999, -E -1 expires never
chage -I -1 -m 0 -M 99999 -E -1 <user>
```

---

## Groups

What groups is a user in

```sh
groups <user>
```

Add a group

```sh
groupadd <group>
# add group by id
groupadd -g <id> <group>
# verify in /etc/group
```

Change group id with **groupmod**

```sh
groupmod -g <group-id> <group>
```

Place users in a group with **gpasswd**

```sh
gpasswd -a <user> <group>
```

Delete a group with **groupdel**

```sh
groupdel <group>
# verify in /etc/group
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

View how starting UIDs are incremented

```sh
cat /etc/login.defs
# > 1000 for Centos
```

To view security for wheel groups

```sh
cat /cet/security/access.conf # to view 'wheel' group privileges
# check the sudo configuration
visudo
```

To view password policies

- difok
- minlen
- dcredit
- ucredit
- lcredit
- ocredit
- minclass
- maxrepeat
- maxclassrepeat
- gecoscheck

```sh
cat /etc/security/pwquality.conf
```