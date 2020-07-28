# Working with Electronic Mail

Email terms

- Mail User Agent (MUA)
  - program that sends mail from a computer to an MTA (SMTP)
- Mail Transfer Agent (MTA)
  - delivers email from sending server to delivery server (SMTP)
  - or between other MTAs (SMTP)
- Mail Submission Agent (MSA)
  - accepts mail from the MTA (may be all inclusive or separate program)
- Mail Delivery Agent (MDA)
  - delivers messages to mail spool (may be all inclusive or separate program)

Downloading Mail from MTA

- Post Office Protocol (POP)
  - POP3 - port 110
  - POP3s - port 995 uses SSL
  - defaults to deleting mail from MTA upon downloading
- Internet Mail Access Protocol (IMAP)
  - more powerful, downloads a copy only
- Smart Host or Mail Relay
  - an MTA configured to deliver mail to another MTA
  - for systems that do not have connectivity always
  - mail is submitted to the relay before sending it onwards
  - Mail Queue
    - where the mail is stored, waiting to be processed
- Mailbox
  - where user mail is stored

---

Email structure

- Sender's ID
- Sender's domain
- Destination email address
- Subject line
- Message data

---

## Simple Mail Transfer Protocol (SMTP)

- runs on IP
- uses TCP and UDP port 25

## Mailer options

- Sendmail (1983)
  - complex to setup, difficult to secure
- Postfix (1998)
  - addressed Sendmail's security issues
  - default on Linux
- Qmail (1995)
  - secure, reliable and efficient
  - lacks updates
- Exim (1995)
  - most popular MTA in the world
  - 57% of market share (~2019)
  - long history of security vulnerabilities
  - lots of configuration options and easy to configure

---

## Postfix

Installing

```sh
# remove sendmail (vulnerable)
yum remove sendmail
# install postfix
yum install -y postfix
# set as default MTA
alternatives --set mta /usr/bin/sbin/sendmail.postfix
```

Configuration: check **/etc/postfix/access**

To update configuration use **postmap** which will create a db file

```sh
# update postfix with access file changes
postmap /etc/postfix/access
```

Configuration: **/etc/postfix/mail.cf**

```conf
myhostname = <updated-hostname>
# myhostname = virtual.domain.tld

mydomain = <updated-domain>
# mydomain = localnet.com

# who is the mail coming from, use variable substitution
myorigin = $myhostname
# myorigin = $myhostname
# myorigin = $mydomain

# which network interfaces with postfix answer on
inet_interfaces = all
# inet_interfaces = $myhostname
# inet_interfaces = $myhostname, localhost
# inet_interfaces = localhost

mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain
# other options

mynetworks = <network-CIDR>, 127.0.0.0/8
# other options

# additional option
# instructs postfix to use the get address info system library routine
disable_dns_lookups = yes
```

Check configuration

```sh
postfix check
```

Check firewall for allowing SMTP ports

You send and receive mail with the **mail** command

```sh
# send mail by
<message> | mail -s "This is the subject line" <recipient>
# open mail by
mail
# view mail list and select by numeric value which mail item to read
# &
<number>
```

---

### Aliases and Forwarding

Edit **/etc/aliases**

Simply modify the redirections to the users accounts for their respective mail

Impliment changes with **newaliases**

```sh
newaliases
# creates a db file
```

Can forward mail by creating a **~/.forward** file in the home directory of user

```sh
# permissions: need to be readable by user
# example vim ~/.forward
<forwarding-address>
# name@gmail.com
```
