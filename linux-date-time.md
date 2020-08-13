# Working with date/time

## Setting time options

Adjusting time and date with **timedatectl**

Output current time and date

```sh
timedatectl
```

List timezones

```sh
timedatectl list-timezones
# pipe to grep
timedatectl list-timezones | grep America
```

Set timezone

```sh
timedatectl set-timezone America/St_Johns
```

Manually set time

```sh
# sometimes you may have to run the command twice
timedatectl set-time 23:26:00
# to set date
timedatectl set-time 2020-08-22
# set time and date together
timedatectl set-time '2020-08-22 23:26:00'
```

---

## Setting locales for region and language

Get locale information

```sh
localectl
# list locales
localectl list-locales
# use with grep for ones beginning with 'en'
localectl list-locales | grep ^en
```

Setting locales

```sh
localectl set-locale LANG=en_US.utf8
```

List keymaps

```sh
localectl list-keymaps
# pipe with grep
localectl list-keymaps | grep ^us
```

Set keymaps

```sh
localectl set-keymap us
```

---

## Using date

Show current date and time

```sh
date
# show UTC
date --utc
# change date format: short-month, day, year
date +"%h %d %Y"
# seconds since January 1 1970
date +"%s"
```

Convert date in seconds to full date/time display

```sh
date +"%s"
# 1595601516
date --date='@1595601516'
# Fri Jul 24 10:38:36 EDT 2020
```

Calculate date

```sh
# calculate date in 10 days
date --date '+10 days'
# abstract calculations
date --date 'next friday'
```

---

## using calendar

Show calendar

```sh
cal
#       July 2020
# Su Mo Tu We Th Fr Sa
#           1  2  3  4
#  5  6  7  8  9 10 11
# 12 13 14 15 16 17 18
# 19 20 21 22 23 24 25
# 26 27 28 29 30 31

# show 3 months
cal -3
#       June 2020             July 2020            August 2020
# Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
#     1  2  3  4  5  6            1  2  3  4                     1
#  7  8  9 10 11 12 13   5  6  7  8  9 10 11   2  3  4  5  6  7  8
# 14 15 16 17 18 19 20  12 13 14 15 16 17 18   9 10 11 12 13 14 15
# 21 22 23 24 25 26 27  19 20 21 22 23 24 25  16 17 18 19 20 21 22
# 28 29 30              26 27 28 29 30 31     23 24 25 26 27 28 29
#                                             30 31

# show calendar from a different year
# ie 1752, note the calendar act of 1750 in September
cal 1752
```

---

## Setting up NTP

Configure NTP

```sh
# this will enable NTP
timedatectl set-ntp true
# now restart the client
systemctl restart systemd-timedated
# you may have to install the NTP client
# on Centos it is chrony
yum install chrony
```

### chronyd

- accepts client queries by default
- can be configured to allow client to control it remotely
- allows queries by Unix domain sockets by default
- optionally allows queries by IPv4 and IPv6

chrony package includes:

- chronyd server
- chronyc client

Make sure chronyd is installed, started and enabled by default, firewalls may have to be modified

```sh
yum install chrony
systemctl start chronyd
systemctl enable chronyd
```

configurations are found in **/etc/chrony.conf**

### ntpd

Make sure ntp is installed, started and enabled by default, firewalls may have to be modified

```sh
yum install ntp
systemctl start ntpd.service
systemctl enable ntpd.service
```

Query ntp server

```sh
ntpq -p
```

configurations are found in **/etc/ntp.conf**

