# Kubernetes

Kubernetes is an **orchestrator**, i.e. a system that deploys applications and dynamically responds to changes.

Deploying an application with Docker + Kubernetes has the following advantages compared to the simple setup from part I:

- applications can be automatically scaled up (or down) based on demand
- applications can self-heal when something breaks
- zero-downtime rolling updates and rollbacks can be performed

A Kubernetes **cluster** consists of one or more **nodes** that provide resources (CPU, memory, ...) for applications.
Basically, the nodes are the physical machines (e.g. an AWS or Hetzner instance or your local machine).

**Worker nodes** run applications, while **cluster nodes** implement the Kubernetes intelligence.

**Pods** are the basic Kubernetes units.
They wrap containers and execute on nodes.

## Creating a Kubernetes Cluster

Install Minikube and `kubectl`.

Next, start a Minikube cluster:

```sh
minikube start
```

Check the status of the cluster:

```sh
minikube status
```

## Deploying the Database

## Deploying the Date Service

Next let's create a directory `date-service`.
Create the following `app.py` file in it:

```python
from flask import Flask
from flask_cors import CORS

from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/date', methods=['GET'])
def get_current_date():
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return {'current_date': current_date}
```

Create a deployment file `date-service.yml` in `date-service`:

```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: date-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: date-service
  template:
    metadata:
      labels:
        app: date-service
    spec:
      containers:
        - name: date-service
          image: date-service:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8000

---
apiVersion: v1
kind: Service
metadata:
  name: date-service
spec:
  type: NodePort
  selector:
    app: date-service
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
      nodePort: 32000
```

Next, let's dockerize it.
Here is the `Dockerfile`:

```
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

Switch to Minikube's Docker environment:

```sh
eval $(minikube docker-env)
```

Go to `date-service` and build the Docker image:

```sh
cd date-service
docker build -t date-service .
```

Apply the manifest:

```sh
kubectl apply -f date-service.yml
```

Get the IP of the cluster:

```sh
minikube ip
```

You should be able to access the `date` route via the IP of the Minikube cluster.
For example, if the IP is `192.168.49.2`, then you should be able to do:

```console
$ curl http://192.168.49.2:32000/date
{"current_date":"2024-06-07 12:55:11"}
```

First, lets look at the pods:

```sh
kubectl get pods
```

You will see something like this:

```
NAME                           READY   STATUS    RESTARTS   AGE
date-service-f4ccc5779-4fvbq   1/1     Running   0          52s
date-service-f4ccc5779-69bqn   1/1     Running   0          52s
date-service-f4ccc5779-7qhw5   1/1     Running   0          52s
```

Let's look at the deployments:

```sh
kubectl get deployments
```

You will see something like this:

```
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
date-service   3/3     3            3           55s
```

Let's have a look at the services:

```sh
kubectl get services
```

You will see something like this:

```
NAME           TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
date-service   NodePort    10.104.148.100   <none>        80:31365/TCP   3m2s
kubernetes     ClusterIP   10.96.0.1        <none>        443/TCP        3m23s
```

##
