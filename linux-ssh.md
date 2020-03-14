# Openssh

Check available SSH keys on computer

```sh
for key in ~/.ssh/id_*; do ssh-keygen -l -f "${key}"; done | uniq
```

Generate ssh key

```sh
ssh-keygen # ( default sha256 ) stored in ~/.ssh
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