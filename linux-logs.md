# Working with logs

Syslogd and the newer journald

## Journald

Basic log output

```sh
journalctl # displays logs oldest to newest
journalctl -n 20 # displays the last 20 entries
```

Displaying based on priority

```sh
journalctl -p debug
journalctl -p info # informational
journalctl -p notice # normal conditions
journalctl -p warning
journalctl -p err
journalctl -p crit
journalctl -p alert # immediate action requiers
journalctl -p emerg # displays entries categorized as emergency
```

Displaying entries in real time

```sh
journalctl -f # -f flag is for follow
```

Time constraints

```sh
journalctl --since 15:15:00 --until 15:52:00
```

| filename | purpose                                                           |
|----------|-------------------------------------------------------------------|
| auth.log | System authentication and security events                         |
| boot.log | A record of boot-related events                                   |
| dmesg    | kernel-ring buffer events related to device drivers               |
| dpkg.log | software package-management events                                |
| kern.log | linux kernel events                                               |
| syslog   | a collection of all logs                                          |
| wtmp     | tracks user sessions (accessed through the who and last commands) |

Setting explicit limits on how journald stores log information [/etc/systemd/journal.conf] [SystemMaxUse=] [RuntimeMaxUse=]

For setting up persistent logs using journald ( each time a machine is restarted it will erase temp logs otherwise)  

```sh
mkdir -p /var/log/journal
systemd-tmpfiles --create --prefix /var/log/journal # using systemd-tmpfiles to direct log traffic
```

## Syslogd

By default syslogd handles log rotation. The log rotation configs can be accessed in [/etc/logrotate.conf]

```conf
# rotate log files weekly
weekly
# keep 4 weeks worth of backlogs
rotate 4
# create new (empty) log files after rotating old ones
create
# packages drop log rotation information into this directory
include /etc/logrotate.d
```

To list the individual services or applications connected to log daemon

```sh
ls /etc/logrotate.d/
# sample output
apache2 apt dpkg mysql-server rsyslog samba unattended-upgrade
```

Listing the config for apt log for example

```conf
/var/log/apt/term.log {
   rotate 12 # files will be rotated 12 times before being deleted
   monthly # rotations take place once a month
   compress # rotated files with be compressed
   missingok
   notifempty
}
/var/log/apt/history.log {
   rotate 12
   monthly
   compress
   missingok
   notifempty
}
```

## Sifting through logs

Using grep and before and after flags to gather information on auth failures

```sh
cat /var/log/auth.log | grep -B 1 -A 1 failure # -B 1 before 1 ln -A 1 after 1 ln
grep -nr <term> # -n returns line # and r searches recursively within directory
```

