# Swarm Stacks

Docker Stacks allows you to declaratively deploy a swarm by utilizing the `docker-compose.yml` file.
This makes it easy to deploy even complex multi-container apps.

The way this works is as follows:

1. You build a swarm.
2. You define you apps in Compose files.
3. You deploy and manage the apps with the `docker stack` command.
