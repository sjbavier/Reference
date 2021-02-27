# Using the nmap tool

To find out all ips/devices on the network

```sh
nmap -sn <ip-addr-range> # run as sudo
```

To scan ports on a host when the host is possibly blocking ping probes

```sh
nmap -Pn <host>
```

Can also scan several ports and subnets

```sh
nmap -p 21,22,80 192.168.0.0/24
```

To scan open ports on a host

```sh
nmap -sT <host> # Open TCP ports
# -s for scan
# -T for TCP

nmap -sU <host> # Open UDP ports
```

To enable OS and version detection, script scanning and traceroute -A and -T4 for faster execution (0-5)

```sh
nmap -A -T4 <host>
```

Scan which ports are open, OS/version detection and -sS sends a TCP SYN scan preventing the 3-way TCP handshake typically leaving no logs

```sh
nmap -A -sS <host-or-IP>
```
