# Images

Docker images are read-only templates with instructions for creating containers.
You can think of images as blueprints for containers.

## Pulling an Image

The easiest way to get image is to pull it from the official Docker registry.
Let's pull the `nginx` image for example:

```sh
docker image pull nginx
```

Let's show all images:

```sh
docker image ls
```

Assuming you only have the `nginx` image pulled, the output will be approximately as follows:

```
REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
nginx        latest    5ef79149e0ec   2 weeks ago     188MB
```

You can use the `-a` flag to show all images (including the intermediate layers) and the `-q` flag to only show image IDs.

## Inspecting an Image

Just as with container, you can inspect images using the `docker inspect` command:

```sh
docker inspect nginx
```

## Building an Image

> If you're following along in the web version, you can find the example at in the `examples/hello` directory in the accompanying GitHub repository.

Alternatively, you can build an image yourself.
For that, you'll need application code and a `Dockerfile`.

First, let's create a simple application `app.py`:

```python
print("Hello, World!")
```

Next, let's create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY . /app

CMD ["python", "app.py"]
```

We will cover Dockerfiles in more detail later, right now let's just build an image:

```sh
docker build -t hello .
```

As we already covered, you can run the container using the `docker run` command:

```sh
docker run hello
```

This container will simply print `Hello, World!` and then stop.

If you now run `docker image ls`, you will see the `hello` image as well (along with the `nginx` image we've pulled before):

```
REPOSITORY  TAG       IMAGE ID       CREATED         SIZE
hello       latest    78d35b56c06c   8 seconds ago   125MB
nginx       latest    5ef79149e0ec   2 weeks ago     188MB
```

## Image Tags

If you look at the `docker image ls` output, you will see that every image has a tag.
Note that by default images will be pulled and created with the `latest` tag.
However, you can change that by manually specifying a tag when pulling or creating an image using the `IMAGE:TAG` syntax.

For example, here is how you can pull the `nginx` image with tag `1.27.1`:

```sh
docker image pull nginx:1.27.1
```

And here is how you can create image with a tag:

```sh
docker build -t hello:1.0.0 .
```

Let's again run `docker image ls`, your output should show the two new images:

```
REPOSITORY  TAG       IMAGE ID       CREATED         SIZE
hello       latest    78d35b56c06c   4 minutes ago   125MB
hello       1.0.0     78d35b56c06c   4 minutes ago   125MB
nginx       1.27.1    5ef79149e0ec   2 weeks ago     188MB
nginx       latest    5ef79149e0ec   2 weeks ago     188MB
```

You should manually specify tags and never rely on the `latest` tag (since `latest` is just the last image that was created and you have no idea what that might be).
This goes for both building images and pulling images.

Tags should be in the SemVer (semantic versioning) format, i.e. `MAJOR.MINOR.PATCH`.
Sometimes it's useful to do `MAJOR.MINOR.PATCH-GITSHA` (since that ties the image directly to a specific version of the source code).

Once an image with a specific tag is pushed to a registry, you should also not overwrite it since that will lead to a lot of confusion.

From now on, we will always use specific tags and never rely on the `latest` tag.

## Removing Images

You can remove images using the `docker image rm` command.

> There is also `docker rmi` which is basically an alias for `docker image rm`.
> We will stick to `docker image rm` however since it neatly fits into the Docker command hierarchy.

For example, here is how we can remove the `example` image:

```sh
docker image rm example
```

If you want to remove all images, you can do:

```sh
docker image rm $(docker image ls -aq)
```

Note that you can't remove certain images (e.g. images of a running container).
If you still wish to do so, you can specify the `-f` flag when executing `docker image rm`.

## Layers

On a purely technical level, an image is nothing more than a collection of layers.
To better understand this process conceptually, we will rebuild the `hello` image without Docker BuildKit (because BuildKit introduces a lot of optimizations which will confuse us conceptually):

```sh
DOCKER_BUILDKIT=0 docker build -t hello:1.0.0 .
```

Let's now export the image as a tarball:

```sh
docker save -o hello_image.tar hello:1.0.0
```

Unpack the tarball:

```sh
tar -xvf hello_image.tar
```

Inside you'll find a `manifest.json` file that contains the layers:

```json
[
  {
    "Config": "blobs/sha256/bd936f5d46cf5977732cb6bd1e00e09b9c42675f51a2115cede89b22d603ac08",
    "RepoTags": ["hello:1.0.0"],
    "Layers": [
      "blobs/sha256/8d853c8add5d1e7b0aafc4b68a3d9fb8e7a0da27970c2acf831fe63be4a0cd2c",
      "blobs/sha256/fb5ccd0db472b0b9feb557d01e6c39097acc9ad1a502e1e6a29fde48d74eb7b0",
      "blobs/sha256/e228adf1886f79aec8c40dff455c30bab317b17ce3ae3dce4fea87d6f18687d2",
      "blobs/sha256/9e599118e168a6c61d9766a48fe656725ffdf0ab38d135d49abee6767213efc4",
      "blobs/sha256/61399dbf1da52f8ccb215425621f8d09e41a2166f3f49a992bb1da53188b64c8",
      "blobs/sha256/fb06e4157373373ad0eac405c0e3f78f77e90f7b0f98813825c80fac1620a979"
    ],
    "LayerSources": {
      "sha256:61399dbf1da52f8ccb215425621f8d09e41a2166f3f49a992bb1da53188b64c8": {
        "mediaType": "application/vnd.oci.image.layer.v1.tar",
        "size": 1536,
        "digest": "sha256:61399dbf1da52f8ccb215425621f8d09e41a2166f3f49a992bb1da53188b64c8"
      },
      "sha256:8d853c8add5d1e7b0aafc4b68a3d9fb8e7a0da27970c2acf831fe63be4a0cd2c": {
        "mediaType": "application/vnd.oci.image.layer.v1.tar",
        "size": 77832192,
        "digest": "sha256:8d853c8add5d1e7b0aafc4b68a3d9fb8e7a0da27970c2acf831fe63be4a0cd2c"
      },
      "sha256:9e599118e168a6c61d9766a48fe656725ffdf0ab38d135d49abee6767213efc4": {
        "mediaType": "application/vnd.oci.image.layer.v1.tar",
        "size": 5120,
        "digest": "sha256:9e599118e168a6c61d9766a48fe656725ffdf0ab38d135d49abee6767213efc4"
      },
      "sha256:e228adf1886f79aec8c40dff455c30bab317b17ce3ae3dce4fea87d6f18687d2": {
        "mediaType": "application/vnd.oci.image.layer.v1.tar",
        "size": 42818560,
        "digest": "sha256:e228adf1886f79aec8c40dff455c30bab317b17ce3ae3dce4fea87d6f18687d2"
      },
      "sha256:fb06e4157373373ad0eac405c0e3f78f77e90f7b0f98813825c80fac1620a979": {
        "mediaType": "application/vnd.oci.image.layer.v1.tar",
        "size": 4608,
        "digest": "sha256:fb06e4157373373ad0eac405c0e3f78f77e90f7b0f98813825c80fac1620a979"
      },
      "sha256:fb5ccd0db472b0b9feb557d01e6c39097acc9ad1a502e1e6a29fde48d74eb7b0": {
        "mediaType": "application/vnd.oci.image.layer.v1.tar",
        "size": 9551360,
        "digest": "sha256:fb5ccd0db472b0b9feb557d01e6c39097acc9ad1a502e1e6a29fde48d74eb7b0"
      }
    }
  }
]
```

Each layer introduces a filesystem diff.
You can see the diffs by inspecting the tarball located in `blobs/sha256`.

Let's look at the first layer:

```sh
tar -tf blobs/sha256/8d853c8add5d1e7b0aafc4b68a3d9fb8e7a0da27970c2acf831fe63be4a0cd2c
```

This will simply contain a regular Linux file system.

The penultimate layer contains the `app` directory:

```sh
tar -tf blobs/sha256/61399dbf1da52f8ccb215425621f8d09e41a2166f3f49a992bb1da53188b64c8
```

The output will be:

```sh
app/
```

Finally, we can have a look at the last layer:

```console
$ tar -tf blobs/sha256/fb06e4157373373ad0eac405c0e3f78f77e90f7b0f98813825c80fac1620a979
app/
app/Dockerfile
app/README.md
app/app.py
```

## Inspecting the File System

It's often helpful to inspect an image without creating a container from it (especially when your problem is that the created container crashes immediately).

You can use `docker create` to create a new container from a specified image without starting it:

```sh
docker container create
```

Find out the container ID with `docker ps`.
You can the use `docker container export` to export the created container's filesystem as a tar archive:

```sh
docker container export $CONTAINER_ID -o hello_fs.tar
```

You can now have a look at the archive to view the final filesystem of the image:

```sh
tar -tvf hello_fs.tar
```
