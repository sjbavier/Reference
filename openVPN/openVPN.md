# Working with openVPN

## Table of contents

1. [Installing](#installing)
2. [PKI](#PKI)
3. [Configure](#configure)
   - [Server Keys](#server-keys)
   - [Client Keys](#client-keys)
   - [Server Conf](#server-conf)
   - [Client Conf](#client-conf)
4. [Test](#test)

## Installing

Packages required openvpn and easy-rsa, ports 22 and 1194

```sh
apt install openvpn && apt install easy-rsa
firewall-cmd --permanent --add-port=22/tcp
firewall-cmd --permanent --add-port=1194/tcp
```

To permit routing in between network interfaces on the server you'll need to uncomment [net.ipv4.ip_forward=1] in [/etc/sysctl.conf] this allows remote clients to be redirected once they are connected

```sh
vim /etc/sysctl.conf
```

To run the new setting run sysctl -p

```sh
sysctl -p
```

## PKI

Working with easy-rsa  [/etc/easy-rsa]

```sh
clean-all # removes old key files to prepare for new key generatoin
pkitool # frontend for openssl
build-ca # uses pkitool script to generate root certificate
build-key-server server # uses the pkitool script to generate a key pair and certificate
build-dh # sets Diffie-Hellman authentication parameters
```

## Configure

### Server Keys

Update environment variables for easy-rsa [/etc/openvpn/easy-rsa/vars]

```sh
cd /etc/openvpn/easy-rsa/
. ./vars # has to run as root
. ./clean-all # script will encourage running clean-all to wipe all content is /etc/openvpn/easy-rsa/keys/
```

After running clean-all script run the build-ca script which uses pkitool to create the root certificate

```sh
./clean-all
./build-ca # generates 2048 bit RSA private key
```

Run build-key script which uses the same pkitool along with the root certificate, use [server] unless running multiple VPNs on this machine

```sh
./build-key-server server
```

OpenVPN uses the Diffie-Hellman algorithm to negotiate authentication for new connections.  The file created running the build-dh script uses the RSA keys that are currently active, if you create new RSA keys you'll need to update.

```sh
./build-dh # this creates keys in /etc/openvpn/easy-rsa/keys/
```

By default openvpn will look for keys in the /etc/openvpn/ directory, but easy-rsa puts them in /etc/openvpn/easy-rsa/keys/

```sh
cp /etc/openvpn/easy-rsa/keys/server* /etc/openvpn
cp /etc/openvpn/easy-rsa/keys/dh2048.pem /etc/openvpn
cp /etc/openvpn/easy-rsa/keys/ca.crt /etc/openvpn
```

### Client Keys

To generate a client.crt and client.key

```sh
./pkitool client
```

You'll need to copy the following to the client and modify ownership

```sh
cp /etc/openvpn/easy-rsa/keys/client.key /home/ubuntu/
cp /etc/openvpn/easy-rsa/keys/ca.crt /home/ubuntu/
cp /etc/openvpn/easy-rsa/keys/client.crt /home/ubuntu/
chown ubuntu:ubuntu /home/ubuntu/client.key
chown ubuntu:ubuntu /home/ubuntu/client.crt
chown ubuntu:ubuntu /home/ubuntu/ca.crt
# or
cp /etc/openvpn/easy-rsa/keys/{ca.crt,client.{key,crt}} /home/ubuntu/
chown ubuntu:ubuntu /home/ubuntu/{ca.crt,client.{key,crt}}
```

### Server Conf

The original OpenVPN installation left some compressed template configuration files

```sh
zcat /openvpn/examples/sample-config-files/server.conf.gz > /etc/openvpn/server.conf # uncompress and cat with zcat
```

Example [/etc/openvpn/server.conf]

```conf
   port 1194
   # TCP or UDP server?
   proto tcp
   ;proto udp
   ;dev tap # If you need to connect multiple network interfaces and the networks they represent by creating and ethernet bridge
   dev tun # dev tun is a simpler and more efficient tunnel that transfers data and not much else
   ca ca.crt
   cert server.crt
   key server.key # This file should be kept secret
   dh dh2048.pem
   server 10.8.0.0 255.255.255.0 # sets the subnet range and netmask that will be used to assign IP addresses to clients as they connect
   ifconfig-pool-persist ipp.txt
   push "route 10.0.3.0 255.255.255.0" # optional: allows remote clients to access private subnets behind the server, also requires network configuration to ensure the private subnet is aware of the openvpn subnet (10.8.0.0)
   keepalive 10 120
   comp-lzo
   port-share localhost 80 # allows client traffic coming from port 1194 to be rerouted to local webserver listening on port 80.  Only work with proto tcp
   user nobody # minimizes privileged system exposure
   group nogroup # user nobody and group nogroup forces clients to work as nobody and nogroup ensures server sessions will be unprivileged
   persist-key
   persist-tun
   status openvpn-status.log # writes session logs to /etc/openvpn/openvpn.log
   log openvpn.log # sets log entries to overwrite old entries
   ;log-append openvpn.log # appends new entries to the existing log file in the /etc/openvpn/ directory
   verb 3 # output verbosity, max is 9
```

Start the openvpn server, you may have to reboot if the following steps do not work

```sh
systemctl start openvpn # may require this syntax: systemctl start openvpn@server
ip addr

   [...]
   4: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc [...]
   link/none
   inet 10.8.0.1 peer 10.8.0.2/32 scope global tun0
```

### Client Conf

You'll need to install openvpn client ( available on Mac, Linux, Windows, Android and iOS )

```sh
apt install openvpn
cp /openvpn/examples/sample-config-files/client.conf /etc/openvpn
```

Example [/etc/openvpn/client.conf]

```conf
   client # identifies computer as a VPN client
   ;dev tap
   dev tun
   proto tcp
   remote 192.168.1.23 1194 # points the client to the servers ip address
   resolv-retry infinite
   nobind
   user nobody
   group nogroup
   persist-key
   persist-tun
   ca ca.crt
   cert client.crt
   key client.key
   comp-lzo
   verb 3
   remote-cert-tls server # enforces server certificate validation in hopes to prevent a man-in-the-middle-attack
```

Launch OpenVPN client with the following arguments that coincide with above client configuration and location

```sh
openvpn --tls-client --config /etc/openvpn/client.conf  # enables tls encryption and location of configuration file
```

# Test