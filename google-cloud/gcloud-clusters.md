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

# also can get login
gclooud auth application-default login
```
