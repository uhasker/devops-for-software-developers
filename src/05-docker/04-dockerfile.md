# Dockerfiles

Now that we know what images and containers are, we can containerize our first app!

These are the steps:

1. Write your application and create a list of dependencies
2. Create a Dockerfile that tells Docker how to build and run the app
3. Create an image using the Dockerfile
4. Run a container from the image

Here is an example Dockerfile:

```
FROM python:3.9-slim

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN python -m pip install --no-cache-dir -r /src/requirements.txt

COPY ./app /src/app

EXPOSE 80

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

- Cmd: specifies the default that should run when a container is started, can be overridden
- Entrypoint: specifies the command that always run when the container starts
