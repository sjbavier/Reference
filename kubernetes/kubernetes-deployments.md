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

To get more information on deployment object

```sh
kubectl explain deployment

# to see all fields use recursive option
kubectl explain deployment --recursive

# to access specific fields of deployment object using dot notation
kubectl explain deployment.metadata.name
```

To scale deployment by modifying replicas

```sh
kubectl scale deployment hello --replicas=5
```

## Rolling updates

Once you update the deployment, Kubernetes will begin rolling update

```sh
kubectl edit deployment <deployment-name>
# modify image: - production ? or useless reference?
```

Check the new entry in rollout history

```sh
kubectl rollout history <deployment-name>
```

Pause a rollout

```sh
kubectl rollout pause <deployment-name>
```

Resume a rollout

```sh
kubectl rollout resume <deployment-name>
```

Verify current state of a rollout

```sh
kubectl rollout status <deployment-name>

# can also verify this on pods directly
kubectl get pods -o jsonpath --template='{range .items[*]}{.metadata.name}{"\t"}{"\t"}{.spec.containers[0].image}{"\n"}{end}'
```

Undo a previous rollout

```sh
kubectl rollout undo  <deployment-name>
```

