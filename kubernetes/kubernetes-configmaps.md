# Working with Kubernetes ConfigMaps

ConfigMap is a Kubernetes object that defines a small filesystem, or in other words a set of variables that can be used when defining the environment or commandline for your containers.

ConfigMaps are combined with the Pod right before it is run and must be encoded as UTF-8 **max size 1MB**.

There are 3 ways to use a ConfigMap
**filesystem:** You can mount a ConfigMap into a Pod. A file is created for each entry based on the key name.
**environment variable:** A ConfigMap can be used to dynamically set the value of an environment variable.
**command-line argument:** Kubernetes supports dynamically creating the command line for a container based on ConfigMap values.

Example containing all 3

```yaml
apiVersion: v1
kind: Pod
metadata:
   name: kuard-config
spec:
   containers:
      - name: test-container
         image: gcr.io/kuar-demo/kuard-amd64:blue
         imagePullPolicy: Always
         # command-line arguments can use the $(<env-var>) syntax
         command:
            - "/kuard"
            - "$(EXTRA_PARAM)"
         # environment variables referenced with valueFrom
         env:
            - name: ANOTHER_PARAM
               valueFrom:
               configMapKeyRef:
                  name: my-config
                  key: another-param
            - name: EXTRA_PARAM
               valueFrom:
               configMapKeyRef:
               name: my-config
               key: extra-param
         # filesystem method volume mounted in container /config
         volumeMounts:
            - name: config-volume
               mountPath: /config
   # filesystem method
   volumes:
   - name: config-volume
      configMap:
         name: my-config
restartPolicy: Never
```

## Creation

To create a ConfigMap

```sh
# Load from the file with the config data key the same as the filename.
kubectl create configmap --from-file=<filename>

# Load from the file with the secret data key explicitly specified.
kubectl create configmap --from-file=<key>=<filename>

# Load all the files in the specified directory where the filename is an acceptable key name.
kubectl create configmap --from-file=<directory>

# Use the specified key/value pair directly.
kubectl create configmap --from-literal=<key>=<value>
```