# Working with Kubernetes extensions

There are many extensions available for kubernetes some that extend the api server, admission controllers, DaemonSets that automatically install loggin monitoring and scanning tools for your services for XSS vunerabilities and more.

( CustomeResourceDefinitions, Container Network Interfaces, Container Storage Interfaces, Container Runtime Interfaces )

API server request flow

User => Authentication/Authorization => Admission Control (validating, mutating) => API server => Storage

## Creating a CustomResourceDefinition

This resource is actually a meta-resource, a resource that is the definition of another resource

An example of a loadtest CustomResourceDefinition

```yaml
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
   # the name is unique and has to be in the following format <resource-plural>.<api-group>
   name: loadtests.beta.kuar.com
spec:
   # the api group and has to match the suffix of the CRD's name
   group: beta.kuar.com
   versions:
      - name: v1
         served: true
         storage: true
   scope: Namespaced
   names:
      # names for kubectl ie: kubectl get loadtests
      plural: loadtests
      singular: loadtest
      kind: LoadTest
      shortNames:
      - lt
```

This resource definition will refer to the following LoadTest resource. Further configuration is needed to do any type of loadtests

```yaml
apiVersion: beta.kuar.com/v1
kind: LoadTest
metadata:
   name: my-loadtest
spec:
   service: my-service
   scheme: https
   requestsPerSecond: 1000
   paths:
   - /index.html
   - /login.html
   - /shares/my-shares/
```
