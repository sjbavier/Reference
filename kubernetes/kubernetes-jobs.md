# Working with Kubernetes Job Objects

| Type                       | Use case                                               | Behavior                                                                           | completions | parallelism |
|----------------------------|--------------------------------------------------------|------------------------------------------------------------------------------------|-------------|-------------|
| One shot                   | database migrations                                    | a single pod running once until successful termination                             | 1           | 1           |
| Parallel fixed completions | multiple Pods processing a set of work in parallel     | one or more Pods running one or more times until reaching a fixed completion count | 1+          | 1+          |
| Work queue: parallel jobs  | multiple Pods processing from a centralized work queue | one or more Pods running once until successful termination                         | 1           | 2+          |

Example: One shot Job

```yaml
apiVersion: batch/v1
kind: Job
metadata:
   name: oneshot
spec:
   template:
   spec:
      containers:
      - name: kuard
      image: gcr.io/kuar-demo/kuard-amd64:blue
      imagePullPolicy: Always
      args:
      - "--keygen-enable"
      - "--keygen-exit-on-complete"
      - "--keygen-num-to-gen=10"
      restartPolicy: OnFailure
```

## Cron Jobs

Example of a cronjob that runs every 5 hours

```yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
   name: example-cron
spec:
   # Run every fifth hour
   schedule: "0 */5 * * *"
   jobTemplate:
      spec:
         template:
            spec:
               containers:
               - name: batch-job
               image: my-batch-image
               restartPolicy: OnFailure
```