# App Example

This example illustrates a simple standalone app.

You can build an image like this:

```sh
docker build -t example-app .
```

You can run a container like this:

```sh
docker run -d -p 8000:80 fastapi-app
```

You can run the app using Docker Swarm like this:

```sh
docker swarm init
docker stack deploy -c docker-compose.yml example_stack
```
