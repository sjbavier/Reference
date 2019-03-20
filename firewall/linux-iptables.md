# Working with iptables or its replacement since 2014 nftables

These rules form the basis of a filewall by blocking (DROP) all incoming and forwarding traffic for all interfaces but allowing outgoing

```sh
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT
```

## The following examples are based on these designations

| Designation | Purpose                            |
|-------------|------------------------------------|
| eth0        | connected to internet              |
| eth1        | connected to the DMZ               |
| eth2        | connected to local private network |

To add -A two rules that allow FORWARD chain in the Filter table will allow data packets to move (FORWARD) networks [eth1] and [eth2], allowing your web server in the DMZ to exchange data with a database in the private network

```sh
iptables -A FORWARD -i eth1 -o eth2 -m state \
--state NEW,ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -i eth2 -o eth1 -m state \ 
--state ESTABLISHED,RELATED -j ACCEPT
```

This rule will be added to the NAT table (-t nat), it uses TCP to reroute traffic coming from [eth0] your [public-ip] on port 80 to your web server in the DMZ

```sh
iptables -t nat -A PREROUTING -p tcp -i eth0 -d <public-ip \
--dport 80 -j DNAT --to-destination <web-server-ip>
```
