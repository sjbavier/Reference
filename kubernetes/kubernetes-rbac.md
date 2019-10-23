# Working with Kubernetes RBAC

**Note: anyone who can run arbitrary code inside the cluster can effectively obtain root privileges on the entire cluster.**
The correct RBAC setup can be part of the defense, but don't believe that RBAC by itself is sufficient to protect you.  You must isolate the Pods running in your cluster to provide multitenant security.  Generally this is done with a hypervisor isolated container and/or some sort of container sandbox.

**Authentication** with Kubernetes is generally performed by a third-party such as Azure Active Directory.
**Authorization** is determined by the identity of the user, the resource or HTTP path and the verb or action of the request.

1) User Identities - even a request with no identity falls under **system:unauthenticated**
2) Service Account Identities - 

## Roles and RoleBinding

Role resources are namespaced and cannot be used for non-namespaced resources. RoleBinding to a role only provides authorization within the namespace that contains both the Role and RoleDefinition.

Simple role example to create and modify Pods and Services:

```yaml
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
   namespace: default
   name: pod-and-services
rules:
- apiGroups: [""]
   resources: ["pods", "services"]
   verbs: ["create", "delete", "get", "list", "patch", "update", "watch"]
```

To bind this Role to user <user> and also bind to the group <group>:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
   namespace: default
   name: pods-and-services
subjects:
- apiGroup: rbac.authorization.k8s.io
   kind: User
   name: <user>
- apiGroup: rbac.authorization.k8s.io
   kind: Group
   name: <group>
roleRef:
   apiGroup: rbac.authorization.k8s.io
   kind: Role
   name: pod-and-services
```

## Kubernetes verbs

| Verb   | HTTP Method | Description                                           |
|--------|-------------|-------------------------------------------------------|
| create | POST        | create a new resource                                 |
| delete | DELETE      | delete an existing resource                           |
| get    | GET         | get a resource                                        |
| list   | GET         | list a collection of resources                        |
| patch  | PATCH       | modify an existing resource via a partial change      |
| update | PUT         | modify an existing resource via a complete object     |
| watch  | GET         | watch for streaming updates to a resource             |
| proxy  | GET         | connect to a resource via a streaming WebSocket proxy |

## Using built-in roles

To get a list of built-in roles

```sh
kubectl get clusterroles
```

| role          | description                                        |
|---------------|----------------------------------------------------|
| cluster-admin | provides complete access to the entire cluster     |
| admin         | provides complete access to a complete namespace   |
| edit          | allows an end user to modify things in a namespace |
| view          | allows for read-only access to a namespace         |

To view these role-bindings

```sh
kubectl get clusterrolebindings
```

## Testing Authorization

Use auth can-i

```sh
kubectl auth can-i create pods
kubectl auth can-i get pods --subresource=logs # test whether you can access subresources like logs
```

Reconcile works somewhat like the kubectl apply method

```sh
kubectl auth reconcile -f <rbac-config.yaml>
```

## Aggregating ClusterRoles

To define roles that are combinations of other roles use aggregation rules

## Groups

```yaml
...
subjects:
- apiGroup: rbac.authorization.k8s.io
   kind: Group
   name: my-great-groups-name
...
```

