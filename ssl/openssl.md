# Working with openssl

Using s_client to check connection on TLS versions

```sh
openssl s_client -tls1 -connect <host:port>
openssl s_client -tls1_1 -connect <host:port>
```

Test SSL configuration

```sh
openssl s_client -CApath /etc/ssl/certs/ -connect <host>:443
```
