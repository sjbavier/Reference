# Working with networks

Change hostnames and modify [/etc/hosts]

```sh
# systemd's api for standardizing
hostnamectl set-hostname <new-hostname>
# old way
hostname <new-hostname>
```

Set up network on Centos

```sh
nmtui # set up network interfaces gui
systemctl restart network # restart network to update
```

Check connection to ip/address and port

```sh
telnet <ip/addr> <port> # ctrl+]
# telnet>'close' or 'q' to quit
```

---

## Netstat

To display open ports and established TCP connections

```sh
netstat -vatn
```

To display only open UDP ports

```sh
netstat -vat
```

Print listening numeric addresses in a verbose extended way

```sh
netstat -ptnle
```

## Network interfaces

Common network interface tools

```sh
ifconfig # networking interfaces
ip addr # networking interfaces
ip addr show # show ip
iwconfig # wireless networking interfaces
```

List all established ssh connections with ss

```sh
ss -o state established

    '( dport = :ssh or sport = :ssh )'
    Netid Recv-Q    Send-Q  Local Address:Port
    tcp   0         0       10.0.3.1:39874
    timer:(keepalive,18min,0)
```

Find the route packets take to a network host

```sh
traceroute <ip-address>
traceroute <domain>
# use tcp datagrams
tcptraceroute <ip-address>
tcptraceroute <domain>
```

For insight into network usage

```sh
iftop -i eth0 # use iftop (need to install) for information on the eth0 interface
nethogs eth0 # another utility
tcpdump -i eth0 # -i to specify interface
tcpdump -i eth0 -c 5 --n port 22 -vv # -c is count --n to specify port -vv very verbose
tcpdump -nn tcp # specify protocol to intercept packets
tcpdump -i eth0 -nn tcp -w packet-record -s 0 # -w write output to file, -s specify bytes per packet 0 is whole packet
```

## Using tc to shape network traffic

To list all current rules associated with a network interface

```sh
tc -s qdisc ls dev eth0 # qdisc stands for queueing discipline through which packets must pass
```

Adding a rule to delay all traffic by 100ms

```sh
tc -s qdisc add dev eth0 root netem delay 100ms
```

To delete rules added to device eth0

```sh
tc qdisc del dev eth0 root
```

## Network monitoring tools (nmon, nagios, collectd, munin)

nmon is a multi-target system monitoring and benchmarking tools

```sh
nmon -f -s 30 -c 120 # saves data collected every 30 seconds over a full hour (120 * 30)
```

You can use nmonchart to convert the files collected into a html chart

simple convert hex to binary

```sh
echo 'ibase=16;obase=2;<HEXIDECIMAL>' | bc
```