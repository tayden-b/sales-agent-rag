# Terraform State Management

## Overview

Terraform must store state about your managed infrastructure and configuration. This state is used by Terraform to map real world resources to your configuration, keep track of metadata, and to improve performance for large infrastructures.

## State File

By default, Terraform stores state locally in a file named `terraform.tfstate`. This works for individual developers but creates problems for teams.

Problems with local state:
- No shared access for team collaboration
- No locking — concurrent runs can corrupt state
- No encryption — state may contain sensitive data
- No versioning — cannot roll back to previous state

## Remote State Backends

Remote backends solve the problems of local state by storing the state file remotely and providing locking.

### Terraform Cloud / HCP Terraform

The recommended backend for teams. Provides:
- Remote state storage with encryption
- State locking to prevent concurrent modifications
- State versioning with rollback capability
- Run history and audit trail
- Team access controls and SSO
- Policy enforcement via Sentinel

### S3 Backend

Store state in an AWS S3 bucket with DynamoDB for locking:
```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

### Azure Blob Storage Backend

Similar to S3 but for Azure environments, using Azure Blob Storage with lease-based locking.

## State Locking

State locking prevents concurrent operations on the same state. When supported by the backend, Terraform will lock the state for all operations that could write state.

If locking fails, Terraform will not proceed. This prevents state corruption from concurrent writes.

Force-unlock should only be used if automatic unlocking fails:
```
terraform force-unlock LOCK_ID
```

## Sensitive Data in State

Terraform state can contain sensitive values (database passwords, API keys). Best practices:
- Always use a backend that supports encryption
- Use Terraform Cloud for automatic encryption
- Never commit state files to version control
- Restrict access to state storage (IAM policies)
- Consider using Vault for secret management alongside Terraform

## State Migration

Moving state between backends:
```
terraform init -migrate-state
```

Terraform will detect the backend change and prompt to migrate state from the old backend to the new one.

## Workspaces

Workspaces allow multiple state files for the same configuration. Common use case: managing dev, staging, and prod environments with the same Terraform code.

```
terraform workspace new staging
terraform workspace select staging
terraform apply
```

Each workspace maintains its own state file independently.
