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

## SSH tunneling

### Local Forwarding

Local forwarding: SSH client listens for connections on a configured port, when it receives the connection it tunnels to an SSH server.  The server connects to a configured destination port, possibly on another machine.

- Tunneling sessions and file transfers through jump servers
- Connecting to a service on an internal network from the outside
- Connecting to a remote file share

```sh
# forwards connection to port 2222 on <local-machine>
# to port 22 connection to <jump-server>
# by default this allows anyone to connect on <local-machine>:2222
ssh -L 2222:<local-machine>:22 <jump-server>
```

Local Forwarding with binding

```sh
# restricting connections to the same host
# by supplying a bind address 127.0.0.1
ssh -L 127.0.0.1:2222:<local-machine>:22 <jump-server>
```

### Remote Forwarding

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