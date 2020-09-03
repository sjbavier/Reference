# Pluggable Authentication Modules (PAM)

Present on all modern Linux distros, PAM offer the flexibility of setting a specific authentication scheme and provides dynamically the library that contains the functions for the right authentication scheme.

Changing the authentication scheme for the program is easy and involves editing the configuration file most likely located in /etc/pam.d or (but no likely) in /etc/pam.conf

We can tell if certain applications use PAM by checking if the PAM library (libpam) has been linked to it:

using ldd (list dynamic dependencies)

```sh
# check the login
ldd $(which login) | grep libpam # output should show using libpam
# check top
ldd $(which top) | grep libpam # top should not use libpam
```

Taking a look at /etc/pam.d/passwd

```conf
cat /etc/pam.d/passwd

auth        include     system-auth
account     include     system-auth
password    substack    system-auth
-password   optional    pam_gnome_keyring.so use_authtok
password    substack    postlogin
```

First column types available:

- **account**: this module checks if the user or service has supplied valid credentials to authenticate
- **auth**: this module type verifies that the user is who he/she claims to be and grants any needed privileges
- **password**: this module type allows the user or service to update their password
- **session**: this module type indicates what should be done before and/or after the authentication succeeds

Second column (control)

- **requisite**: if authentication via this module fails, overall authentication will be denied immediately
- **required**: is similar to requisite, although all other listed modules for this service will be called before denying authentication
- **sufficient**: if the authentication via this module fails, PAM will still grant authentication even if previous marked as required failed
- **optional**: if the authentication via this module fails or succeeds, nothing happens unless this is the only module of its type definined for this service
- **include**: lines of the given type should be read from another file
- **substack**: is similar to includes but authentication failures or successes do not cause the exit of the complete module only the substack