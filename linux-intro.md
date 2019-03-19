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

System Logs

```sh
journalctl
journalctl | grep filename.php | grep -v error
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

Restart a service

```sh
systemctl restart <service>
```

Scan for active services

```sh
systemctl list-unit-files --type=service --state=enabled
```

Change shell

```sh
chsh
```

Rsync is a great utility for copying and syncing directories

```sh
rsync -aPv /home/downloads <user>@<host>:<directory>
```
