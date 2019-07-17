# Using the nmap tool

To find out all ips/devices on the network

```sh
nmap -sn <ip-addr-range> # run as sudo
```

To scan ports on a host when the host is possibly blocking ping probes

```sh
nmap -Pn <host>
```

To enable OS and version detection, script scanning and traceroute -A and -T4 for faster execution (0-5)

```sh
nmap -A -T4 <host>
```