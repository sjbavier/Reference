# Working with Postgresql

connecting using psql

```sh
psql -U <user> -h localhost
# -U user flag and -h for host etc.
```

psql has built in commands for navigation starting with `\`

```sql
# help command
\?

# list all databases
\l
```

Default databases `template1` and `template0` are default databases. `template1` is the default that your new databases will be spawned off of, if you want to modify the default shape you can modify `template1` to suit that.

`template0` should **never be modified**, if your `template1` gets out of whack you can always recreate from `template0`

---

## Basics

Create database

```sql
CREATE DATABASE <database>;
```

Connect to database

```sql
\c <database>
```

---

### Creating tables

Create a table with a generated auto-generated primary key, and title with constraints as string max length 255 characters, unique and not null.

```sql
CREATE TABLE <table> (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    title VARCHAR ( 255 ) UNIQUE NOT NULL DEFAULT '<default_value>'
);
```

Alter table to add column by name

```sql
ALTER TABLE <table>
ADD COLUMN <column_name> VARCHAR ( 50 ) NOT NULL;
```

---

### Inserting data

Insert data into table (single quotes mean 'this is a literal value' an double quotes mean "this is an identifier of some variety")

```sql
INSERT INTO <table> (
    <column>, <column>, <column>
) VALUES (
    '<value>', '<value>', '<value>' -- comments with --
);

-- ON CONFLICT can be used if row exists
INSERT INTO <table> (
    <column>, <column>, <column>
) VALUES (
    '<value>', '<value>', '<value>',
    '<value>', '<value>', '<value>',
) ON CONFLICT DO NOTHING;

-- ON CONFLICT perform 'upsert'
INSERT INTO <table> (
    <column>, <column>, <column>
) VALUES (
    '<value>', '<value>', '<value>'
) ON CONFLICT (<column>) DO UPDATE SET <column> = '<value>';
```

---

### Updates

Update a field

```sql
UPDATE <table> SET <column> = '<value>' WHERE column = '<value>';

-- update with returning values
UPDATE <table> SET <column> = '<value>' WHERE column = '<value>' RETURNING <column>, <column>, <column>;
-- or returning all
UPDATE <table> SET <column> = '<value>' WHERE column = '<value>' RETURNING *;

--
```

---

### Deletes

```sql
DELETE FROM <table>
WHERE <column>='<value>'
RETURNING *;
```

---

### Selects, limits and offsets

```sql
-- select all
SELECT * FROM <table>;

-- select particular columns limit to the first 5
SELECT <column> <column> <column> FROM <table> LIMIT 5;

-- select particular columns limit to the first 5, after the first 5
SELECT <column> <column> <column> FROM <table> LIMIT 5 OFFSET 5;

-- using WHERE
SELECT * FROM <table> WHERE <column> = '<value>';
SELECT * FROM <table> WHERE <column> = '<value>' AND <column> <= '<value>' OR <column >;

-- select with order by
SELECT * FROM <table> ORDER BY <column>; -- default is ASC
SELECT * FROM <table> ORDER BY <column> DESC;

-- built in functions
-- fuzzy search strings
-- (% match 0 to infinite characters (%<fragment>, %<fragment>%, <fragment>%, <fra%ent>))
SELECT * FROM <table> WHERE <column> LIKE '%<fragment>%';
-- use concat to join multiple strings for fuzzy search
SELECT * FROM <table> WHERE CONCAT(<column>, <column>, <column>) LIKE '%<fragment>%';

-- you can use lower to convert string to lowercase
SELECT * FROM <table> WHERE LOWER(CONCAT(<column>, <column>)) LIKE LOWER('%<fragment>%');
-- or more simply use ilike for case insensitive
SELECT * FROM <table> WHERE CONCAT(<column>, <column>, <column>) ILIKE '%<fragment>%';
```

---

### Aggregates

```sql
-- return total count of all rows as an integer total_count
SELECT <column>, <column> COUNT(*) OVER ()::INT AS total_count FROM <table>;
```

---

## Relationships

Basic one to many

```sql
-- create table1
CREATE TABLE <table1> (
    <table1_id> INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    <column> VARCHAR ( 255 ) UNIQUE NOT NULL
);
-- create related table2
CREATE TABLE <table2> (
    <table2_id> INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    <table1_id> INTEGER,
    <column> VARCHAR ( 255 ) NOT NULL
);
-- select on table1_id
SELECT <column> FROM <table1> WHERE <table1_id> = <INTEGER>;
SELECT <column> FROM <table2> WHERE <table1_id> = <INTEGER>;
-- select inner venn diagram section
SELECT <column>, <column>
    FROM <table2>
    INNER JOIN
        <table1>
    ON
        <table2>.<table1_id> = <table1>.<table1_id>
    WHERE <table2>.<table1_id> = <INTEGER>;


```

### Joins and constraints
