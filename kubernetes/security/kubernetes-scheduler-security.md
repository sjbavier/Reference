# Kubernetes Scheduler Security Best Practices

From: [https://www.stackrox.com/post/2019/09/12-kubernetes-configuration-best-practices/#6-securely-configure-the-kubernetes-api-server]

run on the master node

```sh
ps -ef | grep kube-scheduler
```

Check following output parameters:

```sh
--profiling
# argument is set to false so that you have a reduced attack surface. While profiling can be useful when you have a performance bottleneck by identifying the bottleneck, it can also be exploited to reveal details about your system.
--address
# argument is set to 127.0.0.1 so that the scheduler is not bound to a non-loopback insecure address, since the scheduler API service is available without authentication or encryption.
```
