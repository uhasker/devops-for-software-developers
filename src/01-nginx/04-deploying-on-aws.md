# Deploying on AWS

## Create an Instance

Launch an EC2 instance:

- give it a name, e.g. `example`
- select an OS image, e.g. Debian
- select an instance type, e.g. `t2.medium`
- generate a key pair, e.g. `example-rsa`
- create a security group that allows ssh, http and https traffic from anywhere
- configure 128GB of `gp3` storage

Download the key and ssh:

```sh
ssh -o PubkeyAuthentication=yes -o PasswordAuthentication=no -o IdentitiesOnly=yes -i example-rsa.pem admin@18.197.51.187
```

## Configure a Target Group

Create a target group that targets an instance:

- name `example`
- choose HTTP+80
- add the VPC (vpc-0d3e9aea031aa41e3) of your instance
- select HTTP1 as the protocol version
- configure HTTP and `/` as the health check path+protocol
- register `example` on the next page

## Configure Load Balancer

- name `example`
- choose Application Load Balancer
- set scheme to internet fcing, IP to IPv4
- networking mapping to VPC + availability zones 2
- leave security groups as is
- forward traffic to `example` target group

## Get certificte from CM

- FQDN example.titanom.com
- DNS validtion
- RSA 2048

## Domain

- create CNAME record
