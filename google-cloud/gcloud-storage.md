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

List buckets

```sh
gsutil ls
gsutil ls gs://<unique-name>
```

Remove bucket

```sh
gsutil rb gs://<unique-name>
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

It is important to enable and configure Object Lifecycle Management with versioning [https://cloud.google.com/storage/docs/lifecycle]

Getting lifecycle configuration

```sh
gsutil lifecycle get gs://<bucket-name>
```

Setting lifecycle configuration with JSON file

```sh
gsutil lifecycle set <configuration-json> gs://<bucket-name>
```

To disable lifecycle management for a bucket set an empty configuration file

```sh
gsutil lifecycle set <configuration-json> gs://<bucket-name>
```

```json
{
  "lifecycle": {
    "rule": []
  }
}
```

## Using Customer Supplied Encryption Keys

You can create your own AES-256 base-64 key

```sh
python3 -c 'import base64; import os; print(base64.encodebytes(os.urandom(32)))'
# copy the output without the b' and the \n'
```

Check if an empty .boto file exists and if so create new base configuration

```sh
gsutil config -n
```

Open the .boto file and paste the python generated encryption key into the line below:

```conf
Before:
# encryption_key=
After:
encryption_key=tmxElCaabWvJqR7uXEWQF39DhWTcDvChzuCmpHe6sb0=
```

### Rotate the CSEK keys

Move the encryption key value to the decryption key value in the .boto file

```conf
Before:
encryption_key=2dFWQGnKhjOcz4h0CudPdVHLG2g+OoxP8FQOIKKTzsg=
# decryption_key1=
After:
# best practice: delete old encryption_key
# encryption_key=2dFWQGnKhjOcz4h0CudPdVHLG2g+OoxP8FQOIKKTzsg=
decryption_key1=2dFWQGnKhjOcz4h0CudPdVHLG2g+OoxP8FQOIKKTzsg=
```

generate another AES-256 base-64 key

```sh
python3 -c 'import base64; import os; print(base64.encodebytes(os.urandom(32)))'
# copy the output without the b' and the \n'
```

Copy the new key to the encryption_key value

```conf
Before:
# encryption_key=2dFWQGnKhjOcz4h0CudPdVHLG2g+OoxP8FQOIKKTzsg=
After:
encryption_key=HbFK4I8CaStcvKKIx6aNpdTse0kTsfZNUjFpM+YUEjY=
```

Rewrite the storage files with the new key

```sh
gsutil rewrite -k gs://<bucket-name>/file
```

Comment out the old decryption key

```conf
Before:
decryption_key1=2dFWQGnKhjOcz4h0CudPdVHLG2g+OoxP8FQOIKKTzsg=
After:
# decryption_key1=2dFWQGnKhjOcz4h0CudPdVHLG2g+OoxP8FQOIKKTzsg=
```