# Managing firewall rules on various Linux distros

On Centos [firewalld] is the daemon and controlled through [firewall-cmd]

Add firewall allowance for http traffic and ensure permanence on reboot or restart

```sh
firewall-cmd --add-service=http --permanent
```

Check the state of the firewall

```sh
firewall-cmd --state
```

Add port allowance to firewall rules

```sh
firewall-cmd --permanent --add-port=80/tcp
firewall-cmd --permanent --add-port=443/tcp

firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
```

Open port 25 (smtp), port 587 (submission) and port 465 (smtps)

```sh
firewall-cmd --permanent --add-service=smtp
firewall-cmd --permanent --add-service=submission
firewall-cmd --permanent --add-service=smtps
```

To remove allowances

```sh
firewall-cmd --permanent --remove-port=80/tcp
firewall-cmd --permanent --remove-port=443/tcp

firewall-cmd --permanent --remove-service=http
firewall-cmd --permanent --remove-service=https
firewall-cmd --permanent --remove-service=ssh
```

Reload and apply and settings that were updated

```sh
firewall-cmd --reload
```

Using firewall Rich Language

```sh
firewall-cmd --add-rich-rule='rule family="ipv4" \
source address="<ip-address>" port protocol="tcp" port="22" accept'
```

## Ubuntu Uncomplicated firewall [ufw] config: /etc/default/ufw

UFW allow ssh

```sh
ufw allow ssh
```

Enable UFW

```sh
ufw enable
```