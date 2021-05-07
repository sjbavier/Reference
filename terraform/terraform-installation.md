# Terraform installation

Download appropriate Terraform package from the Terraform homepage and make sure it is added to the PATH environment variable.

For mac:

```sh
brew install terraform
```

## AWS integration

Use IAM service to create a new user to acquire the Access Key ID and Secret Access Key.  Generally you will want to add your own policies or use the Managed Policies, most likely you will need the following:

- AmazonEC2FullAccess
- AmazonS3FullAccess
- AmazonDynamoDBFullAccess
- AmazonRDSFullAccess
- CloudWatchFullAccess
- IAMFullAccess

Add the credentials to these environment variables for terraform to access

```sh
export AWS_ACCESS_KEY_ID=<access-key-id>
export AWS_SECRET_ACCESS_KEY=<secret-access-key>
```

In addition to the environment variables Terraform supports the same authentication mechanisms as AWS CLI and SDK tools so it will be able to use $HOME/.aws/credentials which are automatically generated if you from configure with the AWS CLI.
