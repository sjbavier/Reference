# Working with Terraform resources

use resources to create servers, databases and load balancers etc.

Terraform resource format:

```tf
   resource "<PROVIDER>_<TYPE>" "<NAME>" {
   [CONFIG ...]
}
```

```tf
resource "aws_instance" "example" {
   ami = "ami-0c55b159cbfafe1f0"
   instance_type = "t2.micro"
}
```