# Linux boot process

When the power button is pressed the EEPROM chip in the motherboard initializes the POST (Power-On Self Test) and then loads the 1st stage bootloader either in the MBR or in the EFI partition of the first available disk.

Firmware stage

- execute code in the BIOS for legacy systems (first 512 bytes)
  - first 446 bytes contain executable code and error message text
  - next 64 bytes contain partition table
  - last 2 bytes are the magic number as validation to the MBR
- execute code in the UEFI firmware for newer computers
- starts bootloader

GRUB2 stage

- firmware executes bootloader(GRUB2) /boot/grub2/grub.cfg or /boot/grub/grub.cfg (dynamically generated)
- flashboot/grub2/grub.cfg for BIOS UEFI location of config varies
- GRUB2 executes the kernel

Kernel stage

- loads RAMDisk into RAM
- this filesystem loads modules, drivers and possibly automation/installation files
- kernel unmounts the RAMDisk and mounts root filesystem
- kernel starts initiation stage

Initialization stage

- systemd started by kernel formally sys file init and upstart
- systemd starts all other system services including login/graphical UI