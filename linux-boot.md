# Linux boot process

Firmware stage

- execute code in the BIOS for legacy systems
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