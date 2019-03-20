# AD Authentication

```squidconf
auth_param basic program /usr/lib64/squid/basic_ldap_auth -R -b OU=users,OU=<ou>,DC=<dc>,DC=<dc> -D ldap-service-acct@<domain> -W /etc/squid/<password-file> -f sAMAccountName=%s -v 3 -s sub -H -Z -P 636 <url-ldap-server>
auth_param basic children 5
auth_param basic realm Please Enter Your Credentials to Gain Access to the Proxy
auth_param basic credentialsttl 1 hour
```

Require authentication

```squidconf
acl ldapauth proxy_auth REQUIRED
```

Attach whitelisted journal domain list

```squidconf
acl whitelist url_regex -i "/etc/squid/whitelisted.txt"
```

Per [https://wiki.squid-cache.org/Features/Authentication]

```squidconf
http_access deny !ldapauth
http_access allow ldapauth whitelist
http_access deny all
```

AD Group Membership

```squidconf
external_acl_type ldap_group %LOGIN /usr/lib64/basic_ldap_group
```

Create access lists for AD groups ( acl <access_list> external <external_acl_type_value> <name_of_AD_group> )

```squidconf
acl journal_acl external ldap_group ad_group
```

Attach http access rule to acl

```squidconf
http_access journal_acl rule1
```

## SSL Bump

Per [https://wiki.squid-cache.org/squidconfigExamples/Intercept/SslBumpExplicit]

```squidconf
http_port 3128 ssl-bump \
  cert=/etc/squid/ssl_cert/private-key-and-cert.pem\
  generate-host-certificates=on dynamic_cert_mem_cache_size=4MB

sslcrtd_program /usr/lib64/squid/ssl_crtd -s /var/lib/ssl_db -M 4MB

acl step1 at_step SslBump1

ssl_bump peek step1
ssl_bump bump all
```

## Force https

```sh
https_port <port> cert=<cert-pem> key=<private-key-pem> cafile=<cert-chain>
```