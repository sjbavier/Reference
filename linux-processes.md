# Working with processes

/proc and procfs

Kill a process

```sh
kill -9 <pid>
```

## Jobs

run a job in the background **&**

```sh
<command>&
# example output
# [1] 1304
# [<job-id>] <pid>
```

basic job operations

```sh
# list jobs
jobs
# example output
# [1] 1304
# [<job-id>] <pid>
jobs -l # long format

# place current or specified job in background
bg %<job-id>

# bring current or specified job into the foreground
fg %<job-id>
```

In Bash shell: to suspend a running processes **Ctrl-z**

Standard IO and background processes:  unless redirected elsewhere, **stdout** and **stderr** from the **bg** processes are streamed to the **controlling terminal** ( the terminal which started the background application ).  In practice you probably want to have stdin and stdout processes feed to and from files.

## signals

**Ctrl+c** terminates a process sends a **SIGINT** interupt signal the **kill** command sends a **SIGTERM**

Some signals cannot be caught, such as some hardware exceptions.  **SIGKILL** cannot be caught by a signal handler and unconditionally terminates a process

If a **controlling terminal** closes or logs off the shell generally sends a **SIGHUP** hangup signal and likely closes.

**nohup** command starts a process that ignores hangup signals, it appends stdout and stderr to a file, usually $HOME/nohup.out though you can redirect stdout and err.

```sh
nohup sh <file.sh>&
```

Send a **SIGTERM** to job %1

```sh
kill -s SIGTERM %1
```

Use **killall** to send **SIGTERM** to all processes with reg-exp match

```sh
killall <reg-exp>
```

Using **pkill** to send a **SIGTERM**

```sh
pkill <reg-exp>
# pkill <name>
```

Use **pkill** to send a **SIGHUP**

```sh
pkill --signal SIGHUP <reg-exp>
```

## Managing processes from `man ps`

Display the processes running with the same euid=EUID as the current user

```sh
ps
ps -af
# -a display processes with controlling terminals
# -f full format
ps -xf
# -x display processes without controlling terminals
# -f full format
```

Display processes of a particular user

```sh
ps -u <user>
```

Display processes of a particular command

```sh
ps -C <command>
```

Deliniate the output of ps

```sh
ps -C <command> -o pid,sid,tname,cmd
# -o output as comma separated arguments
```

Print the memory usage for a user

```sh
ps -U <user> --format %mem | awk '{memory +=$1};END {print memory}'
```

## pgrep

```sh
pgrep <reg-exp>
# pgrep <name>
pgrep -af
# -a prints the command line
# -f matches against full command line
```

### other useful tools top, htop, vtop, ntop

### More ps commands

Lists processes containing specific <name>

```sh
ps auwx | grep <name>
```

To see every process on the system using standard syntax:

```sh
        ps -e
        ps -ef
        ps -eF
        ps -ely
```

To see every process on the system using BSD syntax:

```sh
        ps ax
        ps axu
```

To print a process tree:

```sh
        ps -ejH
        ps axjf
```

To get info about threads:

```sh
        ps -eLf
        ps axms
```

To get security info:

```sh
        ps -eo euser,ruser,suser,fuser,f,comm,label
        ps axZ
        ps -eM
```

To see every process running as root (real & effective ID) in user format:

```sh
        ps -U root -u root u
```

To see every process with a user-defined format:

```sh
        ps -eo pid,tid,class,rtprio,ni,pri,psr,pcpu,stat,wchan:14,comm
        ps axo stat,euid,ruid,tty,tpgid,sess,pgrp,ppid,pid,pcpu,comm
        ps -Ao pid,tt,user,fname,tmout,f,wchan
```

Print only the process IDs of syslogd:

```sh
        ps -C syslogd -o pid=
```

Print only the name of PID 42:

```sh
        ps -q 42 -o comm=
```

To visualize parent and child shells/processes use pstree ( CentOS might need to install psmisc )

```sh
pstree -p
```

