# Backups

## File System Level Backup

There are two restrictions, however, which make this method impractical, or at least inferior to the pg_dump method:

The database server must be shut down in order to get a usable backup.
Half-way measures such as disallowing all connections will not work (in part because tar and similar tools do not take an atomic snapshot of the state of the file system, but also because of internal buffering within the server).
Needless to say, you also need to shut down the server before restoring the data.

If you have dug into the details of the file system layout of the database, you might be tempted to try to back up or restore only certain individual tables or databases from their respective files or directories.
This will not work because the information contained in these files is not usable without the commit log files, `pg_xact/\*`, which contain the commit status of all transactions.
A table file is only usable with this information.

## Example

Enable `postgres` login:

```sql
ALTER USER postgres WITH PASSWORD 'Test1234!';
```

In the file `/etc/postgresql/16/main/pg_hba.conf` change `peer` and restart the service.

Example:

```sql
CREATE DATABASE example;
```

Connect:

```sh
\c example
```

Table:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INT
);

INSERT INTO users (name, age)
VALUES
('Alice', 30),
('Bob', 25),
('Charlie', 35);

SELECT * FROM users;
```

## SQL Dumps

The idea behind this dump method is to generate a file with SQL commands that, when fed back to the server, will recreate the database in the same state as it was at the time of the dump.
PostgreSQL provides the utility program pg_dump for this purpose.
The usage of this command is:

```sh
pg_dump -U username -h hostname -d dbname -F format -f $BACKUP
```

Example:

```sh
PGPASSWORD='Test1234!' pg_dump -U postgres -d example -F c -f example.backup
```

Restore to a new database `restored`:

```sh
PGPASSWORD='Test1234!' pg_restore -U postgres -d restored -F c example.backup
```
