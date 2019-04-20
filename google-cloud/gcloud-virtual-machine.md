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