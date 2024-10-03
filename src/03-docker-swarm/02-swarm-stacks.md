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
    image: $USERNAME/example-app:1.0.0
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

Note that Docker Stacks does not support local build contexts, so we need to push the image to a registry first.

The main part that has changed is that there is now a `deploy` section and that we have switched to an `overlay` network.

You can now deploy the stack on the `mgr` node:

```sh
docker stack deploy -c docker-compose.yml example
```

## Commands

List all stacks:

```sh
docker stack ls
```

List the tasks in a stack:

```sh
docker stack ps example
```

List all services in a stack:

```sh
docker stack services example
```
