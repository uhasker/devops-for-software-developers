# Containers

Fundamentally, containers are a virtualization technology for running applications.

Don't think of containers as VMs, think of them as special processes instead.
This is because VM hypervisors perform hardware virtualization and so every new VM ships its own OS.
Containers share the OS, i.e. you install an engine on top of your OS and start containers.

## Starting a Container

Container are based on images.
We will discuss images on more detail in the next section, but basically they're blueprints for containers.

Let's start a container from the `nginx` image:

```sh
docker run -d --name example -p 8080:80 nginx
```

Let's have a closer look at the command:

- `docker run` tells Docker to run a new container
- `-d` tells Docker to run the container in the background as a daemon process
- `--name example` tells Docker to name this container `example`
- `-p 8080:80` maps port `8080` on your local system to port `80` inside of the container
- `nginx` tells Docker the name of the image to start a container from

Let's check that the container is running:

```sh
docker ps
```

The output is something like:

```
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS                                   NAMES
7b5a7dce6f39   nginx     "/docker-entrypoint.…"   4 minutes ago   Up 4 minutes   0.0.0.0:8080->80/tcp, :::8080->80/tcp   example
```

We can also verify our container is running by going to `http://localhost:8080`.

## Connecting to a Container

You can use `docker exec` to run a command in a running container:

```sh
docker exec example ps
```

This command can take additional flags, the most useful of which are `-i` and `-t`.
The `-i` (short for `--interactive`) flag will keep the container's STDIN open even if not attached.
This ensure that the process remains interactive, i.e. you can type and send commands to it.
The `-t` (short for `--tty`) will allocate a pseudo-TTY which makes Docker emulate a terminal session (providing features like line buffering and interactive command input).

Combining the flags allows you to start a `bash` shell inside a container.
This is a very powerful feature and allows you to debug problems of a running container very quickly:

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

However, most containers ship with a package manager, so you can install the tools you need.
For example, you can get the `ps` command by installing `procps`:

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

## Inspecting a Container

You can use `docker inspect` to inspect a container:

```sh
docker inspect example
```

This will print a lot of useful information about the container.

## Container Lifecycle

You can stop a container with `docker stop`:

```sh
docker stop example
```

It will no longer show up in `docker ps`, but you can still see all containers by passing the `-a` flag to `docker ps`:

```sh
docker ps -a
```

You can start the container again like this:

```sh
docker start example
```

You can also restart the container with `docker restart`.

Note that stopping a container won't lose changes that you've made inside the container.
Nevertheless, you should generally not make changes to a running container and treat containers as immutable objects instead.

You can remove a container like this:

```sh
docker stop example
docker rm example
```

## Container Logs

You can retrieve the logs of a container like this:

```sh
docker logs example
```

You can follow the logs by passing the `-f` flag:

```sh
docker logs -f example
```

## Restart Policies

Docker allows you to specify a restart policy.
The four main restart policies are:

- `no` (default, don't start container automatically)
- `always` (always restart a stopped container unless the container was stopped explicitly)
- `unless-stopped` (restart the container unless the container was in a stopped state before the Docker daemon was stopped)
- `on-failure` (restart the container if it exited with non-zero or if the Docker daemon restarts)
