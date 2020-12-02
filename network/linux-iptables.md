# Working with iptables

Iptables is a firewall program for Linux hat monitors traffic from and to your server using tables comprised of rules called chains that filter ingress and egress datagrams.

When a datagram matches a rule its is given a target which can be a chain or one of several special values:

- **ACCEPT** - allow datagram to pass through
- **DROP** - not allow datagram to pass through
- **RETURN** - stop the datagram from traversing a chain and return to the previous chain

## **Filter**: one of the default tables

utilizes 3 chains

- **input** - controls ingress datagrams to the server
- **forward** - filters ingress datagrams that will be forwarded somewhere else.
- **output** - filter egress datagrams that are going out of your server

To list all existing rules

```sh
iptables -L
# verbose listing
iptables -L -v
# to list prerouting nat rules
iptables -L -n -t nat
```

To delete all of the rules

```sh
iptables -F
```

To delete specific rules

```sh
first show all rules with line numbers
iptables -L --line-numbers
# then use the -D option and the INPUT line-number # 3 in this case
iptables -D INPUT 3
```

Changes are only saved in memory, to survive a reboot you must use the following

```sh
sudo /sbin/iptables-save
```

### Defining chain rules

By default the firewall sets all chains to ACCEPT with no rules

Append a rule to the chain

```sh
iptables -A
```

After the **-A** you can combine the following options:

- **-i (interface)** - the network interface that you want to filter (eth0, lo(local), ppp0)
- **-p (protocol)** - the network protocol where the filtering takes place (tcp, udp, udplite, icmp, sctp, icmpv6)
- **-s (source)** - the address where the datagram comes from (hostname or IP)
- **--dport (destination port)** - the destination port number
- **-j (target)** - the target name (ACCEPT, DROP, RETURN), required for each rule
- **-m (module)** - add a module for additional filtering power

The order of rules should follow:

```sh
sudo iptables -A <chain> -i <interface> -p <protocol> -s <source> --dport <port>  -j <target>
```

#### **Examples:**

enable traffic on localhost, this will enable all communications on the localhost such as connections between a database and wep application on the same machine

```sh
iptables -A INPUT -i lo -j ACCEPT
```

enabling HTTP/HTTPS and SSH
**note** it is crucial to use the **DROP** target for all other traffic after defining **--dport** rules to prevent unauthorized connection from accessing the server via other open ports

```sh
# ssh
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
# http
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
# https
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
# **important** DROP all other traffic
iptables -A INPUT -j DROP
```

filter traffic based on source

```sh
# accept traffic
iptables -A INPUT -s <IP|HOST> -j ACCEPT
# drop traffic
iptables -A INPUT -s <IP|HOST> -j DROP
```

adding the **-m (module)** option and additional modules for other options

**iprange** module

```sh
# drop traffic using iprange
iptables -A INPUT -m iprange --src-range 192.168.1.100-192.168.1.200 -j DROP
```


Establishing rules

```sh
iptables -A INPUT -i lo -j ACCEPT # permits all packets for the local loopback interface -A appends rules
iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT # the -m option loads the state module which determines and monitors a packet's state (NEW, ESTABLISHED or RELATED )
iptables -A INPUT -p tcp -m tcp --dport 22 -j ACCEPT # accepts incoming TCP connections on port 22
iptables -A INPUT -j DROP # drops/rejects incoming packets that do not match any of the preceding rules
```

