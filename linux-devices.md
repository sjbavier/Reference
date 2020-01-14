# Working with devices

udev is responsible for dynamic device management needed for hot plugging devices
Information about configured and active devices can be found in /dev virtual filesystem.
When a device is added the kernel sends an even to systemd-udevd.service daemon.
udev rules are defined in /usr/lib/udev/rules.d and local rules in /etc/udev/rules.d
Configure udev using the /etc/udev/udev.conf file

listing devices on /dev

**b**
Represents a block device such as a disk drive

**c**
Represents a character device such as a terminal or printer, or a special device such as null

**d**
Represents a directory

**l**
Represents a symbolic link to another directory of file, either in /dev, /proc, or /run

Use list hardware

```sh
lshw
lshw -short
```

Hardware information

```sh
hwinfo
hwinfo --short
```

List PCI (most data comes from /usr/share/hwdata/pci.ids)

```sh
lspci
lspci -v
lspci -t # tree view
lspci | column -t
```

List scsi/sata devices like hard drives and optical drives

```sh
lsscsi
```

List usb buses (usb 1.1 12Mbps, usb 2.0 480Mbps, usb 3.0 5Gbps)

```sh
lsusb
lsusb -t # tree view
```

Use dmesg to view the record of kernel-related events involving devices

```sh
dmesg
```

Device information for DMA, IRQ and I/O

```sh
lsdev
```

RAM info

```sh
dmidecode
dmidecode -t 17
```
