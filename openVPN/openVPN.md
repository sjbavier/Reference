# Working with openVPN

## Table of contents

1. [Installing](#Installing)
2. [PKI](#PKI)
3. [Configure](#Configure)
4. [Test](#Test)

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

Configure Server Keys
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

# Test

