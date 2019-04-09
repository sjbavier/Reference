# Working with NFS

## Table of contents

1. [Installing](#installing)
   - [Server Installation](#server_installation)
   - [Client Installation](#client_installation)
2. [Configuration](#configuration)
   - [Server Configuration](#server_configuration)
   - [Client Configuration](#client_configuration)

## Installing

### Server Installation

```sh
yum install nfs-utils # Centos
apt install nfs-kernel-server # Ubuntu
```

### Client Installation

```sh
yum install nfs-utils # Centos
apt install nfs-common # Ubuntu
```

## Configuration

### Server Configuration

Location of the configuration file [/etc/exports]

Do not put a space in between the ip and the read write directives, for example /home 192.168.1.11 (rw,sync) allows anyone to access!

By default nfs communication is on port 2049

```conf
/home 192.168.1.11(rw,sync) # exposes the home directory to client 192.168.1.11 with read/write privileges, maintains a stable environment by writing changes to disk before replying to remote requests
/example2 192.168.1.11(ro,sync) # ro = read only
/example3 192.168.1.11(rw,sync,root_squash) # root_squash does not allow remote client to perform root actions
/example4 192.168.1.11(rw,sync,no_root_squash) # no_root_squash allows remote root access
/home2 192.168.1.0/255.255.255.0(rw,sync) # allow anyone on the 192.168.1.0 network access to the home2 directory
```

```sh
exportfs -ra # applies changes made to the settings, r = synchronize filesystem, a = applies action to all directories
exportfs # View any NFS file system currently exposed to clients
exportfs -a # check the version

firewall-cmd --add-service=nfs # add firewall rule for nfs service
firewall-cmd --reload # reload firewall settings
systemctl start nfs-server # start nfs-server
```

### Client Configuration

Mount the remote directory to a local directory

```sh
mkdir -p /nfs/home
mount 192.168.1.23:/home /nfs/home # the ip address and directory depends on the nfs server's configuration, make sure to match appropriately
```

Mounting NFS share at boot time using [/etc/fstab]

