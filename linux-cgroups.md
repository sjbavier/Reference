# Working with Cgroups (v1)

## Overview

Cgroups are a facility build into the kernel that allow administrative control of setting resource limits.  Some of the controllers are:

- number of **CPU** shares per process (**cpu**)
- limits on RAM per process (**memory**)
- block device **I/O** per process (**blkio**)
- which **network** packets are identified as the same type so that other applications can enforce network traffic rules

### Resource limiting

Focused on ensuring programs stay within acceptable boundaries for CPU, RAM, block device I/O and device groups

**note:** device groups include controlling permissions for read, write and mknod operations.  **mknod** was initially designed to populate all things that show up in the /dev/ directory.  Modern distros use **udev** to autopopulate this virtual filesystem with kernel detected devices.  **mknod** also allows multiple programs to communicate VIA 'named pipe' allowing information to pass from one program to another.

### Prioritization

Utilizing Cgroup to allow process X to have more time on the system than process Y.

### Accounting

By default this is usually turned off as it consumes additional resources.  Accounting can help with insight into resource utilization for a particular tree and determining which resources are being consumed.

### Process control

**freezer** is a utility that can 'freeze' a particular process and move it.  **tuned* lets you performance tune.

