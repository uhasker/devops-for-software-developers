# Containers

Fundamentally, containers are a virtualization technology for running applications.

Don't think of container as VMs, think of them as special processes instead.
This is because VM hypervisors perform hardware virtualization and so every new VM ships its own OS.
With containers, you install an engine on top of your OS and then go from there.
Containers share the OS.

## Starting a Container

Start a container:

```sh
docker run -d --name example -p 8080:80 nginx
```

Let's have a closer look at the command:

- `docker run` tells Docker to run a new container
- `-d` tells Docker to run the container in the background as a daemon process
- `--name example` tells Docker to name this container `example`
- `p 8080:80` tells maps port `8080` on your local system to port `80` instead the container
- `nginx` tells Docker the name of the image to start a container from (we will cover images in a second, but basically they're blueprints for containers)

Let's check that the container is running:

```sh
docker ps
```

The output is something like:

```
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS                                   NAMES
7b5a7dce6f39   nginx     "/docker-entrypoint.…"   4 minutes ago   Up 4 minutes   0.0.0.0:8080->80/tcp, :::8080->80/tcp   example
```

We can also verify that this works by going to `http://localhost:8080`.

## Connecting to a Container

You can `docker exec` to connect to a container:

```sh
docker exec -it example /bin/bash
```

Try executing a few common Linux commands.
Note that not all of them will work because container images are usually optimized for being small and so often don't have all packages installed.

For example, the `nginx` container doesn't have the `ps` command:

```
root@7b5a7dce6f39:/# ps
bash: ps: command not found
```

You can however install `procps`:

```sh
apt update
apt install procps
```

Let's run `ps`:

```
root@7b5a7dce6f39:/# ps -ax
    PID TTY      STAT   TIME COMMAND
      1 ?        Ss     0:00 nginx: master process nginx -g daemon off;
     29 ?        S      0:00 nginx: worker process
     30 ?        S      0:00 nginx: worker process
     31 ?        S      0:00 nginx: worker process
     32 ?        S      0:00 nginx: worker process
     33 ?        S      0:00 nginx: worker process
     34 ?        S      0:00 nginx: worker process
     35 ?        S      0:00 nginx: worker process
     36 ?        S      0:00 nginx: worker process
     37 ?        S      0:00 nginx: worker process
     38 ?        S      0:00 nginx: worker process
     39 ?        S      0:00 nginx: worker process
     40 ?        S      0:00 nginx: worker process
     41 ?        S      0:00 nginx: worker process
     42 ?        S      0:00 nginx: worker process
     43 ?        S      0:00 nginx: worker process
     44 ?        S      0:00 nginx: worker process
    264 pts/0    Ss     0:00 /bin/bash
    270 pts/0    R+     0:00 ps -ax
```

We see that there is an `nginx` process running together with a bunch of worker processes.

You can also execute a command remotely without entering an interactive session:

```sh
docker exec example ps
```

## Inspecting a Container

You can use `docker inspect` to inspect a container:

```sh
docker inspect example
```

## Container Lifecycle

You can stop a container with `docker stop`:

```sh
docker stop example
```

It will no longer show up in `docker ps`, but you can do this:

```sh
docker ps -a
```

You can start the container again like this:

```sh
docker start example
```

You can also restart the container with `docker restart`.

Note that stopping a container won't lose changes that you've made inside the container (although you should not that nevertheless).

You can remove a container like this:

```sh
docker stop example
docker rm example
```
