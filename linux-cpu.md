# Working with cpu's in linux

To get info on your processor you can query the /proc/cpuinfo pseudo file

```sh
cat /proc/cpuinfo | grep processor
```

To use nice to set the priority of process

```sh
nice -15 /var/script/script.sh
nice --15 /var/script/script.sh # setting to negative value (-15) gives the process a more urgent priority
# can use any number between -20 and 19, the higher the number the nicer the process will be when it comes to giving up resources in favor of other processes.

# to change the nice value of a process that has already been started use renice
renice 15 -p 2145 # to change nice value of process with PID 2145
```