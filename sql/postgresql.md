# Working with Postgresql

connecting using psql

```sh
psql -U <user> -h localhost
# -U user flag and -h for host etc.
```

psql has built in commands for navigation starting with `\`

```psql
# help command
\?

# list all databases
\l
```

Default databases `template1` and `template0` are default databases. `template1` is the default that your new databases will be spawned off of, if you want to modify the default shape you can modify `template1` to suit that.

`template0` should **never be modified**, if your `template1` gets out of whack you can always recreate from `template0`

---

Create database

```psql
CREATE DATABASE <database>;
```
