# Source: https://developer.hashicorp.com/vault/docs/what-is-vault

v1.21.x (latest)

- Vault
- [v1.20.x](/vault/docs/v1.20.x/about-vault/what-is-vault)
- [v1.19.x](/vault/docs/v1.19.x/about-vault/what-is-vault)
- [v1.18.x](/vault/docs/v1.18.x/about-vault/what-is-vault)
- [v1.17.x](/vault/docs/v1.17.x/about-vault/what-is-vault)
- [v1.16.x](/vault/docs/v1.16.x/about-vault/what-is-vault)
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

# What is Vault?

Vault provides centralized, well-audited privileged access and secret management
for mission-critical data whether you deploy systems on-premises, in the cloud,
or in a hybrid environment.

With a modular design based around a growing plugin ecosystem, Vault lets you
integrate with your existing systems and customize your application workflow.

## Why should I use Vault?

Modern software works because of **secrets**. Secrets are sensitive, discrete
pieces of information like credentials, encryption keys, authentication
certificates, and other critical pieces of information your applications need
to run consistently and securely.

Vault helps harden applications by centralizing secret management. With Vault
you can:

- [Manage static secrets](/vault/docs/about-vault/why-use-vault/static-secrets)
- [Manage certificates](/vault/docs/about-vault/why-use-vault/certificates)
- [Manage identities and authentication](/vault/docs/about-vault/why-use-vault/identities)
- [Manage 3rd-party secrets](/vault/docs/about-vault/why-use-vault/3rd-party-secrets)
- [Manage sensitive data](/vault/docs/about-vault/why-use-vault/sensitive-data)
- [Support regulatory compliance](/vault/docs/about-vault/why-use-vault/regulatory-compliance)

Try HCP Vault Dedicated

HCP Vault Dedicated runs Vault in the cloud using the same binary as
self-managed Vault Enterprise. It offers a consistent user experience without
the hassle of managing deployment clusters or servers.

[Sign up for HCP Vault Dedicated](https://portal.cloud.hashicorp.com) or
review the [HCP Vault Dedicated tutorials](/vault/tutorials/cloud) to learn
more.

## What is a plugin?

Plugins act as building blocks in Vault that let you control how data moves
through your environment and how clients access that data.

The [plugin ecosystem](/vault/docs/plugins) includes:

- authentication plugins that handle authentication flows and control client
  access to Vault.
- general secret plugins that generate, store, manage, or transform sensitive
  information.
- database secret plugins that manage dynamic credentials that clients use to
  access database data.

Use plugins from the [curated plugin registry](/vault/integrations) or
[build custom plugins](/vault/docs/plugins/plugin-development) to
integrate Vault in the way that makes the most sense for you workflows.

## Who can access data in Vault?

Vault encrypts data at rest and gates access to that data with configurable,
robust [authentication](/vault/docs/concepts/auth) and
[authorization](/vault/docs/concepts/policies) methods.

![How Vault works](https://web-unified-docs-hashicorp.vercel.app/api/assets/vault/latest/img/how-vault-works.png)

1. Clients authenticate with manually generated tokens, protocols like LDAP, or
   third-party providers like Azure and AWS.
2. Vault generates an access token that links the client request to an internal
   entity and applicable security policies.
3. Clients interact with secrets and encryption operations based on resource
   paths mounted in Vault.
4. Vault authorizes the client request against policies set on the resource path
   and grants or denies access accordingly.

Throughout the process, Vault audits all activity, regardless of whether
authentication or authorization succeeds so you can track interactions with
mission critical systems.

## Where does Vault store data?

Vault supports a variety of options for durable information storage.

| Storage type | HA support | Description |
| --- | --- | --- |
| [Integrated](/vault/docs/configuration/storage/raft) | YES | The "built-in" storage option that encrypts and replicates data across an operating Vault cluster. |
| [File system](/vault/docs/configuration/storage/filesystem) | NO | Persists data to the local file system on the machine running Vault. |
| [External](/vault/docs/configuration/storage#integrated-vs-external) | MAYBE | A durable third-party storage system like Azure, AWS, Google Cloud, or MySQL. |
| [In-memory](/vault/docs/configuration/storage/in-memory) | NO | Persists data entirely in-memory on the machine running Vault for development and experimentation. |

We recommend integrated storage for most deployments. Integrated storage
supports backup/restore workflows, high availability, and Enterprise replication
features without relying on third-party systems where Vault cannot verify the
security and traceability of data access.

## When should I not use Vault?

Vault is robust, powerful, and flexible. But it can also be overwhelming if
you have limited or simple secret management needs.

If your organization is just getting started with secrets management or looking
to simplify an existing secrets management processes, consider starting with
[HCP Vault Dedicated](/hcp/docs/vault/what-is-hcp-vault) instead of Vault.

HCP Vault Dedicated is a managed offering of Vault that runs on the HashiCorp
cloud platform. HCP Vault Dedicated provides a Vault Enterprise cluster without
the operational overhead of planning, deploying, and managing a self-hosted
Vault cluster.

## How do I get Vault?

You can
[download Vault as a precompiled binary](http://releases.hashicorp.com/vault),
install an official [Community](/vault/install) or
[Enterprise](/vault/install/enterprise) package with supported package managers,
or clone the Vault Community repo in GitHub and
[build Vault from source code](/vault/get-vault/build-from-code).

To use Vault Enterprise features, you must have a
[valid license configured](/vault/docs/license).

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | [GitHub logo](https://github.com/hashicorp/vault) | [YouTube logo](https://www.youtube.com/HashiCorp) | [LinkedIn logo](https://www.linkedin.com/products/hashicorp-vault) |  |

[Edit this page on GitHub](https://github.com/hashicorp/web-unified-docs/blob/main/content/vault/v1.21.x/content/docs/about-vault/what-is-vault.mdx)