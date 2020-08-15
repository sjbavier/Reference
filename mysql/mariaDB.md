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

## Hardening MariaDB

NOTE: RUNNING ALL PARTS OF THIS SCRIPT IS RECOMMENDED FOR ALL MariaDB
SERVERS IN PRODUCTION USE! PLEASE READ EACH STEP CAREFULLY!137
Installing an SQL database

In order to log into MariaDB to secure it, we'll need the current
password for the root user. If you've just installed MariaDB, and
you haven't set the root password yet, the password will be blank,
so you should just press enter here.

Enter current password for root (enter for none):
OK, successfully used password, moving on...

Setting the root password ensures that nobody can log into the MariaDB
root user without the proper authorisation.
Set root password? [Y/n]

```sh
mysql_secure-installation
```

Export the database

```mysql
mysqldump --user=<user> --password=<password> <name-of-database> > <database-file.sql>
```

Create a user

```mysql
CREATE USER '<user>' IDENTIFIED BY '<password>';
```

Set or change a password

```sh
SET PASSWORD FOR '<user>' = '<password>';
```

Import from mysqldump

```mysql
mysql --user=<user> --password=<password> -e "CREATE DATABASE <database-name>" # create the database first
mysql --user=<user> --password=<password> --database=<database-name> < <database-file.sql> # redirect sql file to db
```

Granting all privileges to user on particular db

```mysql
mysql> GRANT ALL PRIVILEGES ON <database-name>.* TO '<username>'@'<host>';
mysql> FLUSH PRIVILEGES;
```

Gathering User information

```mysql
mysql> select * from mysql.user

mysql> select User, Host, Password from mysql.user
```

Changing siteurl and home for wordpress

```mysql
mysql> SELECT * from wp_options WHERE option_name = 'home' OR option_name = 'siteurl';
mysql> UPDATE wp_options SET option_value = '<domain-name>' WHERE option_name = 'home' OR option_name = 'siteurl';
```
