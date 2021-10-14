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

## Changing MYSQL root user password

To reset the password for MySQL you first must create a new file with the following contents:

```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'PASSWORD';
```

Where PASSWORD is the new password to be used. Save that file as ~/mysql-pwd.

Next, stop the MySQL daemon with the command:

```sh
sudo systemctl stop mysql
```

With the daemon stopped, issue the command:

```sh
sudo mysqld -init-file=~/mysql-pwd
```

Once your command prompt is returned, restart the MySQL daemon with the command:

```sh
sudo systemctl start mysql
```

You should now be able to log into the MySQL command prompt with the new admin password like so:

```sh
mysql -u root -p
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
mysql_secure_installation
```

## Configuration

Default Settings and Descriptions

| DEFAULT SETTINGS                  | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                       |
|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| datadir=/var/lib/mysql            | the directory where the data files are stored                                                                                                                                                                                                                                                                                                                     |
| bind_address=0.0.0.0              | the address where the database server will listen for TCP/IP connections.  0.0.0.0 means it will listen on all IP addresses assigned to the host                                                                                                                                                                                                                  |
| port=3306                         | port the database server will be listening                                                                                                                                                                                                                                                                                                                        |
| innodb_buffer_pool_size=134217728 | memory in bytes that is allocated for the buffer pool (assuming using innoDB) for data and indexes that are accessed frequently                                                                                                                                                                                                                                   |
| skip_name_resolve=0               | (boolean) indicates whether hostnames will be resolved or not on incoming connections. Setting to 1 will only use IP addresses. Some overhead if resolving hostnames will be incurred.                                                                                                                                                                            |
| query_cache_size=0                | bytes allocated of disk space to store results of SELECT queries. IE 100M for 100 megabytes                                                                                                                                                                                                                                                                       |
| max_connections=151               | the maximum number of simultaneous client connections to the server.  Each connection will consume a thread and thus memory.                                                                                                                                                                                                                                      |
| thread_cache_size=0               | indicates the number of threads that a server allocates for reuse after a client disconnects and frees threads previously in use.  In this situation it is cheaper in performance to reuse a thread than to instantiate a new one, but this depends on number of connections we are expecting.  Typically it is safe to set as half of the max_connections value. |

### Tuning configuration

Using MYSQL Tuner

```sh
wget https://github.com/major/MySQLTuner-perl/tarball/master
tar xzf master
cd <major-MySQLTuner-perl>
./mysqltuner.pl
```

This will output some helpful recommendations that can be explored

## Basic commands

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
