# Working with packages

Add a repository

```sh
add-apt-repository <repo> # ubuntu
```

Remove a repository

```sh
add-apt-repository --remove <repo> # ubuntu
```

Install a package

```sh
apt install <package>
```

Remove a package

```sh
apt remove <package>
```

Fix a broken installation

```sh
apt --fix-broken install
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