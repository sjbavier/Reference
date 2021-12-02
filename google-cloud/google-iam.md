# Working with IAM

Generate a service account key file

```sh
gcloud iam service-accounts keys create <file.json> --iam-account=<sa-email>
```

List all keys associated with a Service Account:

```sh
gcloud iam service-accounts keys list --iam-account <user@email.com>
```

Activate service account with key file in json format

```sh
gcloud auth activate-service-account <service-account> --key-file <file.json>
```
