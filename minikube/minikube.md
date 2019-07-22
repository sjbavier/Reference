# Working with minikube

Start minikube

```sh
minikube start # generic start
minikube start -p <name> # start minikube with named cluster
```

Delete minikube

```sh
minikube delete
```

Launch minikube dashboard

```sh
minikube dashboard
```

Get the url of the exposed service

```sh
kubectl get services
# example output
NAME              TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes        ClusterIP      10.96.0.1       <none>        443/TCP        10d
wordpress         LoadBalancer   10.99.135.193   <pending>     80:31509/TCP   5d22h
wordpress-mysql   ClusterIP      None            <none>        3306/TCP       5d22h

minikube service <service-name> --url
```
