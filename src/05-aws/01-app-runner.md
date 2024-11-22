# Deploying with App Runner

The simplest way to deploy something on AWS is by using App Runner.

## Login to AWS CLI

Login:

```sh
aws configure sso
```

## ECR

First, login to the Elastic Container Registry.

Next, create a repository.
Let's call it `example`.

Select `immutable` for image tags.

You can leave the encryption configuration at `AES-256`.

Finally, click "Create".

Retrieve an authentication token and authenticate your Docker client to your registry. Use the AWS CLI:

```sh
aws ecr get-login-password --region eu-central-1 --profile $PROFILE | docker login --username AWS --password-stdin 665359212466.dkr.ecr.eu-central-1.amazonaws.com
```

Let's build `app-example`:

```sh
docker build -t example .
```

Tag example:

```sh
docker tag example:latest 665359212466.dkr.ecr.eu-central-1.amazonaws.com/example:latest
docker push 665359212466.dkr.ecr.eu-central-1.amazonaws.com/example:latest
```

## App Runner

Select step 1:

- repository type > container registry
- provider > Amazon ECR
- copy container image URI
- deployment trigger > manual
- ECR access role > service role name (e.g. AppRunnerECRExampleAccessRole)

Select step 2:

- service name example
- 2 vCPU, 4 GB virtual memory
- port 443
- leave application command blank
- leave auto scaling
- leave health check
- networking > public endpoint
- outgoing > public endpoint

## ECS

- cluster > cluster name > EC2
- create new ASG
- on demand
- Amazon Linux 2
- t2.medium
- 1 to 3 capacity
- leave network settings
