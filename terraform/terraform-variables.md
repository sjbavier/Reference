# Working with Terraform variables

Terraform allows you to keep your IAC DRY(don't repeat yourself)
## Input Variables

### Declaring a variable:

```tf
variable "NAME" {
   [CONFIG...]
}
```

The body of the declaration [CONFIG...] can contain 3 parameters, all optional.

- **description:** always a good idea to use this parameter to describe your code, also will print when running **plan** or **apply**.
- **default:** There are a number of ways to provide a value for the variable, including passing it in at the command line (using the -var option), via a file (using the -var-file option), or via an environment variable (Terraform looks for environment variables of the name TF_VAR_<variable_name>). If no value is passed in, the variable will fall back to this default value. If there is no default value, Terraform will interactively prompt the user for one.
- **type:** this allows type constraints, it supports (string, number, bool, list, map, set, object, tuple, any)

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

