# Networking

## Bridge Networks

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

Run a Postgres container:

```sh
docker run \
  --name database \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=mydb \
  postgres:16.4
```

You'll see an error `Cannot connect to database` with this message:

```
could not translate host name "database" to address: Name or service not known\n
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
docker network create example-bridge
```

Start:

```sh
docker run -d \
  --name example-app \
  --network=example-bridge \
  -p 8080:80 \
  example:1.0.0
```

Start:

```sh
docker run -d \
  --name exampledb \
  --network=example-bridge \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=example \
  postgres:16.4
```
