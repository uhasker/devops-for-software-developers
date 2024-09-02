# Deployments

## Dockerization

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

Go to `date-app` and build the Docker image:

```sh
cd date-service
docker build -t date-app:1.0 .
```

## Deployment File

Create a deployment file `date-app.yml` in `date-app`:

```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: date-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: date-app
  template:
    metadata:
      labels:
        app: date-app
    spec:
      containers:
        - name: date-app
          image: date-app:1.0
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8000
```

The `metadata.name` field contains the name of the deployment.
This should always be a valid DNS name (i.e. only use alphanumerics, dot and dash).

The `spec` section is the most interesting section.

Here `spec.replicas` contains the number of Pod replicas to ask for.
The `spec.template` contains the definition of a Pod.
The `spec.selector` is a list of labels that Pods need to have to be managed.
Note that `spec.selector.matchLabels` should be the same as `spec.template.metadata.labels`?

TODO:

- revisionHistoryLimit
- progressDeadlineSeconds
- strategy

Apply the manifest:

```sh
kubectl apply -f date-app.yml
```

## Inspecting the Deployment

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

Inspect the deployment:

```sh
kubectl get deploy date-service
```

Inspect the deployment with describe:

```sh
kubectl describe deploy date-service
```

Output:

```
Name:                   date-service
Namespace:              default
CreationTimestamp:      Fri, 07 Jun 2024 15:38:55 +0200
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=date-service
Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=date-service
  Containers:
   date-service:
    Image:        date-service:latest
    Port:         8000/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   date-service-f4ccc5779 (3/3 replicas created)
Events:          <none>
```

We can also get the ReplicaSets:

```sh
kubectl get rs
```

Output:

```
NAME                     DESIRED   CURRENT   READY   AGE
date-service-f4ccc5779   3         3         3       79d
```
