# Wireless mischief

## MAC address filtering

Often access points have a rudimentary security feature that is called MAC address (unique hardware identifier) filtering that only allows known MAC addresses to connect.

To spoof a MAC address

```sh
ifconfig <interface> hw ether <MAC-ADDRESS>
# ie:
ifconfig wlan1 hw ether 00:0F:B5:34:30:30
```

However you must know the MAC address of an accepted device.  To check available MAC addresses in the pool you can use airodump.

First your interface must be set to monitor mode, some cards don't allow it.  Supported cards include (Atheros, Ralink, Prism):

```sh
iwconfig <interface> mode monitor
```

### Scan MAC addresses

You can use airodump-ng to scan

```sh
airodump-ng <interface>
```

Output of first section:

- BSSID: the basic service set identification; equivalent to the MAC address of the access point
- PWR: signal power
- Beacons: number of captured ESSID broadcasts
- Data: # of captured packets
- #/s: # of packets per second
- CH: number of channels used by network
- MB: maximum transfer (specified in the standard)
- ENC: used encryption (OPN/WEP/WPA/WPA2)
- CIPHER: used cipher (WEP/WEP40/WEP104/TKIP/CCMP/WRAP)
- AUTH: used authentication protocol (SKA/PSK/MGT)
- ESSID: the wireless network name

Output of second section:

- BSSID: the MAC address of the access point the client is associated with
- STATION: the MAC address of the client
- PWR: Signal level
- Rate: maximum acheivable speed of data transfer
- Lost: packets lost over 10 seconds
- Packets: number of packets sent by client
- Probes: the network name the client is connecting to

### Deauthenticating Clients

Circumventing ESSID hiding (hidden network names):

You can deauthenticate a client, forcing a reconnection and the ESSID will be sent in clear text at logons. Deauthenticating clients (also works with open networks) sends a AP MAC address signed deauthentication packet

```sh
# ie:
aireplay-ng -0 1 -a00:14:6C:7E:40:80 -c 00:0F:B5:34:30:30 wlan1
```

- -0: the attack number (attack 0 is deauthentication)
- 1: the number of deauthentication packets to be sent, if set to 0 it will continue sending packets until ctrl + c
- -a 00:14:6C:7E:40:80 MAC address of the AP
- -c 00:0F:B5:34:30:30 MAC address of client to be deauthenticated, if not provided then all stations are deauthenticated.
- wlan1: network interface

## DoS
### RF Jamming

Involves overpowering the signal of a given AP and interferring with the radio frequency transmission.
### CSMA/CA Jamming (carrier sense multiple access with collision avoidance)

In 802.11 networks using CSMA/CA a station prior to transmitting frames will send out an RTS to see if a collision has occurred, if another station is transmitting at the same time it will wait a random backoff time before attempting to re-transmit.

In this type of disruption an attacker modifies the network card drivers and forces the card to continually send out information without checking for collisions.  The channel is sensed as being busy and other users are forced to wait.

### Deauthentication attack

To force all clients to forcibly reauthenticate.

```sh
aireplay-ng -0 0 -a00:14:6C:7E:40:80 -c FF:FF:FF:FF:FF:FF wlan1
aireplay-ng -0 0 -a <AP-MAC> -c <Client-MAC-or-FF:-for-all> <interface>
# FF:FF:FF:FF:FF:FF is the broadcast address which affects all clients
```

- -0: switch for deauthentication
- 0: number of packets, 0 is infinite
- -a: MAC address of access point
- -c: MAC address of client or broadcast address

### Wireless MITM (man in the middle)

Using airbase-ng. TBD

## WEP Encryption

WEP encryption uses and intialization vector combined with a key then generates a pseudorandom keystream of bits using RC4, it is then XORed with the packet and CRC32 checksum to create the output.

### Obtaining keystreams

#### Chopchop

The chopchop attack makes use of the birthday paradox involving probability theory to derive plaintext packets, by chopping appropriate bytes.  It begins by sniffing packets that are captured by a host, if captured it means the checksum is valid and makes use of the CRC32 checksum vulnerability.  As a linear function is used to calculate the CRC32 checksum the laws of mathematics allow CRC32(A+B) = CRC32(A) + CRC32(B).  Chop off the last byte in a valid frame, send an edited message to the Access Point and if the AP drops it this means your A is incorrect and needs to be recalculated with the CRC32 and a different value.  Since there are only 256 possible bytes each subsequent guesses probility for success looks like 1/256 + 1/255 + 1/254 ... with 50% success after 100 guesses.

( data | A | CRC(data+ A))
( data ) ( CRC(data + A) - CRC(A) )

Using the aireplay-ng tool for a chopchop attack

```sh
aireplay-ng -4 -h 00:09:5B:EC:EE:F2 -b 00:14:6C:7E:40:80 wlan1
aireplay-ng -4 -h <client-MAC> -b <BSSID/MAC-access-point> <interface>
```

- -4 identifies the chopchop attack
- -h client MAC address
- -b BSSID of access point
- wlan1 wireless interface

This may take some time, but the output will be a single decrypted packet and the keystream obtained.

#### Fragmentation Attack

In the layers of 802.11 protocol the Data Link Layer is split into two sublayers the LLC (Logical Link Control) and MAC (Media Access Control). The LLC header also includes another header called SNAP (Subnetwork Access Protocol). SNAP is of particular interest because it is placed at the start of the encrypted part and usually has fixed contents with the first 6 bytes in the header being identical while the next two-octet fields indicate either IP or ARP. Usually ARP packets are fixed in length and 36 bytes.  Using this deduction you can obtain the first eight bytes of a keystream.  Next you can divide the packet into 16 smaller fragments and since the packet was using the same keystream you can deduce the keystream (XOR the plaintext and ciphertext) and use the 8-byte subpackets.

Using aireplay-ng to obtain the keystream

```sh
aireplay-ng -5 -b 00:14:6C:7E:40:80 -h 00:0F:B5:AB:CB:9D wlan1
aireplay-ng -5 -b <BSSID-Access-point> -h <client-MAC> <interface>
```

- -5: identifies the fragmentation attack
- -b 00:14:6C:7E:40:80: the BSSID, or the MAC address of the AP
- -h  00:0F:B5:AB:CB:9D: the MAC address of the associated client used to inject packets
- wlan1: the wireless network interface name


### Keystream reuse
