# WPA and WPA2

## WPA

WPA intruduces a hierarchical key structure; the most important of the keys is the PMK (Pairwise Master Key) which can be calculated in two ways.  The PMK is used to generate the PTK (Pairwise Transient Key) and GTK (Group Temporal Key). There are also EAPOL KCK, EAPOL KEK and Temporal keys.

- PMK is passed to a PBKDF2 function
- PTK is created using a fixed string, AP and Client MAC addresses and nonces sent by client and AP
- PTK is used to encrypt client to AP traffic
- GTK is used to encrypt broadcast traffic
- WPA encryption both PTK and GTK are 512-bit and generated in a four-way handshake

 If WPA-PSK (WPA Personal) is enabled the key is loaded from local resources, otherwise an exteranal server is used for authentication.

### EAP authentication

First sends an association request to the AP, which replies with an authentication request to the client.  Next, several methods broadcast by the AP such as MD5 challenge, TLS, TTLS, or PEAP.  The user is identified and authenticated.  During this process the authenticator communicates with a special authentication server via a different protocol (ie: RADIUS), ideally over a separate wired connection.  The server has a DB with user IDs and passworks and tells the AP if the user is authorized, this uses a centralized infrastructure, using a single server handling multiple APs.

### Dictionary Attack

Uses a captured packets and a txt file containing common passwords, this is time consuming. **must be in monitor mode**

First you must capture packets until you collect the four-way WPA handshake

```sh
airodump-ng --channel 6 --write <packet.cap> <interface>
# or
airodump-ng -c 6 -w <packet.cap> <interface>
```

Next attempt to recover the key using a dictionary file from the cuda-ext archive as the passwords list

```sh
aircrack-ng -w cuda-ext/hackme/dict.txt -0 <packet.cap>
# -w dictionary file
# -0 captured packet
```

## WPA2 

The  key  negotiation  phase  in  WPA2  is  identical  to  the  four-way  handshake  employed  in  WPA  except  for  PMK  size,  now  384  bits.  This update is a by-product of dropping TMK keys. They have been deemed  redundant  due  to  the  omission  of  Michael  (the  CCMP  protocol  has  a  built-in  MIC  generation  function).  Although  as  you  can  see  encryption  has  become  more  complicated  overall,  it  also  delivers stronger security. IVs reappear in WPA2, but the name has been  changed  to  PNs  (packet  numbers).  Similar  to  WPA,  PNs  are  successively  increased,  or  incrementing,  by  1  until  they  overf low.  The PN code is stored in CCMP headers together with the key ID of an encrypted MPDU. The packet number also constructs a Nonce, which  includes  the  said  packet  number,  sender  MAC  address  and  the  priority  field  (no  longer  used  now:  set  to  zero).  The  temporal  key, derived using the same method as in WPA, is passed to the CCMP  encryption  block  alongside  the  Nonce  field,  plaintext  data  and  AAD.  Additional  Authentication  Data  is  a  field  that  contains  information  pertaining  to  all  MAC  header  fields  that  should  not  change in transit. The information includes source and destination address. These inputs are processed by the CCMP function, a stream processing-optimized  AES  algorithm  variant  in  the  CCM  mode.  The AES (Advanced Encryption Standard) is a block cipher, and so you need to feed it data in portions exactly 128 bytes in size. With the  modification,  this  is  not  necessary.  The  CCM  mode  takes  into  account  both  earlier  block  encryption  outputs  and  the  counter  function  output.  The  latter  result  is  concatenated  with  MAC  and  CCMP headers and next sent.

> The only effective attack on WPA2 is a brute force technique, which can be launched offline using a captured four-way handshake.  To sniff this negotiaion you can wait for a user to log on or force using a deauthentication technique. 

### Brute Force w/ dictionary

This attack is time consuming using the dictionary attack.  This is beause PBKDF2 generates the PTK and repeats the HMAC SHA-1 hash 4,096 times.  

First you must capture packets until you collect the four-way WPA handshake

```sh
airodump-ng -w <packet.cap> -c 1 <interface>
# -w packet file
# -c channel
```

Using a dictionary

```sh
aircrack-ng -w <dictionary.file> -0 <packet.cap>
```

### Rainbow tables

