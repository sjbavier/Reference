# Directory structure

```sh
/
    /etc    # Program configuration files
    /var    # Frequently changing content such as log files
    /home   # User account files
    /sbin   # System binary files
    /bin    # User binary files
    /lib    # Shard libraries
    /usr    # Third-party binaries
```

The /etc/group file contains basic information about existing system and user groups

```sh
sudo cat /etc/group
```

To see encrypted passwords of users

```sh
sudo cat /etc/shadow
```

To see encrypted group passwords

```sh
sudo cat /etc/gshadow
```

    Display detailed information about a file

    ```sh
    stat <file>
    ```

    Matching a partial filename [matches file1, file2, ... file9 but not file10]

    ```sh
    mv file? /some/other/directory
    ```

    Matching a partial with wildcard * [all files that start with `file`]

    ```sh
    cp file* /some/other/directory
    ```

    Getting some info on a package

    ```sh
    info <package>
    man <package>
    ```

    System Logs

    ```sh
    journalctl
    journalctl | grep filename.php | grep -v error
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


Get the status of a service

```sh
systemctl status <service>
```

Stop a service

```sh
systemctl stop <service>
```

Force a service to load on system startup

```sh
systemctl enable <service>
```

Remove a service from system startup

```sh
systemctl disable <service>
```

Display ip information

```sh
ip addr
```

Get status on a package

```sh
dpkg -s <package>
```

Listing block devices

```sh
lsblk
```

Rsync is a great utility for copying and syncing directories

```sh
rsync -av /home/downloads <user>@<host>:<directory>
```

Test if a file exists

```sh
test -f <file>
```

Compare two files

```sh
cmp -s <file1> <file2>
```
