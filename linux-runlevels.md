# Working with runlevels on System V and systemd

## System V concepts

## Altering runlevels on boot

| **Level** | **Purpose**                | debian/ubuntu              | slackware                   |
|-----------|----------------------------|----------------------------|-----------------------------|
| 0         | Shutdown or                | ===                        | ===                         |
|           | halt the system            |                            |                             |
|-----------|----------------------------|----------------------------|-----------------------------|
| 1         | Single-user mode,          |                            |                             |
|           | usual alias s or S         |                            |                             |
|-----------|----------------------------|----------------------------|-----------------------------|
| 2         | Multiuser mode             | multiuser  with networking |                             |
|           | without networking         |                            |                             |
|-----------|----------------------------|----------------------------|-----------------------------|
| 3         | Multiuser mode             |                            |                             |
|           | with networking            |                            |                             |
|-----------|----------------------------|----------------------------|-----------------------------|
| 4         |                            |                            | Multiuser  with             |
|           |                            |                            | networking and  windows     |
|-----------|----------------------------|----------------------------|-----------------------------|
| 5         | Multiuser mode with        |                            |                             |
|           | networking and  windows    |                            |                             |
|-----------|----------------------------|----------------------------|-----------------------------|
| 6         | Reboot                     | ===                        | ===                         |
|-----------|----------------------------|----------------------------|-----------------------------|

The default runlevel is determined from **/etc/inittab** from the **id:** entry

```sh
# sample output

#These are the default runlevels in Slackware:
#  0 = halt
#  1 = single user mode
#  2 = unused (but configured the same as runlevel 3)
#  3 = multiuser mode (default Slackware runlevel)
#  4 = X11 with KDM/GDM/XDM (session managers)
#  5 = unused (but configured the same as runlevel 3)
#  6 = reboot

#Default runlevel. (Do not set to 0 or 6)
id:3:initdefault:
```

To alter the runlevel only for 1 boot you can select the runlevel in **GRUB**
=> select the kernel entry for editing
=> move cursor to the end of the line and enter the runlevel #

## Altering runlevels after boot

Print current runlevel

```sh
runlevel
# sample output
N 3 # N means runlevel has not been altered since boot
```

You can use telinit to switch to another runlevel

```sh
telinit 5

runlevel
# sample output
3 5 # 3 is previous runlevel, 5 is current
```

On a system V system such as slackware telinit is really a symbolic link to init

```sh
ls -l $(which telinit)
# sample output
# lrwxrwxrwx 1 root root 4 Aug 28  2011 /sbin/telinit ‑> init*
```

## Other processes in the **/etc/inittab**

Format as follows: **id:runlevels:action:process**

| **type**  | **description**                                                                                         |
|-----------|---------------------------------------------------------------------------------------------------------|
| id        | unique identifier of one to four characters                                                             |
| runlevels | lists runlevels for which the action for this id should be taken. No entry === do action for all levels |
| action    | describes which of several possible actions should be taken                                             |
| process   | tells which process, if any, should be run                                                              |

Some common inittab actions

| **action**  | **purpose**                                                                                                     |
|-------------|-----------------------------------------------------------------------------------------------------------------|
| respawn     | restart the process whenever it terminates                                                                      |
| wait        | start the process once when the specified runlevel is entered and wait for its termination before init proceeds |
| once        | start the process once when the specified runlevel is entered                                                   |
| initdefault | specifies the runlevel to enter after system boot                                                               |
| ctrlaltdel  | execute the associated process when init receives the SIGINT signal, for example CTRL-ALT-DEL                   |

