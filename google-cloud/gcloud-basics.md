# Working with gcloud CLI

Ask for help

```sh
gcloud -h # usage guidelines
gcloud config --help # can be used with any gcloud command
```

Get the active account for the Cloud Shell session

```sh
gcloud auth list

# output
ACTIVE  ACCOUNT
*       gcpstaging23396_student@qwiklabs.net
To set the active account, run:
    $ gcloud config set account <account>
```

List the project ID

```sh
gcloud config list project

# output
[core]
project = <project_ID>
```

Listing config options

```sh
gcloud config list
gcloud config list --all
```

## Regions and Zones

Certain Compute Engine resources live in regions or zones. Regions are geographical location which are divided into 1 or more zones.
For example: **us-central1** is the zone and **us-central1-a** is the region.

| Wester US  | Central US    | Eastern US    | Western Europe | Eastern Asia |
|------------|---------------|---------------|----------------|--------------|
| us-west1-a | us-central1-a | us-eastern1-b | europe-west1-b | asia-east1-a |
| us-west1-b | us-central1-b | us-eastern1-c | europe-west1-c | asia-east1-b |
|            | us-central1-c | us-eastern1-d | europe-west1-d | asia-east1-c |
|            | us-central1-f |               |                |              |

To set the default regions and zones of **gcloud**

```sh
gcloud config set compute/region <region>

gcloud config set compute/zone <zone>
```

To SSH into your gcloud instance

```sh
gcloud compute ssh <name-of-instance> \
--zone <zone> # optional if you have set this globally
```