# Source: https://developer.hashicorp.com/vault/docs/install

v1.21.x (latest)

- Vault
- [v1.20.x](/vault/docs/v1.20.x/get-vault)
- [v1.19.x](/vault/docs/v1.19.x/get-vault)
- [v1.18.x](/vault/docs/v1.18.x/get-vault)
- [v1.17.x](/vault/docs/v1.17.x/get-vault)
- [v1.16.x](/vault/docs/v1.16.x/get-vault)
- ---
- No versions of this document exist before v1.16.x. Click below to redirect to the version homepage.
- [v1.15.x](/vault/docs/v1.15.x)
- [v1.14.x](/vault/docs/v1.14.x)
- [v1.13.x](/vault/docs/v1.13.x)
- [v1.12.x](/vault/docs/v1.12.x)
- [v1.11.x](/vault/docs/v1.11.x)
- [v1.10.x](/vault/docs/v1.10.x)
- [v1.9.x](/vault/docs/v1.9.x)
- [v1.8.x](/vault/docs/v1.8.x)
- [v1.7.x](/vault/docs/v1.7.x)
- [v1.6.x](/vault/docs/v1.6.x)
- [v1.5.x](/vault/docs/v1.5.x)
- [v1.4.x](/vault/docs/v1.4.x)

# Get Vault

You can get Vault through a variety of package managers or from HashiCorp
directly.

## Vault version syntax

HashiCorp does not use [semantic versioning](https://semver.org) for Vault
releases. Instead, Vault uses `X.Y.Z` notation and updates Vault as **major**
releases and **minor** patches.

- Major releases update the `Y` value
- Minor patches update the `Z` value
- On rare occasions, Enterprise-only updates use an expanded notation,
  `X.Y.Z.A`, and update the `A` value.

We strongly recommend upgrading to the latest patch for supported major releases
as soon as possible. Refer to the support article on
[support periods and end-of-life](https://support.hashicorp.com/hc/en-us/articles/360021185113-Support-Period-and-End-of-Life-EOL-Policy)
for more detail.

## Get notified of new releases

You can subscribe to specific tags in the [Vault discussion forum](https://discuss.hashicorp.com/)
to receive alerts about recent changes.

- Use the
  [`vault-release-ce-ent`](https://discuss.hashicorp.com/tag/vault-release-ce-ent)
  tag for alerts about upcoming and new releases.
- Use the
  [`security-vault`](https://discuss.hashicorp.com/tag/security-vault) tag for
  alerts about new security bulletins.

## Install options

You have different options for installing Vault:

1. [Install Vault Community edition with supported package managers](/vault/install)
   for macOS, Ubuntu/Debian, CentIS/RHEL, Amazon Linux, and Homebrew.
2. [Install Vault Enterprise edition with supported package managers](/vault/install/enterprise)
   for macOS, Ubuntu/Debian, CentIS/RHEL, Amazon Linux, and Homebrew.
3. [Use helm to install Vault for Kubernetes](/vault/docs/platform/k8s/helm).
4. [Download a precompiled binary](/vault/install) or
   [build Vault from code](/vault/docs/install/build-from-code) and
   [install the binary manually](/vault/docs/install/install-binary).

## Related tutorials

The following tutorials provide additional guidance for installing Vault and
production cluster deployment:

- [Get started: Install Vault](/vault/tutorials/getting-started/getting-started-install)
- [Day One Preparation](/vault/tutorials/day-one-raft)
- [Recommended Patterns](/vault/tutorials/recommended-patterns)
- [Start the server in dev mode](/vault/tutorials/getting-started/getting-started-dev-server)

[Edit this page on GitHub](https://github.com/hashicorp/web-unified-docs/blob/main/content/vault/v1.21.x/content/docs/get-vault/index.mdx)