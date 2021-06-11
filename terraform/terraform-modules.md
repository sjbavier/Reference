# Using Terraform Modules

Modules are used in Terraform to keep your code DRY (Don't Repeat Yourself).  They are the key to writing reusable testable Terraform code.  

Example File Structure using modules:

- modules
  - services
    - webserver-cluster
      - vars.tf
      - outputs.tf
      - main.tf
      - user-data.sh
- stage
  - services
    - webserver-cluster
      - main.tf
  - data-stores
    - mysql
      - vars.tf
      - outputs.tf
      - main.tf
- prod
  - services
    - webserver-cluster
  - data-stores
    - mysql
      - vars.tf
      - outputs.tf
      - main.tf
- global
  - s3
    - outputs.tf
    - main.tf

The syntax for a module:

```tf
module "<NAME>" {
   source = "<SOURCE>"

   [CONFIG ...]
}
```

> - \<NAME\> is the identifier you can use to refer to the module e.g. web-service
> - \<SOURCE\> is the path where the module can be found e.g modules/services/webserver-cluster.
> - CONFIG consists of one or more arguments specific to the module

Continuing with the example code structure above, you can use the **modules/services/webserver-cluster** module (see: [webserver-cluster](https://github.com/brikis98/terraform-up-and-running-code/tree/master/code/terraform/04-terraform-module/module-example/modules/services/webserver-cluster)) in your staging directory (utilizing state isolation via file layout) 

example : **stage/services/webserver-cluster/main.tf** 

```tf
provider "aws" {
      region = "us-east-2"
   }
   module "webserver_cluster" {
      source = "../../../modules/services/webserver-cluster"
}
```
