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

