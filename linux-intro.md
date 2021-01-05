# Directory structure

```sh
/
    /etc    # Program configuration files, host specific
    /var    # Frequently changing content such as log files
    /home   # User account files
    /sbin   # System binary files
    /bin    # User binary files
    /lib    # essential shared libraries and kernel modules
    /usr    # Third-party binaries
    /boot   # static files of the boot loader
    /dev    # device files
    /media  # mount point for removable media
    /mnt    # mount point for mounting a filesystem temporarilly
    /opt    # add-on application software packages
    /srv    # data for services provided by this system
    /tmp    # temporary files
```

Documentation:  Examples of configurations can be found in **/usr/share/doc**

```sh
man <package>
<command> --help
```

System Logs

```sh
journalctl
journalctl | grep filename.php | grep -v error
```

Change shell

```sh
chsh
```

Rsync is a great utility for copying and syncing directories

```sh
rsync -aPv /home/downloads <user>@<host>:<directory>
rsync -aPv -e "ssh -p 2222" <input> <output> # rsync over different port
```

Get information on memory (RAM and Swap)

```sh
free -h # human readable
```

Get stats on Swap

```sh
vmstat 30 4 # 4 readings in 30 second intervals
```

Get stats on disk usage

```sh
df -h # human readable
df -i # inode data
du -sh <file> # human readable, specific file
```

Use find to see the directories containing the largest number of files

```sh
#  . search within, -xdev remain within single file system, -type f object of type file, cut -d remove text identified by delimiter "/", -f 2 select second field found, sort lines of output, uniq -c count the lines, sort -n sort by numerical order
find . -xdev -type f | cut -d "/" -f 2 | sort | uniq -c | sort -n
```