# Working with Google Cloud

Create a VM instance **default** is Debian 9 (stretch) [https://cloud.google.com/compute/docs/images#debian] with unique name, machine type [https://cloud.google.com/compute/docs/machine-types] and zone specification [https://cloud.google.com/compute/docs/regions-zones/]

```sh
gcloud compute instances create <name> \
--machine-type <machine-type> \
--zone <zone>
```

Get help on the creation of instances

```sh
gcloud compute instances create --help
```

## Instance Templates

To use a startup script that is used by every VM instance

For example this script sets an Nginx server upon startup [startup.sh]

```sh
# this is a here document 
cat << EOF > startup.sh
#! /bin/bash
apt-get update
apt-get install -y nginx
service nginx start
sed -i -- 's/nginx/Google Cloud Platform - '"\$HOSTNAME"'/' /var/www/html/index.nginx-debian.html
EOF # designates end of file
```

To create an instance template that uses the startup script

```sh
gcloud compute instance-templates create <template-name> \
--metadata-from-file startup-script=startup.sh

# expect similar output
Created [...].
NAME              MACHINE_TYPE  PREEMPTIBLE CREATION_TIMESTAMP
<template-name>   n1-standard-1             2018-11-09T08:44:59.007-08:00
```

## Creating a target pool

To create a target pool that allows a single access point to all instances in a group, necessary for load balancing

```sh
gcloud compute target-pools create <name-of-pool>

# expect similar output
Created [...].
NAME              REGION       SESSION_AFFINITY BACKUP HEALTH_CHECKS
<name-of-pool>    us-central1
```

To create a managed instance group using the instance template

```sh
gcloud compute instance-groups managed create <group-name> \
--base-instance-name <name>
--size 2 \
--template <template-name>
--target-pool <name-of-pool>

# expect similar output
Created [...].
NAME         LOCATION       SCOPE  BASE_INSTANCE_NAME  SIZE  TARGET_SIZE  INSTANCE_TEMPLATE  AUTOSCALED
<group-name> us-central1-a  zone   <name>               0     2           <template-name>    no
```

To list the compute engine instances

```sh
gcloud compute instances list
```

Configure firewall to allow tcp traffic on port 80

```sh
gcloud compute firewall-rules create www-firewall --allow tcp:80
```
