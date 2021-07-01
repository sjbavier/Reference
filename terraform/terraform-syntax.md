# Using Terraform syntax

## Loops 

- count - parameter to loop over resources
- for_each - to loop over resources and inline blocks within a resource
- for - expressions to loop over lists and maps
- for - string directive to loop over lists and maps within a string

---

### count

Count works on arrays and can be used to iterate over the items.

For example say you have a list of usernames:

```tf
variable "user_names" {
   description = "Create IAM users with these names"
   type = list(string)
   default = ["neo", "trinity", "morpheus"]
}
```

you can look at an element at index 1 **var.user_names[1]**, or get the number of items with **length**, and iterate over them with **count.index**

```tf
resource "aws_iam_user" "example" {
   count = length(var.user_names)
   name = var.user_names[count.index]
}
```

> Note that after you have used count on a resource it becomes an array of resources rather than one resource so you cannot access it using the standard syntax \<PROVIDER\>_\<TYPE\>.\<NAME\>.\<ATTRIBUTE\> **you must specify the index as well:**  \<PROVIDER\>_\<TYPE\>.\<NAME\>[INDEX].ATTRIBUTE

To get an output of all the users you can use an **"\*"**

```tf
output "all_arns" {
   value = aws_iam_user.example[*].arn
   description = "The ARNs for all users"
}
```

#### **Caveats**

You cannot use **count** within a resource to loop over inline blocks.  For example you couldn't use iterators with the key \<NAME\> or values \[CONFIG...\]

```tf
resource "xxx" "yyy" {
   <NAME> {
      [CONFIG...]
   }
}
```

Per the last example if you removed "trinity" from the list of users and then run **terraform plan** you will see that the var.user_names[2] will be destroyed and "morpheus" will be moved to replace "trinity" at var.user_names[1].

---

### for_each

The for_each expression allows you to loop over lists, sets and maps to create multiple resources, or inline-blocks within a resource.  Syntax as follows:

> note: within a resource using for_each on a list is not supported

```tf
resource "<PROVIDER>_<TYPE>" "<NAME>" {
   for_each = <COLLECTION>
   [CONFIG ...]
}
# example user creation with previous ["neo", "trinity", "morpheus"] list
resource "aws_iam_user" "example" {
   for_each = toset(var.user_names) # toset is used to convert var.user_names list to a set
   name = each.value # user_names in this case are also available in each.key, though normally used with maps of key/values
}
```

Creating output

```tf
output "all_users" {
   value = aws_iam_user.example
}
# or select just the arns
   output "all_arns" {
   value = values(aws_iam_user.example)[*].arn
}
```

Running terraform apply will yield a **map** of resources rather than an array as with count.  Thus allowing you to extract/delete exactly the resources you want and why it is generally prefered over count.

To use for_each in inline-blocks first define your map input variable, for example:

```tf
variable "custom_tags" {
   description = "Custom tags to set on the Instances in the ASG"
   type = map(string)
   default = {}
}
```

Syntax for the inline-blocks looks as follows:

```tf
# VAR_NAME variable will store the value of each iteration (instead of 'each')
dynamic "<VAR_NAME>" {
   # COLLECTION is a list or map to iterate
   for_each = <COLLECTION>
   # content block is what to generate from each iteration
   content {
      # you can use <VAR_NAME>.key and <VAR_NAME>.value within this content block for current context's item
      [CONFIG...]
}
```

For instance definig an aws_autoscaling_group

```tf
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
   # using dynamic 'tag', using custom_tags map
   dynamic "tag" {
      for_each = var.custom_tags

      content {
         # referring to each interations key and value
         key = tag.key
         value = tag.value
         propagate_at_launch = true
      }
   }
}
```

### for

for expressions follow the following syntax:

```tf
[for <ITEM> in <LIST> : <OUTPUT>]
```

Example iterating through names and outputting to uppercase in **list**

```tf
variable "names" {
   description = "A list of names"
   type = list(string)
   default = ["neo", "trinity", "morpheus"]
}
output "upper_names" {
   value = [for name in var.names : upper(name)]
}
# also some filtering applied for string length
variable "names" {
description = "A list of names"
type = list(string)
default = ["neo", "trinity", "morpheus"]
}
output "short_upper_names" {
value = [for name in var.names : upper(name) if length(name) < 5]
}
```

Example syntax with **map**

```tf
[for <KEY>, <VALUE> in <MAP> : <OUTPUT>]
```

Example iterating through **map**

```tf
variable "hero_thousand_faces" {
   description = "map"
   type = map(string)
   default = {
      neo = "hero"
      trinity = "love interest"
      morpheus = "mentor"
   }
}
output "bios" {
   value = [for name, role in var.hero_thousand_faces : "${name} is the ${role}"]
}
```

You can use for expressions to output a value from a map or a list

```tf
# For looping over lists
{for <ITEM> in <MAP> : <OUTPUT_KEY> => <OUTPUT_VALUE>}
# For looping over maps
{for <KEY>, <VALUE> in <MAP> : <OUTPUT_KEY> => <OUTPUT_VALUE>}
```

Example usage:

```tf
variable "hero_thousand_faces" {
   description = "map"
   type = map(string)
   default = {
      neo = "hero"
      trinity = "love interest"
      morpheus = "mentor"
   }
}
output "upper_roles" {
   value = {for name, role in var.hero_thousand_faces : upper(name) => upper(role)}
}
```

### String directives

Similar to string interpolations (**${...}**) a string directive (**%{...}**) can be used in for-loops and conditionals.

syntax as follows:

```tf
%{ for <ITEM> in <COLLECTION> }<BODY>%{ endfor }
```

example:

```tf
variable "names" {
   description = "Names to render"
   type = list(string)
   default = ["neo", "trinity", "morpheus"]
}
output "for_directive" {
   value = <<EOF
   %{ for name in var.names }
   ${name}
   %{ endfor }
   EOF
```

Furthermore you can strip whitespace with the **~** strip marker

```tf
output "for_directive_strip_marker" {
   value = <<EOF
   %{~ for name in var.names }
   ${name}
   %{~ endfor }
   EOF
}
```

---

## Conditionals

