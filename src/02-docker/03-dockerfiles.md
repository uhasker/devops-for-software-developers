# Dockerfiles

## An Example Dockerfile

Now that we know what images and containers are, we can containerize our first app!
To do this, we need to write a `Dockerfile` which contains instructions on how to build an image.

These are the steps we need to take to containerize an application:

1. Write your application and create a list of dependencies
2. Create a Dockerfile that tells Docker how to build and run the app
3. Create an image using the Dockerfile
4. Run a container from the image

> > If you're following along in the web version, you can find the example at in the `examples/app-example` directory in the accompanying GitHub repository.

Let's say we have a simple FastAPI web app that has only the file `app/main.py`:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}
```

Here is an example Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN python -m pip install --no-cache-dir -r /src/requirements.txt

COPY ./app /src/app

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

You will also need a `requirements.txt` file:

```
fastapi[standard]==0.113.0
uvicorn==0.30.6
```

You can build the image like this:

```sh
docker build -t example-app:1.0.0 .
```

## Basic Instructions

Let's go over the most important basic instructions step by step.

The `FROM` instruction begins a new build stage and specifies the base image for the following instructions.
Therefore, every valid Dockerfile must start with a `FROM` instruction.

The `WORKDIR` instruction establishes the working directory for instructions like `RUN` or `CMD` that come after it in the Dockerfile.
If the specified WORKDIR doesn't exist, it will be created.

The `COPY` instruction transfers files or directories from a source and places them into the image's filesystem at a destination.
Files and directories can be copied from the build context, etc.

The `RUN` executes commands in a new layer on top of the current image and commits the result.

The `EXPOSE` instruction tells Docker that the container will listen on specified network ports during runtime.
You can define whether the port uses TCP or UDP, with TCP being the default if no protocol is specified.

Note that `EXPOSE` does not actually publish the port.
Instead, it serves as documentation for the image builder and the container user, indicating which ports are intended for publishing.
To publish a port when running the container, use the `-p` flag with `docker run`.

The `CMD` instruction sets the command to be executed when running a container from an image.
Note that it can be overwritten.

A similar command is the `ENTRYPOINT` command which can't be easily overridden and will always run.

Finally, the `ENV` command can be used to set environment variables that will be available during the container runtime.

## Labels

The `LABEL` instruction allows you to add metadata to the image.
A label is a key-value pair.
For example:

```Dockerfile
LABEL vendor="MyAwesomeCompany"
LABEL description="My awesome image"
```

The `LABEL` instruction is often used for versioning since (unlike tags) labels become part of the image:

```Dockerfile
LABEL version="1.0.0"
```

The OCI provides a set of suggested labels within the `org.opencontainers.image` namespace, most importantly:

- `org.opencontainers.image.created` for the date and time on which the image was built
- `org.opencontainers.image.authors` for the authors
- `org.opencontainers.image.version` for the version
- `org.opencontainers.image.title` for a human-readable title
- `org.opencontainers.image.description` for a human-readable description
