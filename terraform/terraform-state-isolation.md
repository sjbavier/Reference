# Isolation of State

There are two ways to isolate state files:

- Isolation via **workspaces**
- Isolation via file layout

## Isolation via workspaces

Terraform workspaces allow you to store Terraform state in multiple separate named workspaces. Terraform uses the default workspace if no workspace is defined.

To create or switch between workspaces

```sh
terraform workspace