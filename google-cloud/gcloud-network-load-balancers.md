# Working with GCloud [network](https://cloud.google.com/compute/docs/load-balancing/network/) and [HTTP](https://cloud.google.com/compute/docs/load-balancing/http/) load balancers

Prerequisite: cluster of machines with a target pool, using a managed instance group

## Creating an L3 netword load balancer

List the compute engine instances

```sh
gcloud compute instances list

# Example output
NAME        ZONE           MACHINE_TYPE   PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP    STATUS
nginx-jrdn  us-central1-a  n1-standard-1               10.128.0.2   35.226.228.21  RUNNING
nginx-mzp5  us-central1-a  n1-standard-1               10.128.0.3   35.238.174.15  RUNNING
```

Configure firewall to allow tcp traffic on port 80

```sh
gcloud compute firewall-rules create www-firewall --allow tcp:80
```

To create an L3 network load balancer targeting your instance group

```sh
gcloud compute forwarding-rules create <name-of-load-balancer> \
--region <region> \
--ports=<port>
--target-pool <pool-name>
```

List all forwarding rules for your project

```sh
gcloud compute forwarding-rules list

# Example output
NAME           REGION       IP_ADDRESS     IP_PROTOCOL  TARGET
<pool-name>    <region>     35.224.61.212  TCP          <region>/targetPools/<pool-name>
```

## Creating an L7 HTTP Load Balancer

To create a [health check](https://cloud.google.com/compute/docs/load-balancing/health-checks) to verify that the instance is responding to HTTP or HTTPS traffic

```sh
gcloud compute http-health-checks create http-basic-check

# Example output
Created [https://www.googleapis.com/compute/v1/projects/qwiklabs-gcp-ab2a9361baf881e2/global/httpHealthChecks/http-basic-check].
NAME              HOST  PORT  REQUEST_PATH
http-basic-check        80    /
```

To define an HTTP service and map a port to a port name for instance group.

```sh
gcloud compute instance-groups managed \
set-named-ports <pool-name> \
--named-ports http:80

# Example output
Updated [https://www.googleapis.com/compute/v1/projects/qwiklabs-gcp-ab2a9361baf881e2/zones/us-central1-a/instanceGroups/nginx-group].
```

```sh
gcloud compute backend-services create nginx-backend --protocol HTTP --http-health-checks http
-basic-check --global

# Example output
Created [https://www.googleapis.com/compute/v1/projects/qwiklabs-gcp-ab2a9361baf881e2/global/backendServices/nginx-backend].
NAME           BACKENDS  PROTOCOL
nginx-backend            HTTP
```

```sh 
gcloud compute url-maps create web-map --default-service nginx-backend

# Example output
Created [https://www.googleapis.com/compute/v1/projects/qwiklabs-gcp-ab2a9361baf881e2/global/urlMaps/web-map].
NAME     DEFAULT_SERVICE
web-map  backendServices/nginx-backend
```

```sh 
gcloud compute target-http-proxies create http-lb-proxy --url-map web-map

# Example output
Created [https://www.googleapis.com/compute/v1/projects/qwiklabs-gcp-ab2a9361baf881e2/global/targetHttpProxies/http-lb-proxy].
NAME           URL_MAP
http-lb-proxy  web-map
```

```sh
gcloud compute forwarding-rules create http-content-rule \
> --global \
> --target-http-proxy http-lb-proxy \
> --ports 80

# Example output
Created [https://www.googleapis.com/compute/v1/projects/qwiklabs-gcp-ab2a9361baf881e2/global/forwardingRules/http-content-rule].
```

```sh
gcloud compute forwarding-rules list

# Example output
NAME               REGION       IP_ADDRESS      IP_PROTOCOL  TARGET
http-content-rule               35.244.173.176  TCP          http-lb-proxy
nginx-lb           us-central1  35.224.61.212   TCP          us-central1/targetPools/nginx-pool
```