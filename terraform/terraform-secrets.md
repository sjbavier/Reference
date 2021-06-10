# Storing and utilizing secrets in Terraform

> **note:** secrets are always stored in terraform state, so proper state management is essential!

There are two options for storage:

- use Terraform data source to read the secrets from a secret store such as AWS Secrets Manager.  Input the secrets using AWS Secrets Manager UI and read the secret back using:
  -AWS Secrets Manager and the
  - aws_secretsmanager_secret_version data source (shown in thepreceding code)
  - AWS Systems Manager Parameter Store and theaws_ssm_parameter data source
  - AWS Key Management Service (AWS KMS) and theaws_kms_secrets data source
  - Google Cloud KMS and the google_kms_secret data source
  - Azure Key Vault and the azurerm_key_vault_secret data source
  - HashiCorp Vault and the vault_generic_secret data source

```tf
provider "aws" {
   region = "us-east-2"
}
resource "aws_db_instance" "example" {
   identifier_prefix = "terraform-up-and-running"
   engine = "mysql"
   allocated_storage = 10
   instance_class = "db.t2.micro"
   name = "example_database"
   username = "admin"
   password =
      data.aws_secretsmanager_secret_version.db_password.secret_string
}
data "aws_secretsmanager_secret_version" "db_password" {
   secret_id = "mysql-master-password-stage"
}
```

- use a option completely out of Terraform such as 1password, LastPass or OS X Keychain.

```tf
variable "db_password" {
   description = "The password for the database"
   type = string
}
```

And here is how you would set the TF_VAR_db_password environment variable for Linux/Unix/OSX

```sh
 export TF_VAR_db_password="<your-password"
 # note there is a space before export to prevent starage in bash history
terraform apply
```

A better way is to use a commandline-friendly secret store such as **pass** and use a subshell to securely read and pass the secret into an environment variable

```sh
export TF_VAR_db_password=$(pass database-password)
terraform apply
```