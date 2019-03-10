# Working with networks

Change hostnames and modify [/etc/hosts]

```sh
hostname <new-hostname>
```

## Netstat

To display open ports and established TCP connections

```sh
netstat -vatn
```

To display only open UDP ports

```sh
netstat -vat
```

Print listening numeric addresses in a verbose extended way

```sh
netstat -ptnle
```

## Network interfaces

Common network interface tools

```sh
ifconfig # networking interfaces
ip addr # networking interfaces
iwconfig # wireless networking interfaces
```

