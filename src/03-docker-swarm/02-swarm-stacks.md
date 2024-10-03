# Swarm Stacks

## The Basic Idea

Docker Stacks allows you to declaratively deploy a swarm by utilizing the `docker-compose.yml` file.
This makes it easy to deploy even complex multi-container apps.

The way this works is as follows:

1. You build a swarm.
2. You define you apps in Compose files.
3. You deploy and manage the apps with the `docker stack` command.

Let's say you've successfully completed step 1 and built a swarm with a manager node `mgr` and two worker nodes `wrk1` and `wrk2`.

## Deploying a Standalone App

Let's adapt our `docker-compose.yml` file:

```yml
services:
  example-app:
    image: example-app:latest
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:80"
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
    networks:
      - example-network

networks:
  example-network:
    driver: overlay
```

The main part that has changed is that there is now a `deploy` section and that we have switched to an `overlay` network.

You can now deploy the stack on the `mgr` node:

```sh
docker stack deploy -c docker-compose.yml example
```
