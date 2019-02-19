# Issue with MariaDB where it requires sudo to log in #

First Log in using sudo 

```sh
sudo mysql -u root -p
```

Next run these commands

```sql
SET PASSWORD = PASSWORD('<your-password');
update mysql.user set plugin = 'mysql_native_password' where User='root';
FLUSH PRIVILEGES;
```
