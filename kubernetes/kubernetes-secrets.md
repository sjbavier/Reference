# Working with Kubernetes Secrets

Kubernetes object solution for dealing with things like passwords, security tokens or other types of private keys are collectively called Secrets.

Secrets allow container images to be created without bundling sensitive data and are exposed to Pods via explicit declarations in the Pods manifests and the Kubernetes API.

**By default Kubernetes secrets are stored in plain text in the etcd storage for the cluster. Anyone who has cluster administration rights can read all secrets in the cluster.** This may not be sufficient security for your needs so recent updates include support for encrypting secrets with a user-supplied key, generally integrated into a cloud key store.  Additionally, most cloud key stores have integration with Kubernetes flexible volumes, enabling you to skip Kubernetes secrets entirely and rely on the cloud provider's key store.

Secrets hold one or more data elements as a collection of key/value pairs, secret data values hold arbitrary data encoded using base64 or binary **max size 1MB**.  Secrets can be exposed to Pods using the secrets volume type. They are managed by kubelet and created at Pod creation time, stored on tmpfs (RAM disks) and are not written to disk on nodes.

To create a secret via CLI using locally stored crt and key files

```sh
kubectl create secret generic example-tls \
--from-file=example.crt \
--from-file=example.key

# view details of what was created
kubectl describe secrets example-tls
# example output
Name: example-tls
Namespace: default
Labels: <none>
Annotations: <none>

Type: Opaque

Data
====
example.crt: 1050 bytes
example.key: 1679 bytes
```

**note: Secrets can be consumed using Kubernetes REST API by applications that know how to call the API directly.**  However for portability it is recommended to use a **secrets volume**.

Each data element of a secret is stored in a separate file under the target mount point specified in the volume mount.

Secret example:

```yaml
apiVersion: v1
kind: Pod
metadata:
   name: example-tls
spec:
   containers:
      - name: example-tls
         image: gcr.io/example-demo/example-amd64:blue
         imagePullPolicy: Always
         volumeMounts:
         - name: tls-certs
            mountPath: "/tls"
            readOnly: true
   volumes:
      - name: tls-certs
         secret:
            secretName: example-tls
```

If you have a private Docker registry you may create a **imagePullSecrets** to access during pod creation.

To create the Docker registry secret

```sh
kubectl create secret docker-registry my-image-pull-secret \
--docker-username=<username>
--docker-password=<passoword>
--docker-email=<email-address>
```

To utilize the Docker registry secret in yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
   name: kuard-tls
spec:
   containers:
      - name: kuard-tls
         image: gcr.io/kuar-demo/kuard-amd64:blue
         imagePullPolicy: Always
         volumeMounts:
         - name: tls-certs
            mountPath: "/tls"
            readOnly: true
   # here you spec out the Docker registry secret
   imagePullSecrets:
   - name: my-image-pull-secret
   volumes:
      - name: tls-certs
         secret:
            secretName: kuard-tls
```

## Creation

To create a secret

```sh
# Load from the file with the secret data key the same as the filename.
kubectl create secret generic --from-file=<filename>

# Load from the file with the secret data key explicitly specified.
kubectl create secret generic --from-file=<key>=<filename>

# Load all the files in the specified directory where the filename is an acceptable key name.
kubectl create secret generic --from-file=<directory>

# Use the specified key/value pair directly.
kubectl create secret generic --from-literal=<key>=<value>
```