# Working with LXC

Creating a template using the [Ubuntu] template

```sh
lxc-create -n <container-name> -t ubuntu
```

The template reside in the [/usr/share/lxc/templates] directory

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