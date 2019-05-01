# Working with processes

Kill a process

```sh
kill -9 <pid>
```

## Managing processes from `man ps`

Display the processes running with the same euid=EUID as the current user

```sh
ps
```

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

