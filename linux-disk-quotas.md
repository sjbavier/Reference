# Managing Disk Quotas

- Quotas can control disk usage by either **user** or **group**

- XFS also supports quotas by **project**

## Prerequisites

**note:** quota may have to be installed on your distro.

First enable user or group quotas on a filesystem in /etc/fstab

Example fstab:

```conf
UUID=f6d1eba2-9aed-40ea-99ac-75f4be05c05a /home/projects ext4
defaults,grpquota 0 0
UUID=e1929239-5087-44b1-9396-53e09db6eb9e /home/backups ext4
defaults,usrquota 0 0
```

## Enabling quotas

Check status for quotas

```sh
quotacheck -avugc
```

Enable quota for user

```sh
quotaon -vu /home/backups
```

Enable quota for group

```sh
quotaon -vg /home/projects
```

## Settings quotas

Editing quota for user:

- this example sets the hard limit to 1000 (1024 bytes/block * 1000 = 1024000 = 1MB) inodes being the number of files a user can create hard limit 25

```sh
edquota -u <user>
# Example
# Filesystem      blocks      soft     hard     inodes      soft     hard
# /dev/<device>   0           900      1000     1           20       25
```

Editing quota for group:

```sh
edquota -g <group>
```

The grace period where a warning for hitting soft limits is displayed can be changed (system-wide)

```sh
edquota -t
```

## Reporting quotas

To report quotas for a user

```sh
quota -u <user>
```

To report quota for a group

```sh
quota -g <group>
```

For a list

```sh
repquota -v <path-to-filesystem>
```