# Working with shorewall

Startup options are controlled by [/etc/default/shorewall]
Firewall configurations are stored in [/etc/shorewall/]

| filename     | purpose                                                           | Required |
|--------------|-------------------------------------------------------------------|----------|
| zones        | Declares the network zones you want to create                     | Yes      |
| interfaces   | Defines which network interfaces will be used for specified zones | Yes      |
| policy       | Defines high-level rules controlling traffic between zones        | Yes      |
| rules        | Defines exceptions to the rules in the policy file                | No       |
| masq         | Defines dynamic NAT settings                                      | No       |
| stoppedrules | Defines traffic flow while Shorewall is stopped                   | No       |
| params       | Sets shell variables for Shorewall                                | No       |
| conntrack    | Exempts specified traffic from Netfilter connection tracking      | No       |

Good documentation is available using man

```sh
man shorewall-<filename>
```

## Creating a zones file

The first line in [/etc/shorewall/zones] defines the shorewall server as a firewall, proceded by 3 active zones ( net = public/internet, dmz = public facing zone, loc = private/local )

```zonesconf
fw firewall
net ipv4
dmz ipv4
loc ipv4
```

## Creating the interfaces file

Associate each of your new zones with one of the three network interfaces you've attached [/etc/shorewall/interfaces]
   detect = network settings automatically detected
   dhcp = network IP addresses automatically assigned
   nosmurfs,routefilter,logmartians = will filter suspicious packets, source domains and log-related events

```interfacesconf
net eth0 detect dhcp,nosmurfs,routefilter,logmartians
dmz eth1 detect dhcp
loc eth2 detect dhcp
```

## Creating a policy file

Established default, baseline behavior [/etc/shorewall/policy].
   net all DROP = silently delete all traffic coming from the internet [net] directed at any destination
   loc net ACCEPT = outbound traffic from [loc] private network is allowed
   fw all ACCEPT = any traffic originating from the firewall should be accepted everywhere
   all all REJECT = any packets not covered by preceding rules will be deleted and a notice will be sent to the sender

```policyconf
net all DROP
loc net ACCEPT
fw all ACCEPT
all all REJECT
```

## Creating a rules file

The rules file works to refine the policy file [/etc/shorewall/rules]
   ACCEPT all dmz tcp 80,443 = allow 80 or 443 to access web server in the [dmz]
   ACCEPT net dmz tcp 22 = allow ssh access from [net] to [dmz] for remote access
   ACCEPT loc dmz tcp 22 = allow local/private [loc] ssh access to [dmz]
   ACCEPT loc fw udp 53 = allow open access to DNS server
   Web(DNAT) net dmz:<dmz-web-server-ip> = allow port-forwarding access from internet [net] to [dmz] web server

```rulesconf
ACCEPT all dmz tcp 80,443
ACCEPT net dmz tcp 22
ACCEPT loc dmz tcp 22
ACCEPT loc fw udp 53
Web(DNAT) net dmz:<server-ip>
```