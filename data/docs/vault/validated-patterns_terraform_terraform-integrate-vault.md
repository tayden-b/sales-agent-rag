# Source: https://developer.hashicorp.com/validated-patterns/terraform/terraform-integrate-vault

# Integrate Terraform with Vault

- 14min
- |
- HCP
- Terraform
- Vault

**Author:** Shriram Rajaraman

Note

This is a beta document and may be subject to change.

HashiCorp Vault offers an identity-based management system for secrets and encryption, ensuring secure access through authentication and authorization. By integrating Terraform with Vault, organizations can enhance their infrastructure and security lifecycle management by enabling secure provisioning, dynamic secret management, and automated secret rotation, thus bolstering their overall security framework.

In this guide, you will learn how to integrate Terraform with Vault to enhance security through:

1. Authenticate to Vault.
2. Configure dynamic provider credentials (dynamic credentials for Terraform Providers including AWS, Azure & GCP).
3. Read and write secrets with Terraform.
4. Enable Terraform secrets engine (Generating dynamic secrets for Terraform runs using Vault).

Note

Unless specifically mentioned, concepts that apply to HCP Terraform also apply to its self-hosted version, Terraform Enterprise (TFE). Similarly, concepts that apply to HCP Vault Dedicated also apply to its self-hosted version, Vault Enterprise.

### Target audience

This guide references the following roles:

- Platform Teams responsible for managing HCP Terraform.
- Security Teams responsible for managing HCP Vault Dedicated.

## Prerequisites

To complete this pattern, you need access to the following:

- **HCP Vault**: admin rights to configure Vault namespaces, policies, authentication methods and secret engines.
- **HCP Terraform**: workspace administrator rights to configure workspaces, set up VCS integrations, and manage environment variables.
- **Version control system (VCS)**: access to repositories storing Terraform configurations and potentially Packer templates, including permissions to commit changes and manage branches.

We recommend you review the following before following this pattern:

