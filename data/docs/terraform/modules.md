# Terraform Modules

## Overview

Modules are containers for multiple resources that are used together. A module consists of a collection of .tf files kept together in a directory. Modules are the main way to package and reuse resource configurations with Terraform.

## Module Structure

A typical module has this structure:
```
module/
├── main.tf          # Primary resource definitions
├── variables.tf     # Input variable declarations
├── outputs.tf       # Output value declarations
├── versions.tf      # Provider and Terraform version constraints
└── README.md        # Module documentation
```

## Using Modules

### Terraform Registry

The Terraform Registry hosts publicly available modules:
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "my-vpc"
  cidr = "10.0.0.0/16"
}
```

### Private Registry (HCP Terraform)

Organizations can publish private modules in HCP Terraform:
```hcl
module "internal_vpc" {
  source  = "app.terraform.io/my-org/vpc/aws"
  version = "2.1.0"
}
```

### Local Modules

Reference modules from local paths:
```hcl
module "database" {
  source = "./modules/database"

  instance_class = "db.t3.medium"
  engine         = "postgresql"
}
```

## Module Best Practices

### Composition Over Inheritance
- Build small, focused modules that do one thing well
- Compose larger infrastructure from smaller modules
- Avoid deeply nested module hierarchies (2-3 levels max)

### Input Variables
- Provide sensible defaults where possible
- Use variable validation for input constraints
- Document all variables with descriptions
- Use object types for related variables

### Output Values
- Output all values that downstream modules might need
- Include resource IDs, ARNs, endpoints
- Use descriptive output names

### Versioning
- Pin module versions in production environments
- Use semantic versioning for module releases
- Test module upgrades in non-production first

## Module Testing

Use `terraform test` (Terraform 1.6+) for module testing:
```hcl
# tests/main.tftest.hcl
run "verify_vpc" {
  command = plan

  assert {
    condition     = module.vpc.vpc_id != ""
    error_message = "VPC ID should not be empty"
  }
}
```

## Terraform Cloud Private Module Registry

HCP Terraform provides a private module registry for organizations:
- Version control integration (GitHub, GitLab, Bitbucket)
- Automatic version tagging from Git tags
- Module documentation generated from README and variables
- Team-based access controls
- Usage tracking across workspaces
