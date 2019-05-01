# Working with cpu's in linux

To get info on your processor you can query the /proc/cpuinfo pseudo file

```sh
cat /proc/cpuinfo | grep processor
```

To use nice to set the priority of process

```sh
nice -15 /var/script/script.sh
# can use any number between -20 and 19, the higher the number the nicer the process will be when it comes to giving up resources in favor of other processes.
```