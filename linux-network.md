# Working with networks

Change hostnames and modify [/etc/hosts]

```sh
hostname <new-hostname>
```

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
```
