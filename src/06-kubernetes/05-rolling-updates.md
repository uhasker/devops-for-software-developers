# Rolling Updates

## A Rolling Update

Note that rollout, release, zero-downtime update mean the same thing here?

All update operations are actually replacement operations, i.e. when you update a Pod, you actually delete it and create a new one.
Pods are immutable objects, so you never change or update them after they're deployed.

Add an endpoint to `app.py`:

```python
@app.route('/date-ms', methods=['GET'])
def get_current_date_ms():
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    return {'current_date': current_date}
```

Rebuild the Dockerfile:

```sh
docker build -t date-app:2.0 .
```

Post the new file:

```sh
kubectl apply -f date-app.yml
```

## Settings of Rolling Updates

Reset the `app.py` file and reset `date-app` to `1.0` and apply the file.

Let's set:

- `revisionHistoryLimit` to 5 to keep the configs from the 5 previous release for easy rollbacks
- `progressDeadlineSeconds` to 300 (5 minutes) to give each new Pod five minutes to start
- `minReadySeconds` to 10 to wait 10 seconds between each replica (in the real world this should be large enough to catch common failures)

Now add the changes back to `app.py` file and set `date-app` to `2.0`.

We do this:

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
  revisionHistoryLimit: 5
  progressDeadlineSeconds: 300
  minReadySeconds: 10
  template:
    metadata:
      labels:
        app: date-app
    spec:
      containers:
        - name: date-app
          image: date-app:2.0
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8000
```

You can monitor the rollout with:

```sh
kubectl rollout status deployment date-app
```

You can see the history like this:

```sh
kubectl rollout history deployment date-app
```
