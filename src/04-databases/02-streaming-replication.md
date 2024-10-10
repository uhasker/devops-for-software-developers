# Streaming Repliaction

## Write Ahead Log

At all times, PostgreSQL maintains a write ahead log (WAL) in the `pg_wal/` subdirectory of the cluster's data directory.

The log records every change made to the database's data files. This log exists primarily for crash-safety purposes: if the system crashes, the database can be restored to consistency by “replaying” the log entries made since the last checkpoint. However, the existence of the log makes it possible to use a third strategy for backing up databases: we can combine a file-system-level backup with backup of the WAL files. If recovery is needed, we restore the file system backup and then replay from the backed-up WAL files to bring the system to a current state.

## Warm Standby vs Hot Standby

Continuous archiving can be used to create a high availability (HA) cluster configuration with one or more standby servers ready to take over operations if the primary server fails.
This capability is widely referred to as **warm standby** (or **log shipping**).

It should be noted that log shipping is asynchronous, i.e., the WAL records are shipped after transaction commit.
As a result, there is a window for data loss should the primary server suffer a catastrophic failure; transactions not yet shipped will be lost.

A server enters standby mode if a `standby.signal` file exists in the data directory when the server is started.

In standby mode, the server continuously applies WAL received from the primary server.
The standby server can read WAL from a WAL archive or directly from the primary over a TCP connection (streaming replication).

Standby mode is exited and the server switches to normal operation when `pg_ctl promote` is run, or `pg_promote()` is called.

Streaming replication allows a standby server to stay more up-to-date than is possible with file-based log shipping.
The standby connects to the primary, which streams WAL records to the standby as they're generated, without waiting for the WAL file to be filled.

## Primary Setup

We need to edit the config file `/etc/postgresql/16/main/postgresql.conf` on `primary`:

```
listen_addresses = '*'
wal_level = replica
max_wal_senders = 10
wal_keep_size = 64
```

These are the explanations:

The `listen_addresses` setting specifies the TCP/IP address(es) on which the server is to listen for connections from client applications.
The value takes the form of a comma-separated list of host names and/or numeric IP addresses.
The special entry `*` corresponds to all available IP interfaces.
The entry `0.0.0.0` allows listening for all IPv4 addresses and `::` allows listening for all IPv6 addresses.

The `wal_level` determines how much information is written to the WAL.
The default value is `replica`, which writes enough data to support WAL archiving and replication, including running read-only queries on a standby server.

The `max_val_senders` value pecifies the maximum number of concurrent connections from standby servers or streaming base backup clients (i.e., the maximum number of simultaneously running WAL sender processes).
The default is 10.
The value 0 means replication is disabled.
Abrupt disconnection of a streaming client might leave an orphaned connection slot behind until a timeout is reached, so this parameter should be set slightly higher than the maximum number of expected clients so disconnected clients can immediately reconnect.
This parameter can only be set at server start.

The `wal_keep_size` value specifies the minimum size of past WAL files kept in the pg_wal directory, in case a standby server needs to fetch them for streaming replication.
If a standby server connected to the sending server falls behind by more than wal_keep_size megabytes, the sending server might remove a WAL segment still needed by the standby, in which case the replication connection will be terminated.

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
