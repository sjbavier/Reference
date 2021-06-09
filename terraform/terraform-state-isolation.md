# Isolation of State

There are two ways to isolate state files:

- Isolation via **workspaces**
- Isolation via file layout

## Isolation via workspaces

Terraform workspaces allow you to store Terraform state in multiple separate named workspaces. Terraform uses the default workspace if no workspace is defined.  These get stored in your state 'env' directory.  This essentially stores a new terraform.tfstate in a different directory so you may try some expiraments with a module you have already deployed by switching workspaces and deploying a new copy of the exact same infrastructure.

To show current workspace

```sh
terraform workspace show
```

To create a new workspace

```sh
terraform workspace new <name>
```

Show all workspaces

```sh
terraform workspace list
```

Switch to another workspace

```sh
terraform workspace select <name>
```

You may even want to change for example instance types when expiramenting in a new workspace.

Using the below code will use a t2.medium instance for default workspace and t2.micro for anything else:

```tf
resource "aws_instance" "example" {
   ami = "ami-0c55b159cbfafe1f0"
   instance_type = terraform.workspace == "default" ? "t2.medium" : "t2.micro"
}
```

> Workspaces are a great way to quickly spin up and tear down different versions of your code but they have a few drawbacks making them not ideal for production IAC.
>
> - The state files are stored inthe same backend or storage bucket.  Meaning that authentication and access controls are the same.  So they become unsuitable for isolating production from staging etc.
> - Workspaces are not visible in the code or terminal unless you run terraform workspace commands and thus maintenance becomes more difficult and less transparent.
> - Because of these workspaces are fairly error prone such as running terraform destroy accidentally in a production workspace instead of in the expiramental workspace. 

## Isolation via File Layout

To acheive isolation between environments you need to:

- put Terraform configuration files for each environment into a separate folder ie: staging environment in a directory called 'stage'
- configure different backend for each environment using different authentication mechanisms and access control.  Ie: each environment in a separate AWS account with separate S3 bucket backend

File structure example:

- stage
   - vpc
   - services
      - frontend-app
      - backend-app
         - var.tf
         - outputs.tf
         - main.tf
   - data-storage
      - mysql
      - redis
- prod
   - vpc
   - services
      - frontend-app
      - backend-app
   - data-storage
- mgmt
   - vpc
   - services
      - bastion-host
      - jenkins
- global
   - iam
   - s3

   