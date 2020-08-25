# Working with Redundant Array of Independent Drives (RAID)

## Types of RAID

- RAID 0 - striping
- RAID 1 - mirroring
- RAID 5 - striping with parity
- RAID 6 - striping with double parity
- RAID 10 - combining mirroring and striping

There are hardware and software RAID controllers where hardware RAID controllers offer better performance especially with RAID 5 and 6.

### **RAID 0** - striping

Data is written across all drives in the array (at least 2) at the same time, ideally with one controller per disk.

Pros:

- great performance in I/O, no overhead with parity controls
- all storage capacity is used
- easy to implement

Cons:

- not fault-tolerant, if 1 drive fails, the data in the array is lost

### **RAID 1** - mirroring

Data is stored twice by writing to a data drive (or set) and a mirror drive (or set).  If a drive fails the controller uses the other copy for a continous operation. Uses at least 2 drives.

Pros:

- excellent read and write speed comparable to that of a single drive
- if a drive fails, the data will just have to be copied to the replacement drive
- simple technology

Cons:

- double the storage is necessary since data is written twice
- software RAID 1 solutions don't always allow hot swapping a failed drive, and powering down a computer is necessary; the alternative is a hardware controller that supports hot swapping

### **RAID 5** - striping with parity

The most common secure RAID level, requires at least 3 drives with a maximum of 16.  Data blocks are striped across the drives and a parity checksum of all the block data is stored.  The parity checksum data is spread across all drives and is used to recalculate the data of the other data blocks should data no longer be available.

Pros:

- read data transactions are fast while write data transactions can be slowed due to calculation of parity
- if a drive fails, the data is still accessible and automatically rebuilt when the drive is replaced

Cons:

- drives failures effect throughput
- a complex technology, if 1 drive is lost data may be restored, however if another disk goes bad during that time data may be lost

### **RAID 6** - striping with double parity

Using double parity, engineers estimate the Mean Time Before Failure (MTBF) is over 100 times that of a single parity RAID.  The two sets of parity data is stored diagonally across rows of datablocks.

Pros:

- up to 56 drives can be used (4 min) allowing 2 failures at once
- read data transactions are fast

Cons:

- write transactions are slower than RAID 5 due to extra parity (~20% lower)
- complex technology, drive failures have an effect on throughput

### **RAID 10** - RAID 1 & RAID 0 combined

This is a nested or hybrid RAID configuration that mirrors all data on secondary drives while using striping across each set of drives to speed up data transfers.

Pros:

- if one disk fails rebuild time is very fast

Cons:

- half the storage goes to mirroring

## Installation of RAID software controllers

```sh
# Debian based
apt update && apt install mdadm
# Centos
yum update && yum install mdadm
```

Creating the array

```sh
# RAID 0
mdadm --create --verbose /dev/md0 --level=stripe \
--raid-devices=2 /dev/sdb1 /dev/sdc1
# RAID 1
mdadm --create --verbose /dev/md0 --level=1 \
--raid-devices=2 /dev/sdb1 /dev/sdc1
# RAID 5
mdadm --create --verbose /dev/md0 --level=5 \
--raid-devices=3 /dev/sdb1 /dev/sdc1 /dev/sdd1 --spare-devices=1 /dev/sde1
# RAID 6
mdadm --create --verbose /dev/md0 --level=6 \
--raid-devices=4 /dev/sdb1 /dev/sdc1 /dev/sdd1 /dev/sde1 --spare-devices=1 /dev/sdf1
# RAID 10
mdadm --create --verbose /dev/md0 --level=10 \
--raid-devices=4 /dev/sdb1 /dev/sdc1 /dev/sdd1 /dev/sde1 --spare-devices=1 /dev/sdf1
# check array creation status
cat /proc/mdstat
# or more detail
mdadm --detail /dev/md0
```

To instruct the monitoring service to 'keep an eye' on the array

```sh
# add the output of this:
mdadm --detail --scan
# to /etc/mdadm/mdadm.conf (debian) /etc/mdadm.conf (centos)
# assemble the array
mdadm --assemble --scan
```

Ensuring the service starts on system boot **/etc/default/mdadm**

```sh
# in /etc/default/mdadm
AUTOSTART=true
# start and enable in systemd
systemctl start mdmonitor
systemctl enable mdmonitor
```

If a device fails, replace and add a new device to the array

```sh
mdadm /dev/md0 --add /dev/<new-device>
```
