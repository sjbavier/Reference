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