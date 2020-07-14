# Openssh

Check available SSH keys on computer

```sh
for key in ~/.ssh/id_*; do ssh-keygen -l -f "${key}"; done | uniq
```

Generate ssh key

```sh
ssh-keygen # ( default sha256 ) stored in ~/.ssh
# faster and more secure Edwards-curve Digital Signature Algorithm (EdDSA)
ssh-keygen -t ed25519
# add a comment
ssh-keygen -t ed25519 -C "<comment>"
# add output keyfile
ssh-keygen -t ed25519 -f <output_keyfile>
```

Push ssh public key to remote authorized key file

```sh
ssh-copy-id -i <location-of-key> <user>@<host>

# Below is the deprecated form
cat .ssh/id_rsa.pub \
| ssh <user>@<host> \
"cat >> .ssh/authorized_keys" # text is appended to authorized_keys
```

ssh with particular key

```sh
ssh -i <location-of-key> <user>@<host>
```

## To ssh with graphic support you need to enable X11forwarding

With the package ubuntu-desktop installed:

Edit in [/etc/ssh/sshd_config]

```sh
vim /etc/sshd_config
   X11Forwarding yes
```

Edit in [/etc/ssh/ssh_config]

```sh
vim /etc/ssh/ssh_config
   ForwardX11 yes
```

ssh with -X flag **remember to restart ssh service**

```sh
ssh -X <user>@<host>
```

Then you can launch gnome-mines in Ubuntu

```sh
gnome-mines
```

## Hardening ssh authentication process

Disable root login VIA ssh in [/etc/ssh/sshd_conf]

```sh
vim /etc/ssh/sshd_conf
PermitRootLogin no
```

Disable password authentication and force key pairs [/etc/ssh/sshd_conf]

```sh
vim /etc/ssh/sshd_conf # make sure to add your public key to authorized_keys file before restarting ssh daemon
PasswordAuthentication no
```

---

## SSH tunneling

### Local Forwarding

Local forwarding: SSH client listens for connections on a configured port, when it receives the connection it tunnels to an SSH server.  The server connects to a configured destination port, possibly on another machine.

- Tunneling sessions and file transfers through jump servers
- Connecting to a service on an internal network from the outside
- Connecting to a remote file share

Requires:
sshd_config

```conf
AllowTcpForwarding yes
```

Syntax:
ssh -L
   [bind_address:]port:host:hostport [USER@]ssh_server
   [bind_address:]port:remote_socket [USER@]ssh_server
   local_socket:host:hostport [USER@]ssh_server
   local_socket:remote_socket [USER@]ssh_server

```sh
# ssh -L [LOCAL_IP:]LOCAL_PORT:DESTINATION:DESTINATION_PORT -p [PORT_NUMBER] [USER@]SSH_SERVER
# client localhost listens on port 2222
# forwards connection to <jump-server> 
# then to <remote-machine> port 22
# by default this allows anyone to connect on local-machine:2222
ssh -L 2222:<remote-machine>:22 <jump-server>

# all connections to client at port 80 
# forwarded to ssh_server port 2222
# connected to port 80 on private.server.com
ssh -L 80:private.server.com:80 -p 2222 user@ssh_server
```

### Local Forwarding with binding

```sh
# restricting connections to the same host
# by supplying a bind address 127.0.0.1
ssh -L 127.0.0.1:2222:<remote-machine>:22 <jump-server>
```

### Remote Forwarding

ssh -R [REMOTE:]REMOTE_PORT:DESTINATION:DESTINATION_PORT [USER@]SSH_SERVER

Requires sshd_config:

```conf
GatewayPorts yes
```

For example to allow the public to view a web application on your local machine when you do not have a public IP but you have access to a remote server/host.

```sh
# run this command from local machine
# the remote ssh server/host will listen on port 8080
# then tunnel traffic back to port 3000 on your local machine
# -N is for not executing remote command
# -f is to run in background
ssh -R 8080:127.0.0.1:3000 -N -f user@remote.ssh_server
```

### Reverse Tunneling

Reverse ssh tunneling is useful when you cannot directly connect a local server to a remote server but the remote server can establish a connection to your local server. This involves the remote server establishing a connection to your local server then within that secure connection you can create a private tunnel within the original connection in reverse back to the remote.

On the remote server:

```sh
# To allow a remote server and port to tunnel back to the client host
# Use this command on the <remote-server> aka 'localhost' in this case
# connections to port 43022 on <remote-server> localhost should be
# forwarded to port 22 of the <remote-server>
# and connect to <local-server> using <user>@<local-server>
ssh -R 43022:localhost:22 <user>@<local-server>
# note that this will open a shell on the <user>@<local-server> host
```

Once the connection is established, you can connect to the remote server from the local server.
The remote server is listening on port 43022 on the local server.

```sh
# On the <local-server>
# When we ask for an ssh connection on port 43022
# that connection request will be forwarded to the <remote-server>
ssh localhost -p 43022
```

#### Configuration

By default openSSH only allows connected to remote forwarded ports from the server. There are options to adjust this:

sshd_config:

```conf
# this is the default setting
# prevents connecting to forwarded ports from outside the server
GatewayPorts no

# this allows anyone to connect to the forwarded ports
GatewayPorts yes

# to only allow connections from a specific IP address
GatewayPorts clientspecified
```

```sh
# Using:
# GatewayPorts clientspecified
# we can tunnel connections from <IP-address> to port 8080
# this can allow <IP-address> to access remote server website on <Website-domain>
ssh -R <IP-Address>:8080:localhost:80 <Website-domain>
```

By default openSSH allows TCP forwarding.
Alternative configurations:

```conf
# TCP forwarding allowed:
AllowTcpForwarding yes
AllowTcpForwarding all

# Local TCP forwarding only
AllowTcpForwarding local

# Remote forwarding only
AllowTcpForwarding remote

# no forwarding
AllowTcpForwarding no
```

Another option is forwarding unix domain sockets, the default is yes:

```conf
AllowStreamLocalForwarding yes
# same options as TCP forwarding
# AllowStreamLocalForwarding yes|all|local|remote|no
```