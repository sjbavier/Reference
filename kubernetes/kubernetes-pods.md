# Working with kubernetes pods

Pods hold a collection of one or more containers generally if you have multiple containers with hard dependency on each other you package the containers in a single pod

**Pod - Logical Application** = 1 or more containers and shared volumes( GCE, iSCSI, NFS ), shared namespaces, 1 IP per pod

Creating pods with yaml configuration files

```sh
kubectl create -f <path-to-yaml-file>
```

To label pods

```sh
kubectl label pods <pod-name> 'secure=enabled'
kubectl get pods <pod-name> --show-labels # check the labels to see if they have updated
```

To view all pods

```sh
kubectl get pods

kubectl get pods -l "app=<name>,secure=enabled" # get all pods by label
```

To get more information about the pod

```sh
kubectl describe pods <pod-name>
```

Get secrets

```sh
kubectl get secrets
```

Get persistent volumes

```sh
kubectl get pvc
```

By default pods are allocated a **private IP address and cannot be reached outside the cluster**

To map a local port to a port inside the pod

```sh
kubectl port-forward <pod-name> <cluster-port>:<pod-port>

# snippet to grab the JWT from a login
TOKEN=$(curl https://127.0.0.1:<cluster-port>/login -u user|jq -r '.token')
# and then use it to access
curl -H "Authorization: Bearer $TOKEN" https://127.0.0.1:<cluster-port>/secure
```

To view the logs for a pod

```sh
kubectl logs <pod-name>
# stream the logs real-time
kubectl logs -f <pod-name>
```

To run an interactive shell session inside a pod

```sh
kubectl exec <pod-name> --stdin --tty -c <pod-name> /bin/sh
```

Get simple diagnostics for the cluster

```sh
kubectl get componentstatuses
```

