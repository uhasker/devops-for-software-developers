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

## Building an Image

Alternatively, you can build an image yourself.
For that, you'll need application code and a `Dockerfile`.

First, let's create a simple application `app.py`:

```python
print("Hello, World!")
```

Next, let's create a `Dockerfile`:

```
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Run the Python script
CMD ["python", "app.py"]
```

We will cover Dockerfiles in more detail later, right now let's just build an image:

```sh
docker build -t example .
```

If you now run `docker image ls`, you will see the `example` image as well (along with the `nginx` image we've pulled before):

```
REPOSITORY  TAG       IMAGE ID       CREATED         SIZE
example     latest    78d35b56c06c   8 seconds ago   125MB
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
docker build -t example:v1 .
```

Let's again run `docker image ls`, your output should show the two new images:

```
REPOSITORY  TAG       IMAGE ID       CREATED         SIZE
example     latest    78d35b56c06c   4 minutes ago   125MB
example     v1        78d35b56c06c   4 minutes ago   125MB
nginx       1.27.1    5ef79149e0ec   2 weeks ago     188MB
nginx       latest    5ef79149e0ec   2 weeks ago     188MB
```

## Layers

On a purely technical level, an image is nothing more than a collection of layers.
We can view those layers using the `docker inspect` command.

For example, to view the layers of our `example:latest` image, we can do this:

```sh
docker inspect example:latest
```

Among other things, this will include the following output:

```
"RootFS": {
    "Type": "layers",
    "Layers": [
        "sha256:9853575bc4f955c5892dd64187538a6cd02dba6968eba9201854876a7a257034",
        "sha256:414698da489a5dd0db700cca4a87b7ca20dbc0fbefea813ca0bc9ff4f409e73f",
        "sha256:0900caae955e95ff03870e8180acee583299482dc1a9225429d9f897c753c0bf",
        "sha256:8657193c8651e10f63a6d1f63e23b736ed2905be949907750755e1f3357bc873",
        "sha256:d24f9dbb0a3ab7f7accbcf58fb79f7ba475e598a4c164ec1c569c48887f9ca94",
        "sha256:74ebc255d70104e40a6a2f9f89c7775b9bbe985f64761d7e15f80246df4341a1",
        "sha256:6bfd14ad8ccc8b286d3a639fb289f9470055fe73c562b0f7d0092d6d5501fe42"
    ]
}
```

The layers are sorted top to bottom, i.e. `9853...` is the base layer, followed by the layer `4146...` and so on.
If you're on a regular Linux system and you use the `overlay2` driver, you can find the actual files at `/var/lib/docker/image/overlay2/layerdb/sha256/...`.

For example, let's inspect the base layer of the `example:latest` image:

```sh
sudo ls /var/lib/docker/image/overlay2/layerdb/sha256/9853575bc4f955c5892dd64187538a6cd02dba6968eba9201854876a7a257034
```

Among other things, the output will show a `cache-id` file:

```
cache-id  diff	size  tar-split.json.gz
```

Let's look at it:

```sh
sudo cat /var/lib/docker/image/overlay2/layerdb/sha256/9853575bc4f955c5892dd64187538a6cd02dba6968eba9201854876a7a257034/cache-id
```

The result will be:

```
8c1792bbae4483c0a4b5664c5e9b5cda891f295399442b2a98474de7854ee257
```

Finally, we can inspect:

```sh
sudo ls /var/lib/docker/overlay2/8c1792bbae4483c0a4b5664c5e9b5cda891f295399442b2a98474de7854ee257
```

The output will be:

```
committed  diff  link
```

And the `diff` directory has the actual filesystem differences introduced by the layer.

## Official and Unofficial Images

It's worth knowing that some images are "official".

## Removing Images

You can remove images using the `docker rmi` command.
