# Networking

## CNM Terminology

CNM = Container Network Model

A sandbox is an isolated network stack that includes things like Ethernet interfaces, ports, routing tables (and everything else you would expect from a network stack).

An endpoint is a virtual network interface.
It behaves exactly like a regular network adapter (physical network interface), i.e. you can only connect them to a single network.

A network is a virtual switch (usually an implementation of a 802.1d bridge).
They group together and isolate endpoints that need to communicate.

## Single-Host Bridge Networks

Single-Host bridge network can be created with the `bridge` driver:

- single-host (only spans a single Docker host)
- bridge (implementation of a 802.1d bridge)

Containers on the same bridge network can communicate, but you need to map ports from the container to the host to communicate from outside.

Flask app:

```python
from flask import Flask, jsonify
import psycopg2
from psycopg2 import OperationalError

app = Flask(__name__)

DATABASE_URL = "dbname=example user=postgres password=postgres host=exampledb"

@app.route('/')
def hello():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('SELECT version()')
        db_version = cursor.fetchone()
        cursor.close()
        return jsonify(message="Hello from Flask!", db_version=db_version)
    except OperationalError as e:
        return jsonify(error="Cannot connect to database", message=str(e))
    finally:
        if conn:
            conn.close()
```

Build the app:

```sh
docker build -t example:1.0.0 .
docker run -d --name example -p 8080:80 example:1.0.0
```

Inspect networks:

```sh
docker network ls
```

Inspect a network:

```sh
docker network inspect bridge
```

Create a user-defined network:

```sh
docker network create -d bridge example-bridge
```

Inspect networks:

```
NETWORK ID     NAME             DRIVER    SCOPE
ad7897738e86   bridge           bridge    local
18e749c36705   example-bridge   bridge    loca
```

Behind the scenes this Docker bridge network creates a new Linux bridge in the host's kernel:

```sh
brctl show
```

The output will be something like:

```
bridge name	bridge id		STP enabled	interfaces
br-18e749c36705		8000.024201c6b6bd	no
docker0		8000.0242bf7dd089	no
```

Start a container and attach it to the `example-bridge` network:

```sh
docker run -d \
  --name example-app \
  --network=example-bridge \
  -p 8080:80 \
  example:1.0.0
```

Inspect the network:

```sh
docker network inspect example-bridge --format '{{json .Containers}}'
```

Start another container and attach it to the `example-bridge` network:

```sh
docker run -d \
  --name exampledb \
  --network=example-bridge \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=example \
  postgres:16.4
```

Docker automatically registers container names with an internal DNS service and allows containers on the same network to find each other by name (except for the default `bridge` network).

### Removal

To delete a network:

```sh
docker network rm $NETWORK
```

To remove all unused networks:

```sh
docker network prune
```

Alternatively:

```sh
docker network rm $(docker network ls -q)
```

TODO: Overlay networking!
