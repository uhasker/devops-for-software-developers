# Volumes

You can store data in the read/write layer of the container, but if you want to persist data, you need volumes.

Volumes are independent objects not tied to the lifecycle of a container.

You create a volume, then create a container and finally mount the volume into the container.

## Creating a Volume

Let's create a new volume:

```sh
docker volume create examplevol
```

You can view all volumes by running:

```sh
docker volume ls
```

This will output:

```
DRIVER    VOLUME NAME
local     examplevol
```

We can also inspect the volume:

```sh
docker volume inspect
```

This will output:

```
[
    {
        "CreatedAt": "2024-09-06T09:31:45+02:00",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/examplevol/_data",
        "Name": "examplevol",
        "Options": null,
        "Scope": "local"
    }
]
```

There are three fields especially interesting here.

The `Driver` field specifies the storage backend for the volume.
Here we have `local` which means that we store the volum data on the local file system of the Docker host.
Other drivers include `nfs` for network file systems, cloud-specific drivers etc.

The `Scope` field specifies where the volume is available.
If it's `local` it's only available on the Docker host where it was created.
If it's `global` it's available across multi-host systems.

The `Mountpoint` tells you where the volume exists on the Docker host's filesystem.

## Using Volumes

Let's create a container from the `alpine` image and mount a volume `examplevol`:

```sh
docker run -it --name example --mount source=examplevol,target=/vol alpine
```

Let's add some data to the volume:

```sh
echo "Test" > /vol/test
```

You can inspect `/var/lib/docker/volumes/examplevol/_data/test` to see that the data is present on the host system.
Note that it's not recommend to manipulate the volume from the host system.

## Deleting a Volume

You can delete a volume like this:

```sh
docker volume rm examplevol
```

Pruning:

```sh
docker volume prune
```
