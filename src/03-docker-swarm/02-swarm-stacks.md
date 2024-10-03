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

## Rollout

Create a new image `example-app:2.0.0`:

```sh
docker build -t example-app:2.0.0 .
docker tag example-app:2.0.0 $USERNAME/example-app:2.0.0
docker push $USERNAME/example-app:2.0.0
```

Now redeploy the stack by modifying the `docker-compose.yml` file and redeploying.

## Rollout/Rollback Settings

There are a few important sections that govern updates/rollbacks.

First, `update_config` and `rollback_config`:

- `parallelism` for how many replicas to update at once (e.g. `parallelism: 2` for updating two replicas at a time)
- `delay` for the time to wait between updating/rolling back a group of containers (e.g. `delay: 10s` for waiting 10 seconds between updates)
- `failure_action` for what to do if an update/rollback fails (`continue`, `rollback` or `pause`, of course `rollback` is only available when doing an update)
- `monitor` for specifying a duration to monitor each task after it's updated (e.g. `monitor: 30s` to monitor each updated container for 30 seconds)
- `max_failure_ratio` for the percentage of task failures that Docker will tolerate before marking the update/rollback as failed (e.g. `max_failure_ratio: 0.1` to allow 10% of replicas to fail before considering the update/rollback as a failure)
- `order` to define the order in which Docker stops and starts tasks during the update (e.g. `order: stop-first` means that the current running task is stopped before the new task is started and `order: start-first` means that the new task starts before stopping the old one, i.e. the running tasks briefly overlap)

Here is a good setting if you care about minimizing downtime _even if someone tries to ship a bad image to production_.

First, the `update_config`:

```yml
update_config:
  parallelism: 1 # Update one container at a time to minimize risk
  delay: 5s # Enough time delay between each update to allow time to monitor
  failure_action: rollback # Automatically rollback if an update fails
  monitor: 30s # Monitor updated containers for 30 seconds to catch failures
  max_failure_ratio: 0 # Rollback immediately on any container failure
  order: start-first # Start the new container before stopping the old one to minimize downtime
```

Second, the `rollback_config`:

```yml
rollback_config:
  parallelism: 1 # Roll back one replica at a time to minimize disruptions
  delay: 5s # Add a small delay between rolling back each replica
  failure_action: pause # Pause the rollback if failures are encountered
  monitor: 30s # Monitor each rollback task for 30 seconds to catch any failures
  max_failure_ratio: 0 # Stop rollback immediately on any container failure
```
