# Using kubectl to create and manage services

**Services provide stable endpoints for Pods called Labels** whose IP addresses could readily change

The level of access a service provides a set of pods depends on the service's type

1. **ClusterIP** (internal)- the default type means that this service is only visible inside the cluster
2. **NodePort**- gives each node in the cluster an externally accessible IP
3. **LoadBalancer**- adds a load balancer from the cloud provider which forwards traffic from the service to Nodes within it

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

Listing services

```sh
kubectl get services
```

Describe services

```sh
kubectl describe services <service-name>
```

## Working with secret generic

Examples using yaml

```sh
kubectl create secret generic tls-certs --from-file tls/
```

```yaml
  volumes:
    - name: "tls-certs"
      secret:
        secretName: "tls-certs"
    - name: "nginx-proxy-conf"
      configMap:
        name: "nginx-proxy-conf"
        items:
          - key: "proxy.conf"
            path: "proxy.conf"

```

```sh
kubectl create configmap nginx-proxy-conf --from-file nginx/proxy.conf
```

```yaml
      volumeMounts:
        - name: "nginx-proxy-conf"
          mountPath: "/etc/nginx/conf.d"
        - name: "tls-certs"
          mountPath: "/etc/tls"
```

```sh
curl -ks https://`kubectl get svc frontend -o=jsonpath="{.status.loadBalancer.ingress[0].ip}"`
```

Per orchestrate example:

```sh
kubectl create secret generic tls-certs --from-file tls/
kubectl create configmap nginx-frontend-conf --from-file=nginx/frontend.conf
kubectl create -f deployments/frontend.yaml
kubectl create -f services/frontend.yaml
```


Endpoints are a low level way of finding what a service is sending traffic to
You can watch a service for any changes

```sh
kubectl get endpoints <service-name> --watch
```

## Readiness Checks

A service object has the built ability to track which pods are ready via the readiness check.

An implementation example below:

```yaml
spec:
   ...
   template:
      ...
      spec:
      containers:
         ...
         name: alpaca-prod
         readinessProbe:
            httpGet:
               path: /ready
               port: 8080
            periodSeconds: 2 # check every 2 seconds
            initialDelaySeconds: 0 # start checking immediately after the pod is instantiated
            failureThreshold: 3 # if it fails 3 times, pod is not ready
            successThreshold: 1 # 1 success deams the pod ready
```
