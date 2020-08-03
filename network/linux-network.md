# Working with networks

## Device configuration

In Debian based distros **/etc/network/interfaces** 
in Centos **/etc/sysconfig/network-scripts**

- DEVICE: The logical name of the device, such as eth0 or enp0s2.
- HWADDR: The MAC address of the NIC that is bound to the file, such as 00:16:76:02:BA:DB
- ONBOOT: Start the network on this device when the host boots. Options are yes/no. This is typically set to "no" and the network does not start until a user logs in to the desktop. If you need the network to start when no one is logged in, set this to "yes".
- IPADDR: The IP Address assigned to this NIC such as 192.168.0.10
- BROADCAST: The broadcast address for this network such as 192.168.0.255
- NETMASK: The netmask for this subnet such as the class C mask 255.255.255.0
- NETWORK: The network ID for this subnet such as the class C ID 192.168.0.0
- SEARCH: The DNS domain name to search when doing lookups on unqualified hostnames such as "example.com"
- BOOTPROTO: The boot protocol for this interface. Options are static, DHCP, bootp, none. The "none" option defaults to static.
- GATEWAY: The network router or default gateway for this subnet, such as 192.168.0.254
- ETHTOOL_OPTS: This option is used to set specific interface configuration items for the network interface, such as speed, duplex state, and autonegotiation state. Because this option has several independent values, the values should be enclosed in a single set of quotes, such as: "autoneg off speed 100 duplex full".
- DNS1: The primary DNS server, such as 192.168.0.254, which is a server on the local network. The DNS servers specified here are added to the /etc/resolv.conf file when using NetworkManager, or when the peerdns directive is set to yes, otherwise the DNS servers must be added to /etc/resolv.conf manually and are ignored here.
- DNS2: The secondary DNS server, for example 8.8.8.8, which is one of the free Google DNS servers. Note that a tertiary DNS server is not supported in the interface configuration files, although a third may be configured in a non-volatile resolv.conf file.
- TYPE: Type of network, usually Ethernet. The only other value I have ever seen here was Token Ring but that is now mostly irrelevant.
- PEERDNS: The yes option indicates that /etc/resolv.conf is to be modified by inserting the DNS server entries specified by DNS1 and DNS2 options in this file. "No" means do not alter the resolv.conf file. "Yes" is the default when DHCP is specified in the BOOTPROTO line.
- USERCTL: Specifies whether non-privileged users may start and stop this interface. Options are yes/no.
- IPV6INIT: Specifies whether IPV6 protocols are applied to this interface. Options are yes/no.



### Ethernet

### WiFi

#### debugging

check the channels used on your wifi device using **iwlist**

```sh
# a detailed scan of wifi signals
iwlist <device> scan
# grep for the channel including frequency
iwlist <device> scan | grep \(Channel
```

---

## DHCP configuration

---

## DNS configuration



##

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