# Source: https://developer.hashicorp.com/terraform/language/state/remote

v1.14.x (latest)

- Terraform
- [v1.15.x (alpha)](/terraform/language/v1.15.x/state/remote)
- [v1.13.x](/terraform/language/v1.13.x/state/remote)
- [v1.12.x](/terraform/language/v1.12.x/state/remote)
- [v1.11.x](/terraform/language/v1.11.x/state/remote)
- [v1.10.x](/terraform/language/v1.10.x/state/remote)
- [v1.9.x](/terraform/language/v1.9.x/state/remote)
- [v1.8.x](/terraform/language/v1.8.x/state/remote)
- [v1.7.x](/terraform/language/v1.7.x/state/remote)
- [v1.6.x](/terraform/language/v1.6.x/state/remote)
- [v1.5.x](/terraform/language/v1.5.x/state/remote)
- [v1.4.x](/terraform/language/v1.4.x/state/remote)
- [v1.3.x](/terraform/language/v1.3.x/state/remote)
- [v1.2.x](/terraform/language/v1.2.x/state/remote)
- [v1.1.x](/terraform/language/v1.1.x/state/remote)

# Remote State

By default, Terraform stores state locally in a file named `terraform.tfstate`.
When working with Terraform in a team, use of a local file makes Terraform
usage complicated because each user must make sure they always have the latest
state data before running Terraform and make sure that nobody else runs
Terraform at the same time.

With *remote* state, Terraform writes the state data to a remote data store,
which can then be shared between all members of a team. Terraform supports
storing state in [HCP Terraform](https://www.hashicorp.com/products/terraform/),
[HashiCorp Consul](https://www.consul.io/), Amazon S3, Azure Blob Storage, Google Cloud Storage, Alibaba Cloud OSS, and more.

Remote state is implemented by a [backend](/terraform/language/backend) or by
HCP Terraform, both of which you can configure in your configuration's root module.

## Delegation and Teamwork

Remote state allows you to share
[output values](/terraform/language/block/output) with other configurations.
This allows your infrastructure to be decomposed into smaller components.

Put another way, remote state also allows teams to share infrastructure
resources in a read-only way without relying on any additional configuration
store.

For example, a core infrastructure team can handle building the core
machines, networking, etc. and can expose some information to other
teams to run their own infrastructure. As a more specific example with AWS:
you can expose things such as VPC IDs, subnets, NAT instance IDs, etc. through
remote state and have other Terraform states consume that.

For example usage, see
[the `terraform_remote_state` data source](/terraform/language/state/remote-state-data).

While remote state can be a convenient, built-in mechanism for sharing data
between configurations, you may prefer to use more general stores to
pass settings both to other configurations and to other consumers. For example,
if your environment has [HashiCorp Consul](https://www.consul.io/) then you
can have one Terraform configuration that writes to Consul using
[`consul_key_prefix`](https://registry.terraform.io/providers/hashicorp/consul/latest/docs/resources/key_prefix) and then
another that consumes those values using
[the `consul_keys` data source](https://registry.terraform.io/providers/hashicorp/consul/latest/docs/data-sources/keys).

## Locking and Teamwork

For fully-featured remote backends, Terraform can also use
[state locking](/terraform/language/state/locking) to prevent concurrent runs of
Terraform against the same state.

[HCP Terraform by HashiCorp](https://www.hashicorp.com/products/terraform/)
is a commercial offering that supports an even stronger locking concept that
can also detect attempts to create a new plan when an existing plan is already
awaiting approval, by queuing Terraform operations in a central location.
This allows teams to more easily coordinate and communicate about changes to
infrastructure.

[Edit this page on GitHub](https://github.com/hashicorp/web-unified-docs/blob/main/content/terraform/v1.14.x/docs/language/state/remote.mdx)