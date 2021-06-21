# Using Terraform Modules

Modules are used in Terraform to keep your code DRY (Don't Repeat Yourself).  They are the key to writing reusable testable Terraform code.  

> note: whenever you add a module or update the source parameter of a module you need to run **init** before running **plan** **apply**

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

## Input Variables

Modules are used to scaffold out common pieces of infrastructure.  The general pattern is to use input variables in the module's main.tf file in place of values; then from the development/staging/production directories you can pass values within that definition.

For example: 
Define the variables and types for the module **modules/services/webserver-cluster/variables.tf**

```tf
variable "instance_type" {
   description = "The type of EC2 Instances to run (e.g. t2.micro)"
   type = string
}
variable "min_size" {
   description = "The minimum number of EC2 Instances in the ASG"
   type = number
}
variable "max_size" {
   description = "The maximum number of EC2 Instances in the ASG"
   type = number
}
```

Next utilize the variables within the module **modules/services/webservercluster/
main.tf**

```tf
resource "aws_launch_configuration" "example" {
   image_id = "ami-0c55b159cbfafe1f0"
   instance_type = var.instance_type
   security_groups = [aws_security_group.instance.id]
   user_data = data.template_file.user_data.rendered
   # Required when using a launch configuration with an auto scaling group.
   # https://www.terraform.io/docs/providers/aws/r/launch_configuration.html
   lifecycle {
      create_before_destroy = true
   }
}

resource "aws_autoscaling_group" "example" {
   launch_configuration = aws_launch_configuration.example.name
   vpc_zone_identifier = data.aws_subnet_ids.default.ids
   target_group_arns = [aws_lb_target_group.asg.arn]
   health_check_type = "ELB"
   min_size = var.min_size
   max_size = var.max_size
   tag {
      key = "Name"
      value = var.cluster_name
      propagate_at_launch = true
   }
}
```

Now you can utlize the module and pass values: **stage/services/webserver-cluster/main.tf**

```tf
module "webserver_cluster" {
   source = "../../../modules/services/webserver-cluster"
   cluster_name = "webservers-stage"
   db_remote_state_bucket = "(YOUR_BUCKET_NAME)"
   db_remote_state_key = "stage/data-stores/mysql/terraform.tfstate"
   instance_type = "t2.micro"
   min_size = 2
   max_size = 2
}
```

## Module locals

Module locals are a nice way to use repeated values or even some intermediary calculated values locally without the need to expose the variable for configurable input.

Within the modules main.tf file you may want to consolidate typical values:  **modules/services/webserver-cluster/main.tf**
the syntax is local.\<NAME\>

```tf
// define the locals
locals {
   http_port = 80
   any_port = 0
   any_protocol = "-1"
   tcp_protocol = "tcp"
   all_ips = ["0.0.0.0/0"]
}
// use them locally
resource "aws_security_group" "alb" {
   name = "${var.cluster_name}-alb"
   ingress {
      from_port = local.http_port
      to_port = local.http_port
      protocol = local.tcp_protocol
      cidr_blocks = local.all_ips
   }
   egress {
      from_port = local.any_port
      to_port = local.any_port
      protocol = local.any_protocol
      cidr_blocks = local.all_ips
   }
}

## Module Outputs

