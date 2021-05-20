# Working with Terraform State Management

For various reasons including manual error, locking, and secrets it is recommended to set up remote state storage on a cloud provider (AWS, Google, DigitalOcean, Azure).

The first step is to create a bucket; this is an AWS example with an S3 bucket.

Next make a main.tf, in a directory different from the configurations and specify the AWS.

```tf
provider "aws" {
   region = "us-east-2"
}
```

```tf
resource "aws_s3_bucket" "terraform_state" {
   bucket = "terraform-up-and-running-state"
   # Prevent accidental deletion of this S3 bucket
   lifecycle {
      prevent_destroy = true
   }
   # Enable versioning so we can see the full revision history of our
   # state files
   versioning {
      enabled = true
   }
   # Enable server-side encryption by default
   server_side_encryption_configuration {
   rule {
      apply_server_side_encryption_by_default {
         sse_algorithm = "AES256"
      }
   }
}
```

Next use a DynamoDB table for locking, it is Amazon's distributed key-value supporting consistent reads and conditional writes.  To utilize DynamoDB locking with Terraform you must provide a table with a primary key called LockID with this exact spelling and captialization.

```tf
resource "aws_dynamodb_table" "terraform_locks" {
   name = "terraform-up-and-running-locks"
   billing_mode = "PAY_PER_REQUEST"
   hash_key = "LockID"
   attribute {
      name = "LockID"
      type = "S"
   }
}
```

Then initialize terraform to download the provider code and then apply to deploy.  (you will need the IAM User to have permissions to create S3 buckets and DynamoDB tables)

```sh
terraform init
terraform apply
```

---

To utilize the new S3 bucket state storage you will need to add a backend configuration to Terraform.

```tf
terraform {
   backend "<BACKEND_NAME>" {
      [CONFIG...]
   }
}
```

**Note: backend blocks cannot use variables or references!**

```tf
terraform {
   backend "s3" {
      # Replace this with your bucket name!
      bucket = "terraform-up-and-running-state"
      key = "global/s3/terraform.tfstate"
      region = "us-east-2"
      # Replace this with your DynamoDB table name!
      dynamodb_table = "terraform-up-and-running-locks"
      encrypt = true
   }
}
```

The better way to allow for configuration in modules is to set a **backet-config** argument in the terraform init command

```sh
terraform init -backend-config=backend.hcl
```

Taking advantage of partial configurations.
**backend.hcl**

```tf
bucket = "terraform-up-and-running-state"
region = "us-east-2"
dynamodb_table = "terraform-up-and-running-locks"
encrypt = true
```

```tf
# Partial configuration. The other settings (e.g., bucket, region) will be
# passed in from a file via -backend-config arguments to 'terraform init'
terraform {
   backend "s3" {
      key = "example/terraform.tfstate"
   }
}
```

Or use **Terragrunt** for backend configuration
