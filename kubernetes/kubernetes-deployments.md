# Working with Kubernetes deployments

Deployments are a declarative way to ensure that the number of pods is as defined and drive current state towards desired state.

Deployments use Replica Sets [http://kubernetes.io/docs/user-guide/replicasets/] to manage starting and stopping the Pods

Using kustomization.yaml to deploy from current directory

```sh
kubectl apply -k ./
```

Delete entire deployment based on kustomization.yaml

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

To delete a deployment

```sh
kubectl delete deployments <name>
# use the declarative form
kubectl delete -f <deployment.yaml>

## Rolling updates (RollingUpdate) strategy

This Deployment strategy works by updating a few Pods at a time and incrementally updating until all Pods are running the new version.  This also means that for a period of time your application will be running both versions

```yaml
apiVersion: apps/v1 # for versions before 1.9.0 use apps/v1beta2
kind: Deployment
metadata:
  ...
spec:
  ...
  minReadySeconds: <num-seconds> # The amount of time for the pod to be running to be considered healthy
  progressDeadlineSeconds: <num-seconds> # if any stage of the rollout failes to progress in X amount of seconds, consider the rollout failed.
  strategy:
    type: RollingUpdate
    revisionHistoryLimit: 14 # to limit the size of the Deployment object itself, set a number of revisions to keep in history
    maxUnavailable: <num-pods-allowed-unavailable>
    maxSurge: <num-pods-allowed-surplus>
```

Once you update the deployment, Kubernetes will begin rolling update

```sh
kubectl edit deployment <deployment-name>
# modify image: - production ? or useless reference?
```

Check the new entry in rollout history

```sh
kubectl rollout history <deployment-name>
kubectl rollout history <deployment-name> --revision=<revision-number> # view detailed information on specific rollout
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

## Recreate strategy (Recreate)

This is the simpler of the two deployment strategies.  Applying this will simply updated the ReplicaSet it manages to use the new image and terminates the existing Pods.  This has one major drawback, it will almost certainly result in some site downtime.

```yaml
apiVersion: apps/v1 # for versions before 1.9.0 use apps/v1beta2
kind: Deployment
metadata:
  ...
spec:
  ...
  strategy:
    type: Recreate
```

## Canary Deployments

A separate deployment with your new version and a service that targets both the normal stable deployment as well as canary  deployment

Modify the yaml file to reflect the track of canary and creating the 'canary' deployment alongside the stable.

```sh
kubectl create -f deployments/hello-canary.yaml
```

Portion of yaml file shown:

```yaml
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: hello
        track: canary
        version: 2.0.0
```

To verify that a subset of requests are being routed to canary deployment run this several times per example:

```sh
curl -ks https://`kubectl get svc frontend -o=jsonpath="{.status.loadBalancer.ingress[0].ip}"`/version
```

**PRODUCTION** In order to not have adverse user/client interactions from switching from one deployment to another you can use sessionAffinity field and set to ClientIP

```yaml
kind: Service
apiVersion: v1
metadata:
  name: "hello"
spec:
  sessionAffinity: ClientIP
  selector:
    app: "hello"
  ports:
    - protocol: "TCP"
      port: 80
      targetPort: 80
```

## Blue-green Deployments

This type of deployment is acheived by creating two separate deployments, one for the old 'blue' and one for the new 'green' version.   Once the 'green' version is up and running you switch over by updating the service.
**you'll need twice the resources to provision such a change in your application**

Essentially you'll be creating both blue and green deployments with different versions.  When new green deployment is verified as running properly, modify the service to reflect the proper selection.

First expose the blue service

```sh
kubectl apply -f services/hello-blue.yaml
```

Create the new green deployment

```sh
kubectl create -f deployment/hello-green.yaml
```

Verify the correct green deployment version is correct

```sh
curl -ks https://`kubectl get svc frontend -o=jsonpath="{.status.loadBalancer.ingress[0].ip}"`/version
```

Update the service to point to the new version

```sh
kubectl apply -f services/hello-green.yaml
```

**For a blue-green rollback** Since both deployments are running, simply apply the blue service

```sh
kubectl apply -f services/hello-blue.yaml
```
