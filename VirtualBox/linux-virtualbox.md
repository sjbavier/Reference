# Commands for using Virtualbox on Linux distros

Using vboxmanage to list vms

```sh
vboxmanage list vms
```

Cloning a vm

```sh
vboxmanage clonevm --register <vm-name> --name <new-vm-name>
```

Convert vm to standardized file by exporting

```sh
vboxmanage export <name-of-export> -o <name-of-file.ova>
```

Import from a file

```sh
vboxmanage import <file.ova>
```

## setting up with virtual NAT networks

Create the networks for a DMZ configuration

```sh
vboxmanage natnetwork add -netname dmz \
--network "10.0.1.0/24" --enable --dhcp on

vboxmanage natnetwork add -- netname loc \
--network "10.0.1.0/24" --enable --dhcp on

vboxmanage natnetwork start --netname dmz
vboxmanage natnetwork start --netname loc
```

## Cloning and modifying disks

Clone vmdk disk and convert to vdi

```sh
vboxmanage clonemedium <source-vmdk> <cloned-vdi> --format vdi
```

Resize the disk (does not support vmdk)

```sh
vboxmanage modifymedium <source-vdi> --resize <megabytes>
```
