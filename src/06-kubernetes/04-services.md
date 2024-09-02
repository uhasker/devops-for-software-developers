# Services

We need a service to be able to connect to the app.

Here the `yml` file:

```yml
apiVersion: v1
kind: Service
metadata:
  name: date-service
spec:
  type: NodePort
  selector:
    app: date-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
      nodePort: 32000
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
