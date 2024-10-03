# Multi-Container Applications

## Compose Files

Instead of manually starting and stopping services, you can

```yml
services:
  example-app:
    image: example:1.0.0
    container_name: example-app
    build:
      context: .
    ports:
      - "8080:80"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@exampledb:5432/example
    depends_on:
      - exampledb
    networks:
      - example-bridge

  exampledb:
    image: postgres:16.4
    container_name: exampledb
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: example
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - example-bridge

networks:
  example-bridge:
    driver: bridge

volumes:
  db-data:
    driver: local
```

This Docker Compose file defines a setup with two services: `example-app`, which is the application container, and `exampledb`, which is a PostgreSQL database container.
Additionally, it defines a custom network called `example-bridge` that allows both containers to communicate with each other, as well as a volume called `db-data` for persistent database storage.

The first service, `example-app`, uses the Docker image `example:1.0.0`. If the image is not already available locally, it will be built using the Dockerfile located in the current directory (denoted by `context: .`).
The container is named `example-app` for easy reference.
Port 8080 on the host machine is mapped to port 80 inside the container, meaning that when accessing the application via `localhost:8080` on the host, it will forward traffic to the container’s internal port 80. The application depends on a PostgreSQL database, and this connection is configured through the `DATABASE_URL` environment variable, which points to a PostgreSQL instance (`postgresql://postgres:postgres@exampledb:5432/example`). The `depends_on` directive ensures that the `exampledb` service (the database) starts before the application. Both services are connected via the same network (`example-bridge`), allowing them to communicate using their container names.

The second service, `exampledb`, uses the official PostgreSQL Docker image `postgres:16.4`. It defines three environment variables: `POSTGRES_USER` (the database user, in this case, `postgres`), `POSTGRES_PASSWORD` (the user’s password, set to `postgres`), and `POSTGRES_DB` (the name of the database, which is `example`). The database’s data is stored persistently in a Docker volume (`db-data`), which is mounted to the container’s `/var/lib/postgresql/data` directory. This ensures that database data is not lost when the container is stopped or removed.

The `networks` section defines a custom network called `example-bridge` that uses the `bridge` driver, which is a default type of network allowing communication between containers. Both the application and the database services are connected to this network, so they can reach each other using their container names (`example-app` and `exampledb`).

Finally, the `volumes` section defines a volume named `db-data`, which is used to persist the PostgreSQL database’s data. This volume is created with the default local driver and is mounted to ensure that the data in the database remains available even if the container is stopped or deleted.

In summary, this Docker Compose file sets up an environment where an application (`example-app`) and a PostgreSQL database (`exampledb`) can run in separate containers but communicate with each other via a network, with persistent database storage handled by a Docker volume.

Command:

```sh
docker-compose up --build
```
