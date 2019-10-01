# Working with kubernetes objects

Everything contained in Kubernetes is represented by a RESTful resource.
Example: https://your-cluster.com/api/v1/namespaces/default/pods/my-pod is a representation of a pod in default namespace named my-pod

The kubectl command makes http requests to these URLs for access to the Kubernetes objects that reside at these paths.

## Setting context

Setting contexts based on namespaces

```sh
# set context with namespace
kubectl config set-context <context-name-set> --namespace=<namespace-context>
# set context with users
kubectl config set-context <context-name-set> --users=<users>
# set context with clusters
kubectl config set-context <context-name-set> --clusters=<clusters>
```

Using the defined context

```sh
# use defined context
kubectl config use-context <context-name-set>
```

## kubectl get

List all resources within current namespace

```sh
kubectl get <resource-name>
# more specifically
kubectl get <resource-name> <object-name>
```

To get more information use the -o flag

```sh
kubectl get -o <resource-name>
# View object as JSON
kubectl get -o json <resource-name>
# View object as YAML
kubectl get -o yaml <resource-name>
```

To remove the output headers

```sh
kubectl get --no-headers <resource-name>
```

To use JSONPath query language to select fields of output object

```sh
kubectl get pods <pod-name> -o jsonpath --template={.status.podIP}
```

## Detailed output using describe

```sh
kubectl describe <resource-name> <object-name>
```

## Creating, updating and destroying Kubernetes Objects

To **create** an object using a yaml file.  To **update** the object, its the same command.

```sh
kubectl apply -f obj.yaml
# to do a dry run
kubectl apply -f obj.yaml --dry-run
```

The apply command also records a history of previous configurations.  

```sh
# edit
kubectl apply -f obj.yaml edit-last-applied
# set
kubectl apply -f obj.yaml set-last-applied
# view
kubectl apply -f obj.yaml view-last-applied
```

The apply tool will only modify the objects if they are different from the current objects in the cluster.  If the objects already exist it will simply exit successfully.  You may repeatedly use apply to reconcile state

To make interactive edits use **edit** which will download the latest object and launch an interative editor

```sh
kubectl edit <resource-name> <object-name>
```

To **delete** an object

```sh
kubectl delete -f obj.yaml
# can delete an object using the resource type and name
kubectl delete <resource-name> <object-name>
```

## Labeling and Annotating Objects

Both labels and annotations allow for adding metadata to Kubernetes objects. However labels allow you to identify, select and operate on Kubernetes objects. Annotations are non-identifying

```sh
kubectl label <resource-name> <object-name> <label>=<value>
# example
kubectl label pods <pod-name> color=red
```

To overwrite a label you need to include the **--overwrite** flag

```sh
kubectl label pods <pod-name> color=blue --overwrite
```

To remove a label

```sh
kubectl label pods <pod-name> <label>-
# example
kubectl label pods <pod-name> color-
```

## Debugging

To see the logs for a running container

```sh
kubectl logs <pod-name>
# for pods with multiple containers
kubectl logs <pod-name> -c <container>
```

To execute an interactive bash shell

```sh
kubectl exec -it <pod-name> -- bash
```

To attach to the running process which will allow you to send to standard input

```sh
kubectl attach -it <pod-name>
```

To copy files to and from a container

```sh
# copy to local
kubectl cp <pod-name>:</path/to/remote/file> </path/to/local/file>
# copy to container
kubectl cp </path/to/local> <pod-name>:</path/to/remote/file>
```

If you want to securely tunnel traffic from the local machine to the pod.  Note that this enables traffic to pods that might not be exposed to the public network

To forward traffic from local port 8080 to remote container 80

```sh
kubectl port-forward <pod-name> 8080:80
```

To use a command similar to **top** on either nodes or pods

```sh
kubectl top nodes
kubectl top pods
```
