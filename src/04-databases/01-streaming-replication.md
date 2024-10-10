# Streaming Repliaction

## Primary Setup

We need to edit the config file `/etc/postgresql/16/main/postgresql.conf` on `primary`:

```
listen_addresses = '*'
wal_level = replica
max_wal_senders = 10
wal_keep_size = 64
```

Edit `/etc/postgresql/16/main/pg_hba.conf` on `primary`:

```
host    replication     replicator      10.113.99.159/32        scram-sha-256
```

Create a replication user on `primary`:

```sql
CREATE ROLE replicator WITH REPLICATION LOGIN ENCRYPTED PASSWORD 'Test1234!';
```

Restart PostgreSQL on `primary`:

```sh
sudo systemctl restart postgresql
```

## Secondary Setup

Stop the service:

```sh
sudo systemctl stop postgresql
```

Delete old data on secondary (stop postgres):

```sh
sudo rm -rf /var/lib/postgresql/16/main
sudo mkdir /var/lib/postgresql/16/main
sudo chown postgres:postgres /var/lib/postgresql/16/main
sudo chmod 700 /var/lib/postgresql/16/main
sudo -u postgres pg_basebackup -h 10.113.99.202 -D /var/lib/postgresql/16/main -U replicator -W -P --wal-method=stream
```

Now add to `/etc/postgresql/16/main/postgresql.conf`:

```
primary_conninfo = 'host=10.113.99.202 port=5432 user=replicator password=Test1234!'
```

Add `sudo touch /var/lib/postgresql/16/main/standby.signal`.

## Failover

Promote:

```sh
sudo -u postgres pg_ctlcluster 16 main promote
```

Do:

```sql
SELECT pg_is_in_recovery();
```
