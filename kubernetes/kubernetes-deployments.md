# Working with Kubernetes deployments

Deployments are a declarative way to ensure that the number of pods is as defined and drive current state towards desired state.

Deployments use Replica Sets [http://kubernetes.io/docs/user-guide/replicasets/] to manage starting and stopping the Pods

Using kustomization.yaml to deploy from current directory

```sh
kubectl apply -k ./
```

Delete entire deployement based on kustomization.yaml

```sh
kubectl delete -k ./
```

## Using kubectl to create and manage clusters

Deployments are the scaffolding of the cluster that keep the pods up even when the nodes they run on fail

To launch a single instance of nginx container

```sh
kubectl create deployment <name-nginx> --image=nginx:1.10.0
```

To expose a public IP to a container

```sh
# this creates an external Load Balancer with an external IP that will route traffic to the pods behind the service

kubectl expose deployment nginx --port 80 --type LoadBalancer
```
