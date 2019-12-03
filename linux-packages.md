# Working with packages

## apt (Debian, Ubuntu)

### Configuration

The repository sources are stored in **/etc/apt/souces.list**

APT configuration options are located in **/etc/apt/apt.conf**

```sh
apt-config dump
```

### Repositories

Update repository information

```sh
apt update
```

Add a repository

```sh
add-apt-repository <repo> # ubuntu
```

Remove a repository

```sh
add-apt-repository --remove <repo> # ubuntu
```

### Adding packages

Install a package

```sh
apt install <package>
```

Fix a broken installation

```sh
apt --fix-broken install
```

Get information on package ( not necessarily installed )

```sh
apt show <package>
```

### Removing packages

Remove a package

```sh
apt remove <package>
```

Remove package and dependencies that are unused prerequisites of the package

```sh
apt autoremove <package>
```

To purge configuration information

```sh
apt purge <package>
```

### Upgrading

After running apt update use upgrade to update all packages on your system

```sh
apt upgrade
```

To upgrade distros

```sh
apt distro-upgrade
```

### Reconfiguring packages

View current package configuration with debconf-show

```sh
debconf-show <package>
```

Use dpkg to reconfigure a package

```sh
dpkg-reconfigure <package>
```

Check the status of a package with dpkg

```sh
dpkg -s <package>
```

## yum (centos)

```sh
yum install epel-release # repo
yum install <package>
yum provides */<command>
yum whatprovides */<command>
```



Get status on a package

```sh
dpkg -s <package>
```

Getting some info on a package

```sh
info <package>
man <package>
```

Debian package manager ( -i flag for install )

```sh
dpkg -i <file.deb>
```

To get the

Use shasum to calculate the checksum of a file to make sure it hasn't been tampered with

```sh
shasum <name-of-file>
```