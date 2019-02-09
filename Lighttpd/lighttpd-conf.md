# Using Lighttpd's configuration files

Checking syntax for any errors

```sh
lighttpd -t -f /etc/lighttpd/lighttpd.conf
```

For server testing

```sh
lighttpd -D -f /etc/lighttpd/lighttpd.conf
```