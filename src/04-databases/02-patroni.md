# Patroni

Launch two VMs:

```sh
multipass launch --name primary
multipass launch --name secondary
```

Install dependencies on each machine:

```sh
python -m pip install patroni[etcd,psycopg2-binary]
```

Create a `patroni.yml` config file:

```yml
scope: patroni-cluster
namespace: /service
name: primary

restapi:
  listen: 0.0.0.0:8008
  connect_address: 10.0.0.1:8008

etcd:
  hosts: 10.0.0.1:2379

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576
    postgresql:
      use_pg_rewind: true
      parameters:
        max_connections: 100
        wal_level: replica
        hot_standby: "on"
        wal_log_hints: "on"
  initdb:
    - encoding: UTF8
    - data-checksums

postgresql:
  listen: 0.0.0.0:5432
  connect_address: 10.0.0.1:5432
  data_dir: /var/lib/postgresql/12/main
  config_dir: /etc/postgresql/12/main
  bin_dir: /usr/lib/postgresql/12/bin
  pgpass: /tmp/pgpass
  authentication:
    superuser:
      username: postgres
      password: password
    replication:
      username: replicator
      password: password

tags:
  nofailover: false
  noloadbalance: false
  clonefrom: false
  nosync: false
```
