# Working with terminal wireshark

TShark is a terminal oriented version of Wireshark. 

- Inspection of hundreds of protocols
- Live capture and offline analysis
- VoIP analysis
- Read/Write many different capture file formats including: tcpdump (libpcap), Pcap NG, Cisco Secure IDS iplog, Microsoft Network Monitor
- Live data can be read from Ethernet, IEEE 802.11, Bluetooth, USB
- Decryption support including: IPsec, ISAKMP, Kerberos, SNPv3, TLS, WEP, WPA/WPA2
- Coloring rules can be applied
- Output can be exported to XML, PostScript, CSV or plain text

## Specifying devices

Define the interfaces available:

```sh
tshark -D
```

Capture traffic on specific interface, each packet is denoted by a number beginning at each line

```
tshark -i <interface>
# example
tshark -i eth0
# use -c for count ( 10 packets )
tshark -i eth0 -c 10
```

## Specifying hosts

Capture traffic to and from one host

```sh
tshark -i <interface> host <ip>
# example 
tshark -i eth0 host 8.8.8.8
```

Capture traffic coming from one host

```sh
tshark -i <interface> src host <ip>
# example 
tshark -i eth0 src host 8.8.8.8
```

Capture traffic going to one host

```sh
tshark -i <interface> dst host <ip>
# example
tshark -i eth0 dst host 8.8.8.8
```

## Specifying networks

Capture traffic going to and from a network

```sh
tshark -i <interface> net <network-address> mask <network-mask>
# example
tshark -i eth0 net 10.1.0.0 mask 255.255.255.0

# -- or --
tshark -i <interface> net <CIDR>
# example
tshark -i eth0 net 10.1.0.0/24
```

Capture traffic based on network source

```sh
tshark -i <interface> src net <cidr>
# example
tshark -i eth0 src net 10.1.0.0/24
```

Capture traffic based on network destination

```sh
tshark -i <interface> dst net <cidr>
# example
tshark -i eth0 dst net 10.1.0.0/24
```

## Specifying ports

Capture traffic on a port

```sh
tshark -i <interface> port <port-num>
# example
tshark -i eth0 port 53
```

Capture traffic on a port for a host

```sh
tshark -i <interface> host <host> and port <port-num>
# example
tshark -i eth0 host 8.8.8.8 and port 53
```

Capture all ports except

```sh
tshark -i <interface> port not <port-num> and not <port-num>
# example
tshark -i eth0 port not 53 and not 25
```

## Saving to a file

Check supported formats

```sh
tshark -F
```

Save raw packet data (not text)

```sh
tshark -i <interface> -w <file.pcapng>
```

Save text by redirection

```sh
tshark -i <interface> > file.txt
```
 

