# Working with Google Kubernetes clusters

## Creating and managing a GCloud cluster

Kubernetes Engine uses Kubernetes objects to create and manage your cluster's resources, [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) objects for stateless applications (ie: webservers) and [Service](https://kubernetes.io/docs/concepts/services-networking/service/) objects for defining load balancers and access rules.

Prior to making a cluster make sure you have your default zones/regions

To create a cluster (Cluster names must start with a letter, end with an alphanumeric, and cannot be longer than 40 characters. )

```sh
gcloud container clusters create <cluster-name>
```

To delete a cluster

```sh
gcloud container clusters delete <cluster-name>
```

After creating a cluster you must get the authentication credentials

```sh
gcloud container clusters get-credentials <cluster-name>
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
