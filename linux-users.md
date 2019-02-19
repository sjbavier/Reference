# Reference for managing users and related groups

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

Create or password for user [sudo]

```sh
passwd <user>
```