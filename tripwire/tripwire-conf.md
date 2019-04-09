# Working with Tripwire

You control the way Tripwire behaves through two encrypted files kept in [/etc/tripwire/] [tw.cfg] and [tw.pol]

You build those encrypted files from [twcfg.txt] and [twpol.txt]

## Tripwire configuration

Default contents of twcfg.txt

```txt
ROOT =/usr/sbin
POLFILE =/etc/tripwire/tw.pol
DBFILE =/var/lib/tripwire/$(HOSTNAME).twd
REPORTFILE =/var/lib/tripwire/report/$(HOSTNAME)-$(DATE).twr
SITEKEYFILE =/etc/tripwire/site.key
LOCALKEYFILE =/etc/tripwire/$(HOSTNAME)-local.key
EDITOR =/bin/vi
LATEPROMPTING =false
LOOSEDIRECTORYCHECKING =false
MAILNOVIOLATIONS =true
EMAILREPORTLEVEL =3
REPORTLEVEL =3
MAILMETHOD =SENDMAIL
SYSLOGREPORTING =false
MAILPROGRAM =/usr/sbin/sendmail -oi -t
```

Add your email to config to enable reports to be sent

```txt
GLOBALEMAIL    =your@email.com
```

## Tripwire policies

Once you run tripwire and get a feel for the false positives you wish to rectify, take a look at the [twpol.txt] file and find the referenced lines.

For example: bashrc file

```txt
/etc/bashrc -> $(SEC_CONFIG) ;)
# /etc/bashrc -> $(SEC_CONFIG) ;) # commented out like this
```

