# Working with Terraform Datasources

Datasources are read-only information that is fetched from providers. Each provider specifies a variety of data sources such as VPC data, subnet data, AMI IDs, IP address ranges, user identity etc.

## Defining datasource

To define a datasource:

```tf
data "<PROVIDER>_<TYPE>" "<NAME>" {
   [CONFIG ...]
}
```

The [CONFIG ...] consists of one or more arguments specific to that data source, for example:

```tf
data "aws_vpc" "default" {
   default = true
}
```

Note: the arguments you pass are typically search filters. In this example the filter **default = true** directs Terraform to look up the default VPC in your AWS account.

## Using the data

To use the data source value:

```tf
data.<PROVIDER>_<TYPE>.<NAME>.<ATTRIBUTE>
```

Example:

```tf
data.aws_vpc.default.id
```

You can combine with other data sources:

```tf
data "aws_subnet_ids" "default" {
   vpc_id = data.aws_vpc.default.id
}
```

and pull subnet IDs

```tf
resource "aws_autoscaling_group" "example" {
   launch_configuration = aws_launch_configuration.example.name
   vpc_zone_identifier = data.aws_subnet_ids.default.ids
   min_size = 2
   max_size = 10
   tag {
      key = "Name"
      value = "terraform-asg-example"
      propagate_at_launch = true
   }
}

## Using template_file datasource for User Data scripts

There are many ways to use scripts in your IAC a common need is to interpolate variables within the script:

> note: file(<PATH>) takes a relative or absolute path

```tf
data "template_file" "user_data" {
   template = file("user-data.sh")
   vars = {
      server_port = var.server_port
      db_address = data.terraform_remote_state.db.outputs.address
      db_port = data.terraform_remote_state.db.outputs.port
   }
}
```

And where user-data.sh is:

```sh
#!/bin/bash
cat > index.html <<EOF
<h1>Hello, World</h1>
<p>DB address: ${db_address}</p>
<p>DB port: ${db_port}</p>
EOF
nohup busybox httpd -f -p ${server_port} &
```

The final step would be to update the user_data parameter of the launch configuration resource to point to the rendered output attribute of the template_file data source:

```tf
resource "aws_launch_configuration" "example" {
   image_id = "ami-0c55b159cbfafe1f0"
   instance_type = "t2.micro"
   security_groups = [aws_security_group.instance.id]
   user_data = data.template_file.user_data.rendered
   
   # Required when using a launch configuration with an auto scaling group.
   # https://www.terraform.io/docs/providers/aws/r/launch_configuration.html
   lifecycle {
      create_before_destroy = true
   }
}
```