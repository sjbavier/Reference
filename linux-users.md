# Reference for managing users and related groups

What groups is a user in

```sh
groups <user>
```

Add a group

```sh
groupadd <group>
```

Changing file permissions [owner-group-everybody] r=4, w=2, x=1

```sh
chmod 644 <directory>
```

Changing file ownership

```sh
chown -R <user>:<group> <fileORdirectory>
```

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

Append a user group

```sh
usermod -aG <group> <user>

```

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
