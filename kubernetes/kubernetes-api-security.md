# Kubernetes API security best practices

from: [https://www.stackrox.com/post/2019/09/12-kubernetes-configuration-best-practices/#6-securely-configure-the-kubernetes-api-server]

run on master node

```sh
ps -ef | grep kube-apiserver
```

In the output, check to ensure that the:

```sh
--anonymous-auth
# argument shows as false. This setting ensures that requests not rejected by other authentication methods are not treated as anonymous and therefore allowed against policy. Disallowing anonymous requests can also prevent exploitation of CVE-2019-11253 and protect you against a “billion laughs” attack.

--basic-auth-file
# argument isn’t there. Basic auth uses plaintext credentials, instead of the preferred tokens or certificates, for authentication.

--insecure-allow-any-token
# argument isn’t there. This setting will ensure that only secure tokens that are authenticated are allowed.

-–kubelet-https
# argument either isn’t there or shows as true. This configuration ensures that connections between the API server and the kubelets are protected in transit via Transport Layer Security (TLS).

--insecure-bind-address
# argument isn’t there. This configuration will prevent the API Server from binding to an insecure address, preventing non-authenticated and unencrypted access to your master node, which minimizes your risk of attackers potentially reading sensitive data in transit.

--insecure-port
# argument shows as 0. This setting will prevent the API Server from serving on an insecure port, which would prevent unauthenticated and unencrypted access to the master node and minimize the risk of an attacker taking control of the cluster.

--secure-port
# argument either doesn’t exist or shows up as an integer between 1 and 65535. The goal here is to make sure all your traffic is served over https with authentication and authorization.

--profiling
# argument shows as false. Unless you’re experiencing bottlenecks or need to troubleshoot something that needs investigation, there’s no need for the profiler, and having it there unnecessarily opens you to exposure of system and program details.

--repair-malformed-updates
# argument shows as false. This setting will ensure that intentionally malformed requests from clients are rejected by the API Server.

--enable-admission-plugins
# argument is set with a value that doesn’t contain AlwaysAdmit. If you configure this setting to always admit, then it will admit requests even if they’re not explicitly allowed by the admissions control plugin, which would decrease the plugin’s effectiveness.

--enable-admission-plugins
# argument is set with a value that contains AlwaysPullImages. This configuration ensures that users aren’t allowed to pull images from the node to any pod by simply knowing the name of the image. With this control enabled, images will always be pulled prior to starting a container, which will require valid credentials.

--enable-admission-plugins
# argument is set with a value that contains SecurityContextDeny. This control ensures that you can’t customize pod-level security context in a way not outlined in the Pod Security Policy. See the Pod Security Policy section (2) for additional information on security context.

--disable-admission-plugins
# argument is set with a value that does not contain NamespaceLifecycle. You don’t want to disable this control, because it ensures that objects aren’t created in non-existent namespaces or in those namespaces set to be terminated.

--audit-log-path
# argument is set to an appropriate path where you want your audit logs to be stored. It’s always a good security practice to enable auditing for any Kubernetes components, when available, including the Kubernetes API server.

--audit-log-maxage
# argument is set to 30 or whatever number of days you must store your audit log files to comply with internal and external data retention policies.

--audit-log-maxbackup
# argument is set to 10 or any number that helps you meet your compliance requirements for retaining the number of old log files.


--audit-log-maxsize
# argument is set to 100 or whatever number that helps you meet your compliance requirements. Note that number 100 represents 100 MB.


--authorization-mode
# argument is there and is not set to AlwaysAllow. This setting ensures that only authorized requests are allowed by the API Server, especially in production clusters.


--token-auth-file
# argument is not there. This argument, when present, uses static token-based authentication, which have several security flaws; use alternate authentication methods instead, such as certificates.


--kubelet-certificate-authority
# argument is there. This setting helps prevent a man-in-the-middle attack when there’s a connection between the API Server and the kubelet.

--kubelet-client-certificate
--kubelet-client-key
# arguments are there. This configuration ensures that the API Server authenticates itself to the kubelet’s HTTPS endpoints. (By default, the API Server doesn’t take this step.)

--service-account-lookup
# argument is there and set to true. This setting helps prevent an instance where the API Server verifies only the validity of the authentication token without ensuring that the service account token included in the request is present in etcd.

--enable-admission-plugins
# argument is set to a value that contains PodSecurityPolicy. See above section on Pod Security Policies (2) for more details.

--service-account-key-file
# argument is there and is set to a separate public/private key pair for signing service account tokens. If you don’t specify public/private key pair, it will use the private key from the TLS serving certificate, which would inhibit your ability to rotate the keys for service account tokens.

--etcd-certfile
--etcd-keyfile
# arguments are there so that the API server identifies itself to the etcd server using client cert and key. Note that etcd stores objects that are likely sensitive in nature, so any client connections must use TLS encryption.

--disable-admission-plugins
# argument is set and doesn’t contain ServiceAccount. This configuration will make sure that when a new pod is created, it will not use a default service account within the same namespace.

--tls-cert-file
--tls-private-key-file
#arguments are there such that the API Server serves only HTTPS traffic via TLS.

--client-ca-file
# argument exists to ensure that TLS and client cert authentication is configured for Kube cluster deployments.

--etcd-cafile
# argument exists and it is set such that the API Server must verify itself to the etcd server via SSL Certificate Authority file.

--tls-cipher-suites
# argument is set in a way that uses strong crypto ciphers.

--authorization-mode
# argument is there with a value containing Node. This configuration limits which objects kubelets can read associated with their nodes.

--enable-admission-plugins
# argument is set and contains the value NodeRestriction. This plugin ensures that a kubelet is allowed to modify only its own Node API object and those Pod API objects associated to its node.

--encryption-provider-config
# argument is set to a EncryptionConfig file and this file should have all the needed resources. This setting ensures that all the REST API objects stored in the etcd key-value store are encrypted at rest.
# Make sure aescbc encryption provider is utilized for all desired resources as this provider of encryption is considered the strongest.

--enable-admission-plugins
# argument contains the value EventRateLimit to set a limit on the number of events accepted by the API Server for performance optimization of the cluster.

--feature-gates
# argument is not set with a value containing AdvancedAuditing=false. In other words, make sure advanced auditing is not disabled for auditing and investigation purposes.

--request-timeout
# argument is either not set or set to an appropriate value (neither too short, nor too long). Default value is 60 seconds.

--authorization-mode
# argument exists and is set to a value that includes RBAC. This setting ensures that Role-based access control (RBAC) is turned on. Beyond simply turning it on, you should follow several other recommendations for how to best use Kubernetes RBAC, including:

# Avoid giving users cluster-admin role because it gives very broad powers over the environment and should be used very sparingly, if at all.

# Audit your role aggregation rules to ensure you’re using them properly

# Don’t grant duplicated permissions to subjects because it can make access revocation more difficult
# Regularly remove unused Roles
```