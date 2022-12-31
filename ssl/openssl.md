# Working with openssl

Get a full list of standard commands

```sh
openssl help
```

---

## Basic file encryption

List key algorithms for enc

```sh
openssl enc -list
```

Encrypt a file using `enc`

```sh
# using aes-256 and password-based key derivation function 2
openssl enc -aes-256-cbc -pbkdf2 -in <input-file> -out <output-file>
# this will prompt you for a password
```

Unencrypt a file using `enc`

```sh
openssl enc -aes-256-cbc -d -pbkdf2 -in <encrypted-file>
# this will prompt for the password
```

---

## Public and Private keys

Using the RSA algorithm create a public and private key pair

```sh
openssl genrsa -out key.pem 4096
# for information about how your key was generated
openssl rsa -in key.pem -text -noout
```

Extract the public key from the `pem` key (contains public, private and root certificate and optionally the certificate signing request CSR)

```sh
openssl rsa -in key.pem -pubout -out pub-key.pem
```

Encrypt/decrypt a file with the pubic/private key pair (file can't exceed the key length)

```sh
openssl pkeyutl -encrypt -in <input-file> -inkey <public-key.pem> -out <output-file>
# decrypt
openssl pkeyutl -decrypt -in <input-file> -inkey <private-key.pem> -out <output-file>
```

---

## Digital Signatures

Create a digest value (hash) of the information

```sh
openssl dgst -<hash-algorithm> -out <digest> <input-file>
# for a list of hash algorithms
openssl dgst -list
```

Compute the signature of the digest value using the public key

```sh
openssl pkeyutl -sign -in <digest> -inkey <public-key.pem> -out <signature>
```

Check validity of the signature

```sh
openssl pkeyutl -verify -sigfile <signature> -in <digest> -inkey <public-key.pem>
```

---

## Certificate Signing Requests

Create a new RSA 2048 bit private key with CSR ( common for HTTPS, Apache, Nginx )

The CSR can be sent to a Certificate Authority ( CA ) to request a SSL cert, if your CA supports SHA-2 be sure to add the -sha256 option to sign with SHA-2

```sh
openssl req -newkey rsa:2048 -nodes -keyout <domain-private-key.key> -out <domain-csr.csr>
# -nodes indicates not password protected
openssl req -newkey rsa:2048 -nodes -keyout <domain-private-key.key> -sha256
 -out <domain-csr.csr>
```

To create a CSR for a private key that already exists

```sh
openssl req -key <private-key.key> -new -out <domain-csr.csr>
```

If you already have a certificate that you need to renew and don't have the original CSR

```sh
openssl x509 -in domain.crt -signkey <domain-private-key.key> -x509toreq -out domain.csr
# -x509toreq is needed to define certificate type
```

---

## Generating Self-Signed SSL Certificates

Generate a self-signed certificate and private key

```sh
openssl req -newkey rsa:2048 -nodes -keyout <domain-private-key.key> -x509 -days 365 -out <domain-crt.crt>
openssl req -newkey rsa:4096 -x509 -sha512 -nodes -out <domain-crt.crt> -days 365 -keyout <domain-private-key.key>
```

If you already have a private key and want to create a self-signed cert

```sh
openssl req -key <domain-private-key.key> -new -x509 -days 365 -out <domain-crt.crt>
# -new is necessar to denote new CSR from existing key
```

---

## Viewing Certificates

Decode certificate from PEM format CSR in plain text

```sh
openssl req -text -noout -verify -in <domain-csr.csr>
```

View certificates content in plain txt

```sh
openssl x509 -text -noout -in <domain-crt.crt>
```

To verify from a specific Certificate Authority

```sh
openssl verify -verbose -CAFile <ca-crt.crt> <domain-crt-.crt>
```

---

## Checking TLS connections

Using s_client to check connection on TLS versions

```sh
openssl s_client -tls1 -connect <host:port>
openssl s_client -tls1_1 -connect <host:port>
```

Test SSL configuration

```sh
openssl s_client -CApath /etc/ssl/certs/ -connect <host>:443
```

## Writing Diffie-Hellman Keys

If this option is used, DSA rather than DH parameters are read or created; they are converted to DH format. Otherwise, "strong" primes (such that (p-1)/2 is also prime) will be used for DH parameter generation.

DH parameter generation with the -dsaparam option is much faster, and the recommended exponent length is shorter, which makes DH key exchange more efficient. Beware that with such DSA-style DH parameters, a fresh DH key should be created for each use to avoid small-subgroup attacks that may be possible otherwise.

```sh
# -dsaparam
openssl dhparam -dsaparam -out dhparam2.pem 4096
```
