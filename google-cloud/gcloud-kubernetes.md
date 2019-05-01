# Working with Google Kubernetes clusters

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

To create, using [kubectl run](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#run) a new **Deployment** <server> from the <app> container image on <port>

```sh
kubectl run <server> --image=gcr.io/google-samples/<app> --port <port>

# expect similar output
deployment.apps "<server>" created
```

To create a new **Service** to expose application to external traffic using [kubectl expose](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#expose)

```sh
kubectl expose deployment <server> --type="LoadBalancer"

# expect similar output
service "<server>" exposed
```

Inspect the **Service** using [kubectl get](https://kubernetes.io/docs/user-guide/kubectl/v1.9/#get)

```sh
kubectl get service <server>

# expect similar output
NAME           TYPE           ...   EXTERNAL-IP      PORT(S)          AGE
<server>       LoadBalancer   ...   35.184.112.169   8080:30840/TCP   2m
```