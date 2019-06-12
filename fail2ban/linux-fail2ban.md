# Working with fail2ban

## Jails

**jail.conf file contains basic configuration as a starting point but can be overwritten during updates.  Fail2ban uses the separate jail.local to actually read your configurations**

first copy basic jail.conf to jail.local

```sh
cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
```


