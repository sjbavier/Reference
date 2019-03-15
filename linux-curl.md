# Working with curl

Check proxy with curl using -I for just headers -v for verbose and -x for proxy

```sh
curl -Iv -x <proxy:port> -U <username:password> <url>
```

Get the main page from Netscape's web-server:

```sh
curl http://www.netscape.com/
```

Get the README file the user's home directory at funet's ftp-server:

```sh
curl ftp://ftp.funet.fi/README
```

Get a web page from a server using port 8000:

```sh
curl http://www.weirdserver.com:8000/
```

Get a directory listing of an FTP site:

```sh
curl ftp://cool.haxx.se/
```

Get the definition of curl from a dictionary:

```sh
curl dict://dict.org/m:curl
```

Fetch two documents at once:

```sh
curl ftp://cool.haxx.se/ http://www.weirdserver.com:8000/
```

Get a file off an FTPS server:

```sh
curl ftps://files.are.secure.com/secrets.txt
```

or use the more appropriate FTPS way to get the same file:

```sh
curl --ftp-ssl ftp://files.are.secure.com/secrets.txt
```

Get a file from an SSH server using SFTP:

```sh
curl -u username sftp://example.com/etc/issue
```

Get a file from an SSH server using SCP using a private key
(not password-protected) to authenticate:

```sh
curl -u username: --key ~/.ssh/id_rsa \ 
      scp://example.com/~/file.txt
```

Get a file from an SSH server using SCP using a private key
(password-protected) to authenticate:

```sh
curl -u username: --key ~/.ssh/id_rsa --pass private_key_password \ 
      scp://example.com/~/file.txt
```

Get the main page from an IPv6 web server:

```sh
curl "http://[2001:1890:1112:1::20]/"
```

Get a file from an SMB server:

```sh
curl -u "domain\username:passwd" smb://server.example.com/share/file.txt
```

## DOWNLOAD TO A FILE

Get a web page and store in a local file with a specific name:

```sh
curl -o thatpage.html http://www.netscape.com/
```

Get a web page and store in a local file, make the local file get the name
of the remote document (if no file name part is specified in the URL, this
will fail):

```sh
curl -O http://www.netscape.com/index.html
```

Fetch two files and store them with their remote names:

```sh
curl -O www.haxx.se/index.html -O curl.haxx.se/download.html
```

## USING PASSWORDS

FTP

To ftp files using name+passwd, include them in the URL like:

```sh
curl ftp://name:passwd@machine.domain:port/full/path/to/file
```

or specify them with the -u flag like

```sh
curl -u name:passwd ftp://machine.domain:port/full/path/to/file
```

## FTPS

It is just like for FTP, but you may also want to specify and use
SSL-specific options for certificates etc.

Note that using FTPS:// as prefix is the "implicit" way as described in the
standards while the recommended "explicit" way is done by using FTP:// and
the --ftp-ssl option.

SFTP / SCP

This is similar to FTP, but you can use the --key option to specify a
private key to use instead of a password. Note that the private key may
itself be protected by a password that is unrelated to the login password
of the remote system; this password is specified using the --pass option.
Typically, curl will automatically extract the public key from the private
key file, but in cases where curl does not have the proper library support,
a matching public key file must be specified using the --pubkey option.

## HTTP

Curl also supports user and password in HTTP URLs, thus you can pick a file
like:

```sh
curl http://name:passwd@machine.domain/full/path/to/file
```

or specify user and password separately like in

```sh
curl -u name:passwd http://machine.domain/full/path/to/file
```

HTTP offers many different methods of authentication and curl supports
several: Basic, Digest, NTLM and Negotiate (SPNEGO). Without telling which
method to use, curl defaults to Basic. You can also ask curl to pick the
most secure ones out of the ones that the server accepts for the given URL,
by using --anyauth.

NOTE! According to the URL specification, HTTP URLs can not contain a user
and password, so that style will not work when using curl via a proxy, even
though curl allows it at other times. When using a proxy, you _must_ use
the -u style for user and password.

## HTTPS

Probably most commonly used with private certificates, as explained below.

## PROXY

curl supports both HTTP and SOCKS proxy servers, with optional authentication.
It does not have special support for FTP proxy servers since there are no
standards for those, but it can still be made to work with many of them. You
can also use both HTTP and SOCKS proxies to transfer files to and from FTP
servers.

Get an ftp file using an HTTP proxy named my-proxy that uses port 888:

```sh
curl -x my-proxy:888 ftp://ftp.leachsite.com/README
```

Get a file from an HTTP server that requires user and password, using the
same proxy as above:

```sh
curl -u user:passwd -x my-proxy:888 http://www.get.this/
```

Some proxies require special authentication. Specify by using -U as above:

```sh
curl -U user:passwd -x my-proxy:888 http://www.get.this/
```

A comma-separated list of hosts and domains which do not use the proxy can
be specified as:

```sh
curl --noproxy localhost,get.this -x my-proxy:888 http://www.get.this/
```