# Working with GCloud network load balancers

```sh
google3098666_student@cloudshell:~ (qwiklabs-gcp-ab2a9361baf881e2)$ gcloud compute instances list
NAME        ZONE           MACHINE_TYPE   PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP    STATUS
nginx-jrdn  us-central1-a  n1-standard-1               10.128.0.2   35.226.228.21  RUNNING
nginx-mzp5  us-central1-a  n1-standard-1               10.128.0.3   35.238.174.15  RUNNING
```

```sh
google3098666_student@cloudshell:~ (qwiklabs-gcp-ab2a9361baf881e2)$ gcloud compute forwarding-rules list
NAME      REGION       IP_ADDRESS     IP_PROTOCOL  TARGET
nginx-lb  us-central1  35.224.61.212  TCP          us-central1/targetPools/nginx-pool
```

```sh
google3098666_student@cloudshell:~ (qwiklabs-gcp-ab2a9361baf881e2)$ gcloud compute http-health-checks create http-basic-check
Created [https://www.googleapis.com/compute/v1/projects/qwiklabs-gcp-ab2a9361baf881e2/global/httpHealthChecks/http-basic-check].
NAME              HOST  PORT  REQUEST_PATH
http-basic-check        80    /
```

```sh
google3098666_student@cloudshell:~ (qwiklabs-gcp-ab2a9361baf881e2)$ gcloud compute instance-groups managed \
> set-named-ports nginx-group \
> --named-ports http:80
Updated [https://www.googleapis.com/compute/v1/projects/qwiklabs-gcp-ab2a9361baf881e2/zones/us-central1-a/instanceGroups/nginx-group].
```

```sh
google3098666_student@cloudshell:~ (qwiklabs-gcp-ab2a9361baf881e2)$ gcloud compute backend-services create nginx-backend --protocol HTTP --http-health-checks http
-basic-check --global
Created [https://www.googleapis.com/compute/v1/projects/qwiklabs-gcp-ab2a9361baf881e2/global/backendServices/nginx-backend].
NAME           BACKENDS  PROTOCOL
nginx-backend            HTTP
```

```sh 
google3098666_student@cloudshell:~ (qwiklabs-gcp-ab2a9361baf881e2)$ gcloud compute url-maps create web-map --default-service nginx-backend
Created [https://www.googleapis.com/compute/v1/projects/qwiklabs-gcp-ab2a9361baf881e2/global/urlMaps/web-map].
NAME     DEFAULT_SERVICE
web-map  backendServices/nginx-backend
```

```sh 
google3098666_student@cloudshell:~ (qwiklabs-gcp-ab2a9361baf881e2)$ gcloud compute target-http-proxies create http-lb-proxy --url-map web-map
Created [https://www.googleapis.com/compute/v1/projects/qwiklabs-gcp-ab2a9361baf881e2/global/targetHttpProxies/http-lb-proxy].
NAME           URL_MAP
http-lb-proxy  web-map
```

```sh
google3098666_student@cloudshell:~ (qwiklabs-gcp-ab2a9361baf881e2)$ gcloud compute forwarding-rules create http-content-rule \
> --global \
> --target-http-proxy http-lb-proxy \
> --ports 80
Created [https://www.googleapis.com/compute/v1/projects/qwiklabs-gcp-ab2a9361baf881e2/global/forwardingRules/http-content-rule].
```

```sh
google3098666_student@cloudshell:~ (qwiklabs-gcp-ab2a9361baf881e2)$ gcloud compute forwarding-rules list
NAME               REGION       IP_ADDRESS      IP_PROTOCOL  TARGET
http-content-rule               35.244.173.176  TCP          http-lb-proxy
nginx-lb           us-central1  35.224.61.212   TCP          us-central1/targetPools/nginx-pool
```