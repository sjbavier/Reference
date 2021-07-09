# Working with Terraform variables

Terraform allows you to keep your IAC DRY(don't repeat yourself)

## Input Variables

### Declaring a variable:

The body of the declaration [CONFIG...] can contain 3 parameters, all optional.

- **description:** always a good idea to use this parameter to describe your code, also will print when running **plan** or **apply**.
- **default:** There are a number of ways to provide a value for the variable, including passing it in at the command line (using the -var option), via a file (using the -var-file option), or via an environment variable (Terraform looks for environment variables of the name TF_VAR_<variable_name>). If no value is passed in, the variable will fall back to this default value. If there is no default value, Terraform will interactively prompt the user for one.
- **type:** this allows type constraints, it supports (string, number, bool, list, map, set, object, tuple, any)

```tf
variable "NAME" {
   [CONFIG...]
}
```

examples:

```tf
variable "number_example" {
   description = "An example of a number variable in Terraform"
   type = number
   default = 42
}

variable "list_example" {
   description = "An example of a list in Terraform"
   type = list
   default = ["a", "b", "c"]
}

variable "list_numeric_example" {
   description = "An example of a numeric list in Terraform"
   type = list(number)
   default = [1, 2, 3]
}

variable "map_example" {
   description = "An example of a map in Terraform"
   type = map(string)
   default = {
      key1 = "value1"
      key2 = "value2"
      key3 = "value3"
   }
}

variable "object_example" {
   description = "An example of a structural type in Terraform"
   type = object({
      name = string
      age = number
      tags = list(string)
      enabled = bool
   })
   default = {
      name = "value1"
      age = 42
      tags = ["a", "b", "c"]
      enabled = true
   }
}
```

### Using input variables

Using a variable reference:

```tf
var.<VARIABLE_NAME>
```

```tf
resource "aws_security_group" "instance" {
   name = "terraform-example-instance"
   ingress {
      from_port = var.server_port
      to_port = var.server_port
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
   }
}
```
 
 To use within a User Data script, use the string interpolation syntax:

 ```sh
 ${var.<VARIABLE_NAME>}
 ```

 ```sh
 user_data = <<-EOF
   #!/bin/bash
   echo "Hello, World" > index.html
   nohup busybox httpd -f -p ${var.server_port} &
   EOF
```

## Output variables

### Declaring output variables

**NAME** is the name of the output variable and **VALUE** can be any Terraform expression.  **CONFIG ...** can contain two optional parameters:

- **description:** always a good idea to use this parameter to describe your code
- **sensitive:** set this parameter to **true** to instruct Terraform not to log this output in **terraform apply**, useful for secrets, passwords, private keys etc.

```tf
output "<NAME>" {
      value = <VALUE>
      [CONFIG ...]
}
```

examples:
aws_instance = RESOURCE, example = NAME,  public_ip = ATTRIBUTE

```tf
output "public_ip" {
   value = aws_instance.example.public_ip
   description = "The public IP address of the web server"
}
```

After running **terraform apply** you can see the outputs

```sh
# example
terraform apply
# (...)
# aws_security_group.instance: Refreshing state... [id=sg-078ccb4f9533d2c1a]
# aws_instance.example: Refreshing state... [id=i-028cad2d4e6bddec6]
# Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
# Outputs:
# public_ip = 54.174.13.5
```

After apply you can also use terraform output

```sh
terraform output
# public_ip = 54.174.13.5
terraform output public_ip
# 54.174.13.5
```