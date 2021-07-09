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

---

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

---

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
```

## Module Outputs

In Terraform a module can also return values using output variables.  It is the inverse of input variables, in other words you are getting a return value from the module into the development/staging/production state environments. This is helpful as the name of certain resources is not known until after they have been created.

Syntax is as follows:

```tf
module.<MODULE_NAME>.<OUTPUT_NAME>
```

For example to set autoscaling based on the **recurrence** parameter (which takes cron syntax) we could define the module outputs for the ASG name in **/modules/services/webserver-cluster/outputs.tf**

```tf
output "asg_name" {
   value = aws_autoscaling_group.example.name
   description = "The name of the Auto Scaling Group"
}
```

Then in the production environment main.tf **prod/services/webserver-cluster/main.tf** you can utilize the value

```tf
   resource "aws_autoscaling_schedule" "scale_out_during_business_hours" {
   scheduled_action_name = "scale-out-during-business-hours"
   min_size = 2
   max_size = 10
   desired_capacity = 10
   recurrence = "0 9 * * *"
   autoscaling_group_name = module.webserver_cluster.asg_name
}
resource "aws_autoscaling_schedule" "scale_in_at_night" {
   scheduled_action_name = "scale-in-at-night"
   min_size = 2
   max_size = 10
   desired_capacity = 2
   recurrence = "0 17 * * *"
   autoscaling_group_name = module.webserver_cluster.asg_name
}
```

---

## Module Caveats

- file paths
- inline blocks

### File paths

Reading User Data scripts can be done using **file**, however by default Terraform interprets the path relative to the current working directory (aka where you are running **terraform apply**).  You can also utilize the **path reference** expression path.\<TYPE\>

- **path.module** - returns filesystem path where the module expression was defined
- **path.root** - returns filesystem path of root module
- **path.cwd** - returns filesystem path of the current working directory (usually but not always the same as path.root)

For a User Data script you usually need a path relative to the module itself so in this case you should use **path.module** and the **template_file** datasource within **modules/services/webserver-cluster/main.tf**

```tf
data "template_file" "user_data" {
   template = file("${path.module}/user-data.sh")
   vars = {
      server_port = var.server_port
      db_address = data.terraform_remote_state.db.outputs.address
      db_port = data.terraform_remote_state.db.outputs.port
   }
}
```

### Inline blocks

The configuration of some Terraform resources can be defined as inline blocks but for best practice you should use separate resources.

> note: you cannot use a mix of both inline blocks and separate resources or you will get errors.

For example you can define this aws_security_group resource as an **inline block:**

```tf
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
```

However it is better to separately define the resources rules:
> note: the resource name split into **aws_security_group** and **aws_security_group_rule**. Other resources have similar resource splits including: **aws_route_table** and **aws_route**, **aws_network_acl** and **aws_network_acl_rule**

Here we split the ingress and egress rules into separate resources:

```tf
resource "aws_security_group" "alb" {
   name = "${var.cluster_name}-alb"
}
resource "aws_security_group_rule" "allow_http_inbound" {
   type = "ingress"
   security_group_id = aws_security_group.alb.id
   from_port = local.http_port
   to_port = local.http_port
   protocol = local.tcp_protocol
   cidr_blocks = local.all_ips
}
resource "aws_security_group_rule" "allow_all_outbound" {
   type = "egress"
   security_group_id = aws_security_group.alb.id
   from_port = local.any_port
   to_port = local.any_port
   protocol = local.any_protocol
   cidr_blocks = local.all_ips
}
```

This allows you to say, add an additional port for debugging in the staging environment **stage/services/webservercluster/
main.tf:**:

```tf
resource "aws_security_group_rule" "allow_testing_inbound" {
   type = "ingress"
   security_group_id = module.webserver_cluster.alb_security_group_id
   from_port = 12345
   to_port = 12345
   protocol = "tcp"
   cidr_blocks = ["0.0.0.0/0"]
}
```

You must also add an output variable for the aws_security_group since that id will not be known until after its created:

```tf
output "alb_security_group_id" {
   value = aws_security_group.alb.id
   description = "The ID of the Security Group attached to the load balancer"
}
```

> note: these examples create two different environments for load balancers, servers and databases but they are not isolated at the network level, this opens two risks, one environment could affect the other (routing tables etc.) and an attacker could compromise one environment and affect the other.  **--To be fixed--**
---

## Module Versioning

It is best practice to decouple the development of modules from the live production versions.  The **source** parameter can use local file paths as in above examples but it also can use other module sources such as Git URLS, Mercurial URLS and othe HTTP urls.  It is good architecture to spread your Terraform code across at least two repositories:

- modules - repo with reusable modules for infrastructure
- live - repo with the live infrastructure you're running in each environment (stage, production, management)

New file structure:

- modules
  - services
    - webserver-cluster
- live
  - stage
    - webserver-cluster
    - datastores
      - mysql
  - prod
    - services
      - webserver-cluster
    - datastores
      - mysql
  - global
    - s3

Initialize git in the modules directory and add the remote origin.  The idea here is to utilize git tags within the URL of the **source** parameter which are just human friendly pointers to commit sha1 hashes.

Add a git version tag

```sh
git tag -a "v0.0.1" first release of webserver-cluster module
git push --follow-tags
```

example **live/stage/services/webserver-cluster/main.tf**

```tf
module "webserver_cluster" {
   source = "github.com/foo/modules//webserver-cluster?ref=v0.0.1"
   cluster_name = "webservers-stage"
   db_remote_state_bucket = "(YOUR_BUCKET_NAME)"
   db_remote_state_key = "stage/data-stores/mysql/terraform.tfstate"
   instance_type = "t2.micro"
   min_size = 2
   max_size = 2
}
```

> note the double forward slash // in the Git URL is required. Also you need to run **terraform init** everytime you update your versioned module code

If you are using a private git repo you will need to authenticate and the recommended way is using SSH.  The urls then come in the format git@github.com:\<OWNER\>/\<REPO\>.git//\<PATH\>?ref=\<VERSION\>

example **live/stage/services/webserver-cluster/main.tf**

```tf
module "webserver_cluster" {
   source = "git@github.com:foo/modules.git//webserver-cluster?ref=v0.0.2"
   cluster_name = "webservers-stage"
   db_remote_state_bucket = "(YOUR_BUCKET_NAME)"
   db_remote_state_key = "stage/data-stores/mysql/terraform.tfstate"
   instance_type = "t2.micro"
   min_size = 2
   max_size = 2
}
```
