# Working with packages

## apt (Debian, Ubuntu)

The underlying technology of apt is dpkg

### Configuration

The repository sources are stored in **/etc/apt/souces.list** and **/etc/apt/sources.list.d/**

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
add-apt-repository '<repo>'
```

Remove a repository

```sh
add-apt-repository --remove '<repo>'
```

### Querying packages

Search for package by name

```sh
apt search <package>
```

Show package details

```sh
apt show <package>
```

List packages by criteria

```sh
# ie: upgradable
apt list --upgradable
# installed
apt list --installed
```

Get detailed information on a package

```sh
apt info <package>
```

### Adding packages

Install a package

```sh
apt install <package>
```

Download the package to current directory but do not install

```sh
apt-get download <package>
```

---

Get information on a .deb package

```sh
dpkg --info <package.deb>
```

Check which software will be installed and where on a .deb

```sh
dpkg -c <package.deb>
```

Install .deb with dpkg

```sh
dpkg -i <package.deb>
```

On an installed package we may query where the files reside

```sh
dpkg -L <package>
```

Check what package installed a particular directory

```sh
dpkg -S <path/to/directory>
```

Get status on a package

```sh
dpkg -s <package>
```

---

### Troubleshooting

Fix a broken installation

```sh
apt --fix-broken install
```

Fix a MergeList problem

```sh
# remove the lists
rm -r /var/lib/apt/lists/*
# generate new
apt-get clean && apt-get update
```

---

### Removing packages

Remove a package

```sh
apt remove <package>
```

Remove package and dependencies that are unused prerequisites of the package

```sh
# to remove all unused
apt autoremove
# or specify
apt autoremove <package>
```

To purge configuration information

```sh
apt purge <package>
```

---

### Upgrading

After running apt update use upgrade to update all packages on your system

```sh
# update indexes
apt update
# upgrade all packages
apt upgrade
```

Upgrade all packages and possibly remove packages due to conflicts

```sh
apt full-upgrade
```

---

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

---

### Distro upgrades

Run dist-upgrade to utilize apt's "smart" conflict resolution
this will focus on the most important packages and may remove some as well

```sh
apt dist-upgrade
```

Check for a new release

```sh
do-release-upgrade -c
```

Upgrade to the development release

```sh
do-release-upgrade -d
```

Set the mode to either desktop or server

```sh
# desktop
do-release-upgrade -m desktop
# server
do-release-upgrade -m server
```

Allow third party mirrors

```sh
do-release-upgrade --allow-third-party
```

Put it all together

```sh
do-release-upgrade -d -m desktop
```

---

## yum (centos/redhat)

The underlying technology behind yum is rpm

* yum uses RPM to install packages
* yum resolves dependencies automatically
* yum has concept of software package groups

rpm installed packages cache a package database

### Using rpm

To query all packages installed

```sh
# -q query -a all
rpm -qa
# query a package -i information
rpm -qi <package>
```

Query all packages in a package group

```sh
# ie shells
rpm -qa Group="System Environment/Shells"
```

Query packages based on installed date

```sh
rpm -qa --last
```

Query directories of a package

```sh
# -l for list
rpm -ql <package>
```

Query package for documentation location

```sh
# -d documentation
rpm -qd <package>
```

Query package for configuration files

```sh
# -c configuration
rpm -qc <package>
```

Query file for package name

```sh
rpm -qf <directory/of/file>
```

Which package provides a particular program

```sh
rpm -q --provides <program>
```

Which package requires another package

```sh
rpm -q --requires <package>
```

---

### Using yum

### Installing

Install a package

```sh
yum install <package>
# auto yes
yum install -y <package>
```

Reinstall a package

```sh
yum reinstall <package>
```

### updating/upgrading

List packages with updates

```sh
yum list updates
```

Update packages

```sh
yum upgrade
# upgrade single package
yum upgrade <package>
```

### Removal

Remove a package
**note: careful using -y (not recommended)**

```sh
# leaves behind dependencies and configurations
yum remove <package>
# remove package and dependencies
yum autoremove <package>
```

### yum groups

All groups have a group name and a group ID

Get a list of names and ids

```sh
yum group list ids
```

Get information on a group

```sh
yum group info <group-id>
```

Installing package groups

```sh
# the commands are synonymous
yum group install "<group name>" # quotes needed for group names
yum group install <group-id>
yum install @"<group name>" # quotes for spaces etc.
yum install @<group-id>
```

Optional packages are not installed by default to override this

```sh
yum group install <group-id> --setopt=group_package_types=mandatory,default,optional
```

Remove a group **some packages will not be removed**

```sh
yum group remove <group-id>
yum group remove "<group name>"
```

To remove all packages in a group

```sh
yum autoremove @<group-id>
```

Update all packages in a group

```sh
yum group update <group-id>
```

### Misc

```sh
yum install epel-release # repo
yum install <package>
yum provides */<command>
yum whatprovides */<command>
```

List all the installed packages

```sh
yum list installed
yum list installed | grep <package>
```

## Additional commands

Getting some info on a package

```sh
info <package>
man <package>
```

Use shasum to calculate the checksum of a file to make sure it hasn't been tampered with

```sh
shasum <name-of-file>
```
