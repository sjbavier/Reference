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
