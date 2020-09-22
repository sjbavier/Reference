# Working with LXC

## Configuration

For Red Hat or CentOS you'll need to install the EPEL repositories, in Debian/Ubuntu install lxc:

```sh
apt install lxc
```

Make sure that the current user has both a sub-uid and a sub-gid entry in /etc/[subuid](../linux-subid-subgid.md) and /etc/[subgid](../linux-subid-subgid.md)

```sh
cat /etc/subuid
# output
# <user>:100000:65536
cat /etc/subgid
# expected output
# <user>:100000:65536
# format
# <user>:start:count
```

Create the ~/.config/lxc directory if it doesn't exist and copy the default /etc/lxc/default.conf

Add the following lines to correspond with the sub-uid and sub-gid:

```sh
lxc.id_map = u 0 100000 65536
lxc.id_map = g 0 100000 65536
```

Append the following to /etc/lxc/lxc-usernet, the first column is your username

```conf
<user> veth lxcbr0 10
```

Either reboot or log out the user then when logged in verify the **veth** driver is loaded

```sh
lsmod | grep veth
```

if no results type:

```sh
sudo modprobe veth
```

## Using LXC

Creating a template using the [Ubuntu] template

Containers are stored in ~/.local/share/lxc and /var/lib/lxc for root.

```sh
lxc-create -n <container-name> -t ubuntu
```

The template reside in the [/usr/share/lxc/templates] directory ( may have to install apt install lxc-templates )

```sh
ls /usr/share/lxc/templates/
lxc-alpine
lxc-centos
lxc-fedora
lxc-altlinux
lxc-cirros
lxc-gentoo
lxc-archlinux
lxc-debian
lxc-openmandriva
lxc-busybox
lxc-download
lxc-opensuse
lxc-oracle
lxc-plamo
lxc-slackware
lxc-sparclinux
lxc-sshd
lxc-ubuntu
lxc-ubuntu-cloud
```

When creating an LXC container the temporary root password resides in [/var/lib/lxc/<name-of-lxc-container>/temp_root_pass]
If you are using the Ubuntu template then the username:password is [ubuntu:ubuntu].

```sh
lxc-create -n centos_lxc -t centos
# /var/lib/lxc/centos_lxc/tmp_root_pass
```

Change the password using [passwd]

```sh
passwd
```

To get status on the container

```sh
lxc-ls --fancy
```

Start the container in detached mode [-d] specifying the name of the container [-n]

```sh
lxc-start -d -n <container-name>
```

Start container in the foreground to debug [-F]

```sh
lxc-start -n <container-name> -F
```

Stop an lxc container

```sh
lxc-stop -n <container-name>
```

You may log into a running container as root using [ssh] or [lxc-attach]

```sh
lxc-attach -n <container-name>
```

To exit while within the container and leave it running

```sh
exit
```

To shutdown the container use the [-h] halt

```sh
shutdown -h now
```

To restart the container use the [-r] reboot

```sh
shutdown -r now
```

Lost control of your lxc container ?

```sh
chroot /var/lib/lxc/<container-name>/rootfs/
```