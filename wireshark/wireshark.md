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

```sh
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

| Specifier   | Description |
| ----------- | ----------- |
| host | 4 decimal digit dot separated IP address
| net | a range of 4 decimal digit dot separate IP address
| src net | from a range of IP addresses
| dst | to a range of IP addresses
| mask | to apply to IP address
| arp | Address Resolution Protocol
| ether proto | ethernet type field
| ether dst | ethernet MAC address of destination
| broadcast | broadcast message across the network
| multicast | ethernet multicast packet
| tcp portrange | TCP destination port number
| tcp port | TCP port number
| ip | all IPv4 traffic
| pppoes | all PPPoE traffic
| vlan | all VLAN traffic
| port | TCP port number 

| Operators | Description |
| --------- | ----------- |
| not | NOT the following |
| and | logical AND of the two adjacent parameters |
| or | logical OR of the two adjacent parameters |

## Saving to a file

Check supported formats

```sh
tshark -F
```

Save raw packet data (not text)

```sh
tshark -i <interface> -w <file.pcap>
```

Save text by redirection

```sh
tshark -i <interface> > file.txt
```
 
## Reading from a file

```sh
tshark -r <file.pcap>
```

Yank the output using the -Y parameter

```sh
tshark -r <file.pcap> -Y ip.addr == 192.168.8.243
```

| Field | Description |
| ----- | ----------- |
| frame.time
| frame.time relative | Relative packet time stamp
| frame.len | Length of the packet
| frame.protocols | Protocol to which the packet belongs
| frame.number | Packet number in the data stream
| eth.addr | 6 hex digit colon separated ethernet MAC address
| eth.dst | 6 hex digit colon separated destination MAC address
| ip.addr | 4 decimal digit dot separated IP address
| ip.src | Sender’s IP address
| ip.dst | Receiver’s IP address
| ip.len | length of the IP packet
| tcp.srcport | TCP source port
| tcp.port | TCP port number
| tcp.dstport | TCP destination port
| udp.port | UDP port number
| col.Info | Received packet’s content
| http.response.code | HTTP response code number
| && | logical AND
| \|\| | logical OR
| > | greater than
| ≥ | greater or equal
| < | less than
| ≤ | less than or equal
| == | equal to
| ! | logical NOT

## analysis

use the -V flag to specify details of each packet

```sh
tshark -V
```

use the -O to specify a protocol

```sh
tshark -O icmp
# to list protocols
tshark -G protocols
```



