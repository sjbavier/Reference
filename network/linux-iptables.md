# Working with iptables

To list existing rules

```sh
iptables -L
```

Establishing rules

```sh
iptables -A INPUT -i lo -j ACCEPT # permits all packets for the local loopback interface -A appends rules
iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT # the -m option loads the state module which determines and monitors a packet's state (NEW, ESTABLISHED or RELATED )
iptables -A INPUT -p tcp -m tcp --dport 22 -j ACCEPT # accepts incoming TCP connections on port 22
iptables -A INPUT -j DROP # drops/rejects incoming packets that do not match any of the preceding rules
```

