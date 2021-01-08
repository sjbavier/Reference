# Working with logs

**Syslogd** (legacy) and the newer **journald** (systemd)

Modern **systemd** systems use:

Rsyslog

- compatible with sysklogd
- persistent logs
- logs are text files
- can log remotely

Journald

- notpersistent by default
- logs are binary
- logged to RAM
- very fast

---

## Rsyslog (2004 - )

- backward compatible with sysklogd
- timestamps with millisecond granularity and time zones
- name of relays in the host fields to track the message path
- supports TCP, GSS-API and TLS
- logging directly into database engines
- supports RELP
- support for buffered operation modes
- complete input/output support for systemd journal
- rich filtering and content-based filtering
- default in Red Hat Enterprise 5+, Debian and Ubuntu

| filename | purpose                                                           |
|----------|-------------------------------------------------------------------|
| auth.log | System authentication and security events                         |
| boot.log | A record of boot-related events                                   |
| dmesg    | kernel-ring buffer events related to device drivers               |
| dpkg.log | software package-management events                                |
| kern.log | linux kernel events                                               |
| syslog   | a collection of all logs                                          |
| wtmp     | tracks user sessions (accessed through the who and last commands) |

---

## Journald

- stored in /var/run
- /var/run is in RAM

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

Displaying log for a specific service

```sh
journalctl -u ssh # all logs for service ssh
journalctl -eu ssh # display from -e end
```

Time constraints

```sh
journalctl --since 15:15:00 --until 15:52:00
```

Check the size of the journal directory

```sh
journalctl --disk-usage
```

Setting explicit limits on how journald stores log information [/etc/systemd/journal.conf] [SystemMaxUse=] [RuntimeMaxUse=]

### Persistent journald

For setting up **persistent** logs using journald ( each time a machine is restarted it will erase temp logs otherwise)  

```sh
mkdir -p /var/log/journal
systemd-tmpfiles --create --prefix /var/log/journal # using systemd-tmpfiles to direct log traffic
```

Cleaning up old journals

```sh
# clear journals older than 30 days
journalctl --vacuum-time=30d
# clear older journals when they've reached a size
journalctl --vacuume-size=1G
# clear all but 2 journal files
journalctl --vacuum-files=2
```

To use journalctl to read a different directory (perhaps one from a backup after system crash)

```sh
# read by directory
journalctl --directory=<directory>
# or by file
journalctl --file=<file-path>

# alternatively you may mount the recovered /var/log/journal directory on top of existing
# and merge them
journalctl -m
```

---

You may add messages to the log by using **logger**

```sh
logger "message"
```

---

## Syslogd (1980 - )

- specifies a message
- can log to remote servers over UDP
- does not have congestion control
- protocol became the de facto standard

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

---

## filtering logs

Using grep and before and after flags to gather information on auth failures

```sh
cat /var/log/auth.log | grep -B 1 -A 1 failure # -B 1 before 1 ln -A 1 after 1 ln
grep -nr <term> # -n returns line # and r searches recursively within directory
```

```sh
# print first column $1 from file with matching pattern, sort, report or omit repeated lines and count the occurrences
grep <pattern> <file> |awk '{print $1}'|sort|uniq -c
grep <pattern> <file> |awk -F\" '{print $6}'|sort|uniq -c|sort -nr # awk -F to define the field separator
grep <pattern> <file> |awk '{print $1}'|sort|uniq -c|sort -nr|head # sort -nr -n numeric sort, -r reverse, head is first part of file

# loop through each result and curl ipinfo for IP information
for i in `grep <pattern> <file> |awk '{print $1}'|sort|uniq -c|sort -nr|head|awk '{print $2}'`;do curl -s ipinfo.io/$i;done
```

Searching an access log for an error code 500

```sh
cat access.log | awk '$9 == 500 '|sort -nr|uniq -c
```
