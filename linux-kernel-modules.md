# Working with kernel modules

Before hot plugging, the operating kernel added additional hardware could not be used unless it was built into the operating system kernel

Today's kernel is minimal and device support is configured by loadable kernel modules (LKMs)

To print kernel version

```sh
uname -r
```

To get current status of modules on a linux system **/proc/modules**

```sh
lsmod
```

To get information about a particular module, **does not include built in modules**

```sh
modinfo <module>
modinfo -F <field> <module> # to output a particular field
```

If you don't specify the full filename in modinfo is searches for a module in **/lib/modules/$(uname -r)/kernel**

There are also module dependencies listed in **/lib/modules/$(uname -r)/modules.dep**, module aliases in **/lib/modules/$(uname -r)/modules.alias** and built in modules **/lib/modules/$(uname -r)/modules.builtin**

To remove a module ( careful of dependencies )

```sh
modprobe -r <module> # remove or unload
```

To load or insert a module

```sh
modprobe -a <module>
```

Additional modprobe options

```sh
modprobe -n # --dry-run
modprobe --show # shows what will be done similar to -n
modprobe -v # verbose
```

Some modules may have parameters that need to be provided during a modprobe -a, these can be seen using modinfo and more information is included in the man page for modprobe