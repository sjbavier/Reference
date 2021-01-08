# Working with networks

## Network Tools

| Legacy   | New Tools                          |
|----------|------------------------------------|
| ifconfig | ip addr                            |
| netstat  | ss, ip route, ip -s link, ip maddr |
| arp      | ip neighbor                        |
| route    | ip route                           |
| iptunnel | ip tunnel                          |

Get IP info

```sh
ip addr
# for a specific device
ip addr show <device>
```

---

## Hostnames

**Restrictions:**

- up to 64 characters
- 7-bit ASCII lowercase
- no spaces
- no dots in name
- recommended to match the static and transient names

**Types of hostnames:**

Static

- stored in **/etc/hostname**

Transient

- dynamic hostname used by kernel
- by default upon boot, it is set to the static hostname
- can by modified at anytime by user or service

Pretty

- UTF-8 string of text presented to the user

View hostnames **/etc/hosts**

```sh
# systemd api
hostnamectl
# legacy
hostname
```

Change hostnames and modify [/etc/hosts] - within /etc/hosts <ip-address> <name> <alias(es)>

```sh
# systemd's api for standardizing
hostnamectl set-hostname <new-hostname>
# old way
hostname <new-hostname>
```

---

## Device configuration (NIC)

In Debian based distros **/etc/network/interfaces**
in Centos **/etc/sysconfig/network-scripts/[device-name]**

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

## **Network Manager** and nmcli

After changing any of the device configuration options use **nmcli** to reload

```sh
# reload configuration changes, c for configuration
nmcli c reload
```

See some nmcli examples

```sh
man nmcli-examples
```

After making any changes using nmcli you must bring the device down and back up again

```sh
# disconnect the device
nmcli dev disconnect <device-name>
# connect the device again
nmcli con up <device-name>
```

Show any connected devices

```sh
nmcli con show
# only show active connections
nmcli con show --active
```

nmcli also has an interactive configuration

```sh
nmcli con edit
```

Alternatively Set up network on Centos

```sh
nmtui # set up network interfaces gui
```

---

## **Systemd Networkd**

- network management stack
- detects and configures network devices
- creates virtual network devices
- not as powerful as NetworkManager
- manages static configurations
- manages dynamic configurations

Looks for configuration files in order of:

- /usr/lib/systemd/network
- /run/systemd/network
- /etc/systemd/network

each file has a **.network** extension and contains a match criteria

Since NetworkManager is enabled by default in order to use networkd

```sh
# stop networkmanager
systemctl disable NetworkManager
# enable networkd
systemctl enable systemd-networkd
```

Networkd uses **networkctl** for cli interfaces

---

## Routing

Routing allows one system to find the network path to another.

Routing Decisions:

1. If the source and destination hosts are on the same physical network, the traffic is forwarded directly
2. If the source and destination hosts are not on the the same physical network then all defined routes in the routing table are tried.
3. If a proper route is not found then the packet is sent to the default gateway.

Show default gateways/routing table

```sh
ip route
# example output
# default via 10.1.29.1 dev eth0 proto static metric 100
# 10.1.29.0/24 dev eth0 proto kernel scope link src 10.1.29.62 metric 100

# destination address: the default signifies the default gateway address
# default via 10.1.29.1
# 10.1.29.0/24

# device:
# dev eth0
# dev eth0

# protocol (/etc/iproute2/rt_protos): kernel means it was installed by autoconfiguration
# static means it was set by administrator and overrides dynamic routing
# proto static
# proto kernel

# scope: of destination (/etc/iproute2/rt_scopes)
# scope link

# source address:
# src 10.1.29.62

# metric: cost of using the route or # of hops
# metric 100
# metric 100
```

Creating static routes

for temporary changes (does not survive reboot)

```sh
# example:
#            # subnet mask    #interface        #device
ip route add 192.168.100.0/24 192.168.100.1 dev team0
```

For permanent routes add to /etc/sysconfig/network-scripts/route-[device-name]
Example:

- interface configuration filename: ifcfg-eth0
- static route configuration filename: route-eth0

Continuing example above in: **/etc/sysconfig/network-scripts/route-team0**

```conf
ADDRESS0=192.168.100.0
NETMASK0=255.255.255.0
GATEWAY0=192.168.100.1
```

---

### Ethernet

check device stats

```sh
ethtool <device>
```

---

### WiFi

List wireless connections with **iwconfig**

```sh
iwconfig # wireless networking interfaces
```

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

configuration files reside in:

- **/etc/resolv.conf**
  - first column [search. domain, nameserver, sortlist, options]
- **/etc/nsswitch.conf**

### **resolv.conf**

```conf
# example: when looking up "test" it would try to resolve
# test.localnet.com test.domain1.com test.domain2.com
search localnet.com domain1.com domain2.com # up to 6 domains
# it defaults to your local domain name if not included

# if localnet.com is our local domain name, we can change the lookup order to try
# otherdomain.com first: test.otherdomain.com test.localnet.com [...]
domain otherdomain.com

# to specify nameservers to query up to three in order
nameserver 8.8.8.8
nameserver 4.2.2.2
nameserver 192.168.8.20

# sort list allows you to sort ip addresses certain networks up to 10 subnet pairs
sortlist 130.155.160.0/255.255.240.0

# options to include
options rotate # queries in a round robin to spread load
options timeout: 5 # number of seconds
options attempts: 2 # number of attempts as name resolution
```

**note:** resolv.conf is a global configuration file, device specific DNS configurations are in the /etc/sysconfig/network-scripts directory and if you include the PEERDNS=yes option in your NIC configuration it will get copied to the /etc/resolv/conf automatically

### **nsswitch.conf**

Used for determining which sources to get name service information from [aliases, ethers, group, hosts, initgroups, netgroups, networks, passwd, protocols, publickey, rpc, services, shadow]

```conf
# for specifying the order in which to resolve hosts
# this will resolve the /etc/hosts file first then dns second in /etc/resolv.conf
hosts: files dns
```

### Systemd Resolvd

using backward compatibility with resolv.conf

```sh
# symlink
ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf

systemctl start systemd-resolved
systemctl enable systemd-resolved

```

Or configure with systemd-networkd configuration files

### DNS tools

nslookup

```sh
nslookup <domain>
```

### dig

customizations can be created in ~/.digrc

using dig and a specific DNS server to resolve

```sh
# using Googles DNS
dig @8.8.8.8 <domain>
```

Only show the answer section with dig

```sh
dig <domain> +nocomments +noquestion +noauthority +noadditional +nostats
# or turn off all and then bring back the answer
dig <domain> +noall +answer
```

To get the mail record

```sh
dig <domain> MX +noall +answer
```

To get the nameserver

```sh
dig <domain> NS +noall +answer
```

To get all records

```sh
dig <domain> ANY +noall +noanswer
```

To get a concise answer (good for scripting) in this case IP only

```sh
dig <domain> +short
```

For a reverse lookup that will give the DNS server (default)

```sh
dig -X <ip-address> +short
```

To use a file to run queries (line-separated)

```sh
dig -f <file-location> +noall +answer
```

---

## Network Monitoriing and debugging

### Address Resolution Protocol (ARP)

Used to communicate and discover link layer address within the boundaries of a single network

```sh
arp
# to see ip addresses instead of names
arp -n
```

---

### Netstat

Show services listening on network ports

```sh
netstat -ltup
# -l listening on network ports
# -t TCP ports
# -u UDP ports
# -p print

# for numeric instead of protocol names add -n
netstat -ltup -n
```

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

Get the routing table

```sh
netstat -r
```

---

### ss


List all established ssh connections with ss

```sh
ss -o state established

    # '( dport = :ssh or sport = :ssh )'
    # Netid Recv-Q    Send-Q  Local Address:Port
    # tcp   0         0       10.0.3.1:39874
    # timer:(keepalive,18min,0)
```

---

### telnet

Check connection to ip/address and port

```sh
telnet <ip/addr> <port> # ctrl+]
# telnet>'close' or 'q' to quit
```

---

### traceroute

Find the route packets take to a network host

```sh
traceroute <ip-address>
traceroute <domain>
# use tcp datagrams
tcptraceroute <ip-address>
tcptraceroute <domain>
```

---

### tcpdump, iftop and nethogs

For insight into network usage

```sh
iftop -i eth0 # use iftop (need to install) for information on the eth0 interface
nethogs eth0 # another utility
tcpdump -i eth0 # -i to specify interface
tcpdump -i eth0 -c 5 --n port 22 -vv # -c is count --n to specify port -vv very verbose
tcpdump -nn tcp # specify protocol to intercept packets
tcpdump -i eth0 -nn tcp -w packet-record -s 0 # -w write output to file, -s specify bytes per packet 0 is whole packet
# show only source and destination IPs, requires gawk
tcpdump -i eth0 -n -c 5 ip | awk '{ print gensub(/(.*)\..*/,"\\1","g",$3), $4, gensub(/(.*)\..*/,"\\1","g",$5) }'
```

---

### Using tc to shape network traffic

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

---

### Network monitoring tools (nmon, nagios, collectd, munin)

nmon is a multi-target system monitoring and benchmarking tools

```sh
nmon -f -s 30 -c 120 # saves data collected every 30 seconds over a full hour (120 * 30)
```

You can use nmonchart to convert the files collected into a html chart

simple convert hex to binary

```sh
echo 'ibase=16;obase=2;<HEXIDECIMAL>' | bc
```