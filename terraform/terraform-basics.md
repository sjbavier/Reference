# Basic Terraform commands

Upon starting a new project terraform will not have code for different providers such as AWS, Google Cloud Azure etc.  Create a simple main.tf file in the directory of the new project and add some code that defines a resource in a provider such as AWS.

Run the initialization command and Terraform will scan the file and download the appropriate provider code into the default .terraform folder (usually you'll add this to .gitignore). The init command can be run multiple times it is idempotent.

```sh
terraform init
```

The plan command gives you an output of any changes Terraform might do.  Its a great way to check before innacting any changes.

```sh
terraform plan
```

To apply the changes that terraform plan has deliniated:

```sh
terraform apply
```