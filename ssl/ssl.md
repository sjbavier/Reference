# SSL Permissions should be 700 on the directory and 600 on the contents as root:root

```sh
chmod -R 600 <ssl-directory> # recursively modify directory and contents
chmod 700 <ssl-directory> # now apply the proper directory permissions
chown -r root:root <ssl-directory>
```