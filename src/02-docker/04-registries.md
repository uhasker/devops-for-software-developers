# Registries

## Login

Login to DockerHub:

```sh
docker login -u $USERNAME
```

At the password prompt, enter the personal access token.

## Pushing the Image

First, tag the image with the registry URL and the repository name:

```sh
docker tag example-app:1.0.0 $USERNAME/example-app:1.0.0
```

Next, push the tagged image:

```sh
docker push $USERNAME/example-app:1.0.0
```

## Pulling the Image

You can now pull the image the same way you would pull any other image:

```sh
docker pull $USERNAME/example-app:1.0.0
```
