# Docker Swarm

## Key Concepts

Docker Swarm allows you to perform container orchestration and adds features such as self-healing, scaling, rollouts and rollbacks.

A swarm consists of multiple Docker nodes.
A node is an instance of the Docker engine participating in the swarm.
Each node is either a manager node or a worker node.

Worker nodes run the actual services and manager nodes manage the worker nodes.

Docker Swarm uses a declarative model.
When you create a service, you define its desired state (number of replicas, exposed ports, available resources etc) and Docker works to maintain the desired state.
This works by continually monitoring the actual state and performing state reconciliation if the actual state doesn't match the desired state.

For example, if you specify 5 replicas for a service and there are only 4 replicas present (e.g. because a replica crashed or you just requested a rescaling), Docker will start a new replica.

The atomic scheduling unit is the **task**.
A task carries a Docker container and the commands to run inside the container.
Manager nodes assign tasks to worker nodes.

A **service** is the definition of tasks to execute on nodes.

## Launch machines

We use `multipass`:

```sh
sudo snap install multipass
```

Launch the machines:

```sh
multipass launch docker --name mgr
multipass launch docker --name wrk1
multipass launch docker --name wrk2
```

Get the IP addresses:

```sh
multipass list
```

Our output (yours will be different):

```
Name                    State             IPv4             Image
mgr                     Running           10.113.99.167    Ubuntu 22.04 LTS
wrk1                    Running           10.113.99.87     Ubuntu 22.04 LTS
wrk2                    Running           10.113.99.29     Ubuntu 22.04 LTS
```

Login to `mgr`:

```sh
multipass shell mgr
```

Initialize a new swam on `mgr`:

```sh
docker swarm init --advertise-addr 10.113.99.167:2377 --listen-addr 10.113.99.167:2377
```

This initializes a new swarm:

- `advertise-addr` tells Docker which IP address to advertise as the swarm API endpoint
- `listen-addr` tells Docker which of the node's interfaces to accept swarm traffic on

List the nodes in the swarm:

```sh
docker node ls
```

Output:

```
ID                            HOSTNAME   STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
t49oodaobyzvy5vfdbqowtcud *   mgr        Ready     Active         Leader           27.3.1
```

You can run `docker swarm join-token worker` and `docker swarm join-token manager` respectively to see what commands we need to execute to add new workers and managers.

Join the two workers nodes:

```sh
docker swarm join --token $WORKER_TOKEN 10.113.99.167:2377 --advertise-addr 10.113.99.87:2377 --listen-addr 10.113.99.87:2377
docker swarm join --token $WORKER_TOKEN 10.113.99.167:2377 --advertise-addr 10.113.99.29:2377 --listen-addr 10.113.99.29:2377
```

Again, run `docker node ls`:

```
ID                            HOSTNAME   STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
t49oodaobyzvy5vfdbqowtcud *   mgr        Ready     Active         Leader           27.3.1
vab7ieegrgwujg7z5b13vudk3     wrk1       Ready     Active                          27.3.1
yitd50w3dal0pcl8si32dmyr6     wrk2       Ready     Active                          27.3.1
```

## Services

Create the service:

```sh
docker service create --name example-app -p 8080:80 --replicas 3 nginx:latest
```

The Docker client sent the command to a swarm manager and the leader deployed the 3 replicas across the swarm.

View all services:

```sh
docker service ls
```

View all service replicas and the state of each:

```sh
docker service ps
```

Scale:

```sh
docker service scale example-app=7
```

Delete:

```sh
docker service rm example-app
```

## Rollouts

Note: rollouts, updates and rolling updates are the same thing for us.

Rollout command:

```sh
docker service update --image $IMAGE:2.0.0 --update-parallelism 2 --update-delay 20s example-app
```

## Logs

Run:

```sh
docker service logs example-app
```

## Best Practices

- deploy an odd number of managers
- don't deploy too many managers (usually `3` or `5` is enough)

## Locking Swarms

TODO

## Swarm Networking

- overlay network
- service discovery (DNS)
- load balancer
- secure by default (TLS authentication + encryption enforced)

## Notes

Swarm cluster are HA (highly available), i.e. one or more managers can fail and the swarm will keep running.
Swarm implements active/passive multi-manager HA, i.e. a swarm will have one active manager and the other will be passive.
If the active manager (leader) fails, one of passive managers (followers) takes over.
