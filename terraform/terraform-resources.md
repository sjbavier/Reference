# Working with Terraform resources

use resources to create servers, databases and load balancers etc.

Terraform resource format:

```tf
   resource "<PROVIDER>_<TYPE>" "<NAME>" {
   [CONFIG ...]
}
```

## Example AWS EC2 instance, security group

Create an AWS instance and add the security group ID passed as a **reference**:

```tf
resource "aws_instance" "example" {
   ami = "ami-0c55b159cbfafe1f0"
   instance_type = "t2.micro"
   vpc_security_group_id = [aws_security_group.instance.id]

   tags = {
      Name = "terraform-example"
   }
}
```

By default AWS EC2 instances don't allow traffic, you'll have to create a security group.  CIDR blocks with 0.0.0.0/0 includes all possible IP addresses

```tf
resource "aws_security_group" "instance" {
   name = "terraform-example-instance"
      ingress {
      from_port = 8080
      to_port = 8080
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      }
}
```

The security group ID is passes as a **reference** which allows access to values from other parts of your code.  The format is as follows:

```tf
<PROVIDER>_<TYPE>.<NAME>.<ATTRIBUTE>
[aws_security_group.instance.id]
```

The reference informs Terraform that it has an **implicit dependency** that is must create the security group before the EC2 instance. You can view the dependency graph which is output in a language called DOT which can be turned into an image using Graphviz:

```sh
terraform graph
```

