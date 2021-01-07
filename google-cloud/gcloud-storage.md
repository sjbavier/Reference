# Working with Google Cloud Storage

## Using the gsutil

**gsutil** is used to create and delete buckets and objects, moving storage data and managing bucket and object ACLs.

```sh
gsutil mb gs://<unique-name> # make bucket
```

To copy data to the bucket from gcloud

```sh
gsutil cp data.dat gs://<unique-name>
```

## ACLs

Make all files in a directory public readable

```sh
# -m multi-threaded -R recursive -a all versions
gsutil -m acl set -R -a public-read gs://<bucket-name>/<directory>
```

## Version control

To enable version control [https://cloud.google.com/storage/docs/using-object-versioning#gsutil]

```sh
gsutil versioning set on gs://<bucket-name>
```

To disable version control

```sh
gsutil versioning set off gs://<bucket-name>
```

Check versioning status

```sh
gsutil versioning get gs://<bucket-name>
```
