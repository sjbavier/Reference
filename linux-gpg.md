# Woring with GnuPG

An implementation of PGP.  Using an asymmetric key pair we can encrypt files or emails.

## Setting it up

Generate a GPG key

```sh
gpg2 --gen-key
```

You will need the public key identity. Listed as pub  2048R/XXXXXXXX. Keys and other info will be in ~/.gnupg

```sh
# list the keys
gpg2 --list-keys
```

Export the public key

```sh
gpg2 --export <user> > <user>.pub
# send it to a key server to send to gnupg.net
gpg2 --send-keys <public-identity-XXXXXXXX>
```

Test your keys went to the public key server by pulling them back

```sh
gpg2 --keyserver hkp://keys.gnupg.net --recv-keys <public-identity-XXXXXXXX>
```

## Import a keypair

In order for someone else to use your key, they'll have to import it into their key ring

```sh
gpg2 -import <path-to-public-keyfile>
# then they can verify with
gpg2 --list-keys
```

## Revoke certificate for key pair

To create a revocation certificate in case they key pair gets compromised

```sh
gpg2 --gen-revoke <user>
# this will generate a certificate after you enter your passphrase, store the certificate in a secure location
```

To edit your key

```sh
gpg2 --edit-key <user>
```

## Encrypt a file

```sh
gpg2 --armor --recipient <user> --output <output-file> --encrypt <input-file>
# --armor is optional if you want to view the encrypted file as plain text
```

Encrypt and sign a file

```sh
gpg2 --armor --recipient <user> --output <output-file> --encrypt --sign <input-file>
```

## Decrypt a file

```sh
# this will display on screen
gpg2 --decrypt <file>
# to decrypt the file in place
gpg2 <file>
```
