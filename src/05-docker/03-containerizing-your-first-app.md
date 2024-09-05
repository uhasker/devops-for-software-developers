# Containerizing Your First App

## An Example Dockerfile

Now that we know what images and containers are, we can containerize our first app!

These are the steps:

1. Write your application and create a list of dependencies
2. Create a Dockerfile that tells Docker how to build and run the app
3. Create an image using the Dockerfile
4. Run a container from the image

Here is an example Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN python -m pip install --no-cache-dir -r /src/requirements.txt

COPY ./app /src/app

EXPOSE 80

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

Let's go over the instructions step by step.

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
Note that it can be overridden.

A similar command is the `ENTRYPOINT` command which can't be easily overridden and will always run.

Finally, the `ENV` command can be used to set environment variables that will be available during the container runtime.
