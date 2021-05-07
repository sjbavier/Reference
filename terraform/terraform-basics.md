# Basic Terraform commands

Upon starting a new project terraform will not have code for different providers such as AWS, Google Cloud Azure etc.  Create a simple main.tf file in the directory of the new project and add some code that defines a resource in a provider such as AWS.

Run the initialization command and Terraform will scan the file and download the appropriate provider code.

```sh
terraform init
```
