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

# Test

