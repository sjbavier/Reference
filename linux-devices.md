# Working with devices

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

List PCI

```sh
lspci
lspci -v
lspci | column -t
```

List scsi/sata devices like hard drives and optical drives

```sh
lsscsi
```

List usb buses

```sh
lsusb
```

Use dmesg to view the record of kernel-related events involving devices

```sh
dmesg
```