- [Vault Enterprise](/validated-designs/vault-solution-design-guides-vault-enterprise) and [Terraform Enterprise](/validated-designs/terraform-solution-design-guides-terraform-enterprise) Solution Design Guides (for self-hosted customers)
- Reviewed [Terraform Operating Guide - Adopting](/validated-designs/terraform-operating-guides-adoption)
- Reviewed [Vault Operating Guide - Adopting](/validated-designs/vault-operating-guides-adoption)
- HashiCorp [Terraform and Vault training](https://www.hashicorp.com/training)

## Background and best practices

We recommend careful planning to ensure that objects in both HCP Terraform (Projects/Workspaces) and Vault (Namespaces/Secret Engines) are mapped correctly. This will ensure that the integration is scalable and secure.

Both the Terraform and Vault Operating guides provide recommendations on how an organization should structure their Terraform projects and Vault namespaces. This guide that those recommendations to the next step from an integration perspective.

While there is no one correct answer to how to map Terraform projects to Vault namespaces, we recommend that whatever the pattern is, it should be consistent across the organization. This will ensure that the integration is scalable and secure.

This example demonstrates how workspaces/projects in Terraform can be mapped to namespaces in Vault.

![Terraform Vault Integration Pattern](/_next/image?url=https%3A%2F%2Fcontent.hashicorp.com%2Fapi%2Fassets%3Fproduct%3Dtutorials%26version%3Dmain%26asset%3Dpublic%252Fimg%252Fvalidated-patterns%252Fterraform-better-together-vault%252Ftf-vault-mapping.png%26width%3D1631%26height%3D2719&w=3840&q=75&dpl=dpl_BSBiTKZgSo9Do7qmMBjAos8jUGxr)

1. In the HCP Terraform organization, projects are created based on [two factors](/validated-designs/terraform-operating-guides-adoption/configuration-for-first-use#projects), the line of business they belong to and the application for which the infrastructure will be provisioned. Similarly, Vault namespaces are created for each line of business.
2. Each application would be deployed into multiple environments. Additionally, the infrastructure is divided into different tiers like compute, storage and databases, each having its own workspace according to the workspace design best practices.
3. An HCP Terraform organization would map logically to the Vault root namespace. Similarly, all projects created for a particular line of business(LOB) would map logically to a single namespace in Vault dedicated to storing all secrets of that particular LOB.
4. A dedicated secrets engine mount will be created for each environment within the LOB namespace. For example, dynamic credentials for AWS accounts will be mounted on aws-dev, aws-uat, aws-prod mounts respectively. Mounts that allow a folder structure like K/V can have a path structure like kv/dev, kv/uat etc with RBAC policies in place

Refer to the [Manage tenants with Vault namespaces](/vault/tutorials/manage-hcp-vault-dedicated/vault-manage-namespaces) tutorial for additional recommendations on Vault namespace design.

Note

If your organization already consumes either one of HCP Terraform or Vault or both, has an existing integration design, it is recommended to evaluate the factors and considerations mentioned above and accordingly align your Terraform organization and Vault namespace design to closely match the best practices mentioned in this section.

## Validated architecture

![Terraform and Vault validated architecture](/_next/image?url=https%3A%2F%2Fcontent.hashicorp.com%2Fapi%2Fassets%3Fproduct%3Dtutorials%26version%3Dmain%26asset%3Dpublic%252Fimg%252Fvalidated-patterns%252Fterraform-better-together-vault%252Ftf-vault-integration-arch.png%26width%3D1530%26height%3D788&w=3840&q=75&dpl=dpl_BSBiTKZgSo9Do7qmMBjAos8jUGxr)

Terraform can connect to Vault either directly (a) or via Terraform Cloud Agent (b).

For HCP Terraform customers, we recommend that Terraform Cloud agents are used to connect to Vault (b). This will ensure that Vault DNS is not exposed to the public internet and improves the security posture of the integration.

For Terraform Enterprise customers, since both Terraform and Vault will be on a private network either method will provide the same level of security.

If you are using HCP Terraform or Terraform Enterprise with HCP Vault Dedicated, we again recommend using Terraform Cloud agent. The Terraform Cloud agent should be able to use use private (non-public) networking leveraging [HashiCorp Virtual Network](/hcp/docs/hcp/network) (HVN).

In the following example, we show how to connect Terraform to Vault using the Terraform Cloud agent when Terraform and Vault are on different networks. While this example shows HCP Terraform and HCP Vault Dedicated, the same pattern can be used for Terraform Enterprise and Vault Enterprise in different networks.

![Terraform and Vault network architecture](/_next/image?url=https%3A%2F%2Fcontent.hashicorp.com%2Fapi%2Fassets%3Fproduct%3Dtutorials%26version%3Dmain%26asset%3Dpublic%252Fimg%252Fvalidated-patterns%252Fterraform-better-together-vault%252Ftf-vault-network.png%26width%3D1635%26height%3D1348&w=3840&q=75&dpl=dpl_BSBiTKZgSo9Do7qmMBjAos8jUGxr)

## People and process considerations

The Terraform operation guides include recommended people and process patterns. We recommend that the platform team admin is responsible for the following:

1. Ensure that the integration between HCP Terraform and HCP Vault is established.
2. Establish an appropriate mapping between the Terraform projects, workspaces and Vault namespaces keeping RBAC and scalability as priorities.
3. Ensure that the appropriate Terraform workspaces are assigned the correct variable sets with Vault static secrets or/and integrated with the appropriate Vault namespaces and secret engines for dynamic credentials.
4. Ensure documentation is in a centralized location for the application team regarding this integration.
5. Set up periodic collaboration meetings with the cross-functional teams to ensure that the integration's objectives are being met.

## Authenticate to Vault

The first step of integrating Terraform with Vault is to authenticate Terraform to Vault. Terraform can authenticate to Vault using static credentials or dynamic credentials.

The Vault provider supports authentication engines such as [Userpass](https://registry.terraform.io/providers/hashicorp/vault/latest/docs#userpass), [TLS Certificate](https://registry.terraform.io/providers/hashicorp/vault/latest/docs#tls-certificate), and more. Using such static credentials in your workspaces to authenticate to Vault presents a security risk even if you rotate your credentials regularly.

Note

HashiCorp recommends to use HCP Terraform's native OpenID connect integration with Vault to establish a trust relationship between a Terraform workspace and Vault.

Configuring the authentication for the integration requires the following steps:

1. [Configure Vault](/terraform/cloud-docs/workspaces/dynamic-provider-credentials/vault-configuration#configure-vault): Set up a trust configuration between Vault and HCP Terraform. Then, you must create Vault roles and policies for your HCP Terraform workspaces.
2. [Configure HCP Terraform](/terraform/cloud-docs/workspaces/dynamic-provider-credentials/vault-configuration#configure-hcp-terraform): Add environment variables to the HCP Terraform workspaces where you want to use Dynamic Credentials.

You can set these as workspace variables, or if you'd like to share one Vault role across multiple workspaces, you can use a variable set. We recommend using Variable Sets for better management of environment variables across multiple workspaces.

When you configure dynamic provider credentials with multiple provider configurations of the same type, use either a default variable or a tagged alias variable name for each provider configuration. Refer to [Specifying multiple configurations](/terraform/cloud-docs/workspaces/dynamic-provider-credentials/vault-configuration#specifying-multiple-configurations) for more details.

For example, consider the Terraform Organization: Vault Root Namespace mapping diagram referenced in the previous section. For the `lob1-app1-compute-dev` Terraform workspace to access the AWS secrets engine in the `lob1` Vault namespace, you must set the following environment variables.

| Key | Value |
| --- | --- |
| `TFC_VAULT_PROVIDER_AUTH` | `true` |
| `TFC_VAULT_ADDR` | The address of the Vault instance to authenticate against. |
| `TFC_VAULT_RUN_ROLE` | The name of the Vault role to authenticate against |
| `TFC_VAULT_NAMESPACE` | `lob1` |

There are additional [optional environment variables](/terraform/cloud-docs/workspaces/dynamic-provider-credentials/vault-configuration#optional-environment-variables) that can be configured which give more fine-grained control over the specific Vault configurations for your use case.

Note

Once you set up dynamic credentials for a workspace using a variable set, HCP Terraform automatically authenticates to Vault for each run. Do not pass the address, token, or namespace arguments into the provider configuration block. HCP Terraform sets these values as environment variables in the run environment.

## Configure dynamic provider credentials

Dynamic provider credentials refer to Vault's secrets engines to generate short-lived dynamic secrets for various providers including AWS, GCP and Azure. We recommend that you use these dynamic provider credentials to authenticate to the respective cloud providers instead of static credentials especially for cloud (AWS, GCP, Azure) credentials.

Vault-backed dynamic credentials include several advantages over using only dynamic provider credentials without Vault:

- Consolidated management and auditing for all your cloud credentials and other secrets.
- No OIDC setup required in your cloud provider.
- Leverage existing Vault secrets engine configurations to generate short-lived credentials.
- No need to expose inbound access to self-hosted Terraform Enterprise instances from cloud providers to validate OIDC metadata.

For more details, refer to the [Why use Vault-backed dynamic credentials to secure HCP Terraform infrastructure?](https://www.hashicorp.com/blog/why-use-vault-backed-dynamic-credentials-to-secure-hcp-terraform-infrastructure) blog post.

Refer to the cloud provider specific guidance ([AWS](/terraform/cloud-docs/workspaces/dynamic-provider-credentials/vault-backed/aws-configuration), [GCP](/terraform/cloud-docs/workspaces/dynamic-provider-credentials/vault-backed/gcp-configuration), [Azure](/terraform/cloud-docs/workspaces/dynamic-provider-credentials/vault-backed/azure-configuration)) to set up dynamic provider credentials.

The following is an example that uses Vault-backed dynamic credentials for authenticating to the AWS provider.

Set the following environment variables in your variable set and attach it to the workspace that requires the AWS credentials.

| Key | Value |
| --- | --- |
| `TFC_VAULT_BACKED_AWS_AUTH` | `true` |
| `TFC_VAULT_BACKED_AWS_AUTH_TYPE` | Must be one of the following: `iam_user`, `assumed_role`, or `federation_token`. |
| `TFC_VAULT_BACKED_AWS_RUN_VAULT_ROLE` | The role to use in Vault |

After setting up the variable set, ensure you are not using any of the arguments or methods mentioned in the [authentication and configuration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#authentication-and-configuration) section of the provider documentation. Otherwise, these settings may interfere with dynamic provider credentials.

```
# Initialize the providers for Vault and AWS.
provider "vault" {}

provider "aws" {
  region = "us-east-1"
}
```

On top of credentials used to authenticate to cloud providers, there are other types of secrets such as credentials to authenticate to database providers (eg: PostgreSQL, MongoDB, Oracle, Snowflake etc.), PKI certificates, SSH keys etc. It is recommended to generate such sensitive information with appropriate TTLs and roles instead of static credentials or secrets and use them as a part of your Terraform configuration.

The following example uses Vault to fetch dynamic credentials to authenticate to the MongoDB Atlas provider.

```
# Fetch MongoDB Atlas Credentials from Vault
provider vault {}

data "vault_generic_secret" "mongodb_creds" {
  path = "mongodb/creds/access"
}

# Use Fetched MongoDB Atlas Credentials to Configure MongoDB Atlas Provider
provider "mongodbatlas" {
  public_key  = data.vault_generic_secret.mongodb_creds.data["username"]
  private_key = data.vault_generic_secret.mongodb_creds.data["password"]
}

# Example MongoDB Atlas Resource
resource "mongodbatlas_project" "example" {
  name   = "My Project"
  org_id = var.org_id
}
```

Here the MongoDB database secrets engine has been mofunted at the path `mongodb` and has a role named `access` with the right privileges to perform actions in MongoDB. You can create these credentials with appropriate TTLs to expire after you use them.

You can achieve multi-tenancy using Vault-backed dynamic provider credentials by leveraging `tags` and `aliases`. Refer to the [documentation](/terraform/cloud-docs/workspaces/dynamic-provider-credentials/specifying-multiple-configurations) to setup of multiple dynamic credential configurations.

## Use Terraform to read and write Vault secrets

When writing Terraform configurations for resources such as managed databases, compute instance key pairs, TLS certificates, etc., you generate sensitive information such as database passwords, private keys, API keys etc. These secrets need to be managed securely and we recommend that you store this sensitive information in HashiCorp Vault. Any future references to these secrets can be fetched from Vault.

Consider the example of an SSH keypair. In the code below, a key pair generated randomly is stored in Vault and also used while provisioning an AWS instance. Future references to this private key can then be fetched from Vault and used.

```
# Generate SSH Key Pair
resource "tls_private_key" "example" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Store SSH Key Pair in Vault
resource "vault_kv_secret_v2" "ssh_keys" {
  path = var.ssh-key-path

  data_json = jsonencode({
    private_key = tls_private_key.example.private_key_pem
    public_key  = tls_private_key.example.public_key_openssh
  })
}

# Create AWS Key Pair
resource "aws_key_pair" "example" {
  key_name   = var.aws-ssh-key-name
  public_key = tls_private_key.example.public_key_openssh
}

# Create AWS Compute Instance using the SSH Key Pair
resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0" # Example AMI ID for Amazon Linux 2 in us-west-2 region
  instance_type = "t2.micro"
  key_name      = aws_key_pair.example.key_name

  tags = {
    Name = "example-instance"
  }
}
```

Taking this pattern a step further, we can look to integrate some of these secrets and rotate them with HashiCorp Vault. Consider the scenario of a Google Cloud SQL instance. When a [Cloud SQL for MSSQL](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/sql_database_instance) is created using Terraform, you must pass a `root_password` parameter. Usually, this root password is randomly generated within the Terraform code itself and passed to the `google_sql_database_instance` Terraform resource.

HashiCorp Vault has the [MSSQL Database secrets engine](/vault/docs/secrets/databases/mssql), which can be used to generate dynamic username and password combinations bound by TTLs and leases. Once the **google\_sql\_database\_instance** resource is created, a database secrets engine for the same can be created in Vault along with multiple roles for each kind of database user (eg: administrator, write, read etc on specific tables and schemas). Additionally, the [root credentials can be rotated](/vault/tutorials/db-credentials/database-root-rotation#solution) and the password created earlier can no longer be used. Whenever a new user has to log in to the database, they can generate [dynamic credentials](/vault/docs/secrets/databases/mssql#usage) with TTL according to their role and use that to log in to the database. This pattern can further be refined using [HashiCorp Boundary](/boundary/docs) for [securing access to your MSSQL database](/boundary/tutorials/self-managed-deployment/azure-sql-database).

Note

This pattern means that only Vault has access to the root password of the database and the root password can no longer be retrieved by a normal user. It may be preferable to store the root password rather in the KV store of Vault and create a secondary user dedicated to Vault for managing the database users.

## Enable Terraform secrets engine

As adoption of HCP Terraform grows, you may look at incorporating it into your automated workflows and existing tooling. Interaction with the HCP Terraform API relies on auth tokens generated by the API and used by external systems to automate actions in HCP Terraform, often as part of an organization's CI/CD pipelines. Operators are left with the responsibility of tracking which tokens are in-use by their organizations.

The Vault [Terraform Cloud secrets engine](/vault/docs/secrets/terraform) enables you to generate, manage and revoke credentials for HCP Terraform and Terraform Enterprise while adhering to best practices of access and control.

We recommend that API driven workflows in your organization use the dynamic HCP Terraform API token generated by Terraform Cloud secrets engine. The lifecycle of these tokens is managed by Vault and will auto expire according to the configured TTL and max TTL of the Vault role.

The following example shows a VCS CI/CD pipeline leveraging this workflow:

![Terraform VCS CI/CD](/_next/image?url=https%3A%2F%2Fcontent.hashicorp.com%2Fapi%2Fassets%3Fproduct%3Dtutorials%26version%3Dmain%26asset%3Dpublic%252Fimg%252Fvalidated-patterns%252Fterraform-better-together-vault%252Fterraform-secrets.png%26width%3D1560%26height%3D1427&w=3840&q=75&dpl=dpl_BSBiTKZgSo9Do7qmMBjAos8jUGxr)

1. Platform teams trigger an API driven workflow in the VCS CI/CD pipeline.
2. As an initial step, a stage in the pipeline fetches a dynamic HCP Terraform API token from Vault based on the use case.
3. This dynamic HCP Terraform API token is then leveraged to trigger an API driven workflow in a HCP Terraform workspace and the plan and apply stages of the run proceed.

The HCP Terraform API limits both organization and team roles to one active token at any given time. Generating a new organization or team API token by reading the credentials in Vault or otherwise generating them on app.terraform.io (or your Terraform Enterprise FQDN) will effectively revoke any existing API token for that organization or team.

Due to this behavior, organization and team API tokens created by Vault will be stored and returned on future requests, until the credentials get rotated. This is to prevent unintentional revocation of tokens that are currently in-use.

## Conclusion

This guide demonstrated how to enhance security by integrating HashiCorp Terraform with Vault, covering authentication and access control, dynamic cloud provider credentials, secret management within Terraform configurations, and the generation of dynamic HCP Terraform API tokens through the Terraform secrets engine.

[Previous

Upgrade Terraform provider](/validated-patterns/terraform/upgrade-terraform-provider) [Next

Vulnerability management with HCP](/validated-patterns/terraform/vulnerability-and-patch-management)

## This tutorial also appears in:

- 14 tutorials

  Vault

  Validated patterns for Vault