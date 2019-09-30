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
