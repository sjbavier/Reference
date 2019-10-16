# Working with Kubernetes DaemonSets

Similar to ReplicaSets, its important to understand that DaemonSets should be used when a single copy of your application must run on all or a subset of nodes in the cluster.

Unlike ReplicaSets, DaemonSets will create Pods on every node in the cluster by default unless a node selector is used.

Example DaemonSet

```yaml
apiVersion: extensions/v1beta1
kind: DaemonSet
metadata:
   name: fluentd
   labels:
      app: fluentd
spec:
   template:
   metadata:
      labels:
         app: fluentd
   spec:
      containers:
      - name: fluentd
         image: fluent/fluentd:v0.14.10
         resources:
            limits:
               memory: 200Mi
         requests:
            cpu: 100m
            memory: 200Mi
         volumeMounts:
         - name: varlog
            mountPath: /var/log
         - name: varlibdockercontainers
            mountPath: /var/lib/docker/containers
            readOnly: true
      terminationGracePeriodSeconds: 30
      volumes:
      - name: varlog
         hostPath:
            path: /var/log
      - name: varlibdockercontainers
         hostPath:
            path: /var/lib/docker/containers
```