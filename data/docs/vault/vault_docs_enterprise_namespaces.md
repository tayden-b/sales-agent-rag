# Source: https://developer.hashicorp.com/vault/docs/enterprise/namespaces

v1.21.x (latest)

- Vault
- [v1.20.x](/vault/docs/v1.20.x/enterprise/namespaces)
- [v1.19.x](/vault/docs/v1.19.x/enterprise/namespaces)
- [v1.18.x](/vault/docs/v1.18.x/enterprise/namespaces)
- [v1.17.x](/vault/docs/v1.17.x/enterprise/namespaces)
- [v1.16.x](/vault/docs/v1.16.x/enterprise/namespaces)
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

# Namespace and secure multi-tenancy (SMT) support in Vault

Enterprise

Appropriate [Vault Enterprise](https://www.hashicorp.com/products/vault/pricing) license or [HCP Vault Dedicated](/hcp/docs/vault/tiers-and-features) cluster required.

Many organizations implement Vault as a service to provide centralized
management of sensitive data and ensure that the different teams in an
organization operate within isolated environments known as **tenants**.

Multi-tenant environments have the following implementation challenges:

- **Tenant isolation**. Teams within a Vault as a Service (VaaS)
  environment require strong isolation for their policies, secrets, and
  identities. Tenant isolation may also be required due to organizational
  security and privacy requirements or to address compliance regulations.
- **Long-term management**. Tenants typically have different policies and teams
  request changes to their tenants at different rates. As a result, managing a
  multi-tenant environment can become difficult for a single team as the number
  of tenants within the organization grows.

Namespaces support secure multi-tenancy (**SMT**) within a single Vault
Enterprise instance with tenant isolation and administration delegation so Vault
administrators can empower delegates to manage their own tenant environment.

When you create a namespace, you establish an isolated environment with separate
login paths that functions as a mini-Vault instance within your Vault
installation. Users can then create and manage their sensitive data within the
confines of that namespace, including:

- secret engines
- authentication methods
- ACL, EGP, and RGP policies
- password policies
- entities
- identity groups
- tokens

Tip

Namespaces are isolated environments, but Vault administrators can still share
and enforce global policies across namespaces with the
[group-policy-application](/vault/api-docs/system/config-group-policy-application)
endpoint of the Vault API.

## Namespace naming restrictions

Valid Vault namespace names:

- **CANNOT** end with `/`
- **CANNOT** contain spaces
- **CANNOT** be one of the following reserved strings:
  - [`root`](/vault/docs/enterprise/namespaces#root)
  - [`sys`](/vault/docs/enterprise/namespaces#sys)
  - [`audit`](/vault/docs/enterprise/namespaces#audit)
  - [`auth`](/vault/docs/enterprise/namespaces#auth)
  - [`cubbyhole`](/vault/docs/enterprise/namespaces#cubbyhole)
  - [`identity`](/vault/docs/enterprise/namespaces#identity)

Refer to the [Namespace limits section](/vault/docs/internals/limits#namespace-limits)
of [Vault limits and maximums](/vault/docs/internals/limits) for storage limits
related to managing namespaces.

Related reading

Read the
[Vault namespace and mount structuring](/vault/tutorials/enterprise/namespace-structure)
tutorial for best practices and recommendations for structuring your namespaces.

## Child namespaces

A **child namespace** is any namespace that exists entirely within the scope of
another namespace. The containing namespace is the **parent namespace**. For
example, given the namespace path `A/B/C`:

- [`A`](/vault/docs/enterprise/namespaces#a) is the top-most namespace and exists under the root namespace for the
  Vault instance.
- [`B`](/vault/docs/enterprise/namespaces#b) is a child namespace of `A` and the parent namespace of `C`.
- [`C`](/vault/docs/enterprise/namespaces#c) is a child namespace of `B` and the grandchild namespace of `A`.

Children can inherit elements from their parent namespaces. For example,
policies for a child namespace might reference entities or groups from the parent
namespace. Parent namespaces can also **assert** policies on identities within
a child namespace.

Vault administrators can configure the desired inheritance behavior with the
[group-policy-application](/vault/api-docs/system/config-group-policy-application)
endpoint of the Vault API.

## Delegation and administrative namespaces

Vault system administrators can assign administration rights to delegate
admins to allow teams to self-manage their namespace. In addition to basic
management, delegate admins can create child namespaces and assign admin rights
to subordinate delegate admins.

Additionally,
[administrative namespaces](/vault/docs/enterprise/namespaces/create-admin-namespace)
let Vault administrators grant access to a
[predefined subset of privileged endpoints](/vault/docs/enterprise/namespaces#privileged-endpoints) by setting
the relevant namespace parameters in their Vault configuration file.

## Vault API and namespaces

Users can perform API operations under a specific namespace by setting the
`X-Vault-Namespace` header to the absolute or relative namespace path. Relative
namespace paths are assumed to be child namespaces of the calling namespace.
You can also provide an absolute namespace path without using the
`X-Vault-Namespace` header.

Vault constructs the fully qualified namespace path based on the calling
namespace and the `X-Vault` header to route the request to the
appropriate namespace. For example, the following requests all route to the
`ns1/ns2/secret/foo` namespace:

1. Path: `ns1/ns2/secret/foo`
2. Path: `secret/foo`, Header: `X-Vault-Namespace: ns1/ns2/`
3. Path: `ns2/secret/foo`, Header: `X-Vault-Namespace: ns1/`

Vault Enterprise has a namespaces API

Use the [/sys/namespaces](/vault/api-docs/system/namespaces) API or
[`namespace`](/vault/docs/commands/namespace) CLI command to manage
your namespaces.

## Restricted API paths

The Vault API includes system backend endpoints, which are mounted under the
`sys/` path. System endpoints let you interact with the internal features of
your Vault instance.

By default, Vault allows non-root calls to the less-sensitive system backend
endpoints. But, for security reasons, Vault restricts access to some of the
system backend endpoints to calls from the root namespace or calls that use a
token in the root namespace with elevated permissions.

Rather than granting access to the full set of privileged `sys/` paths, Vault
administrators can also grant access to a predefined subset of the restricted
endpoints with an administrative namespace.

Note

The CLI commands associated with restricted API paths are also restricted.

| API path | Root | Admin |
| --- | --- | --- |
| `sys/activation-flags/secrets-sync/activate` | YES | NO |
| `sys/audit` | YES | NO |
| `sys/audit-hash` | YES | YES |
| `sys/config/auditing/*` | YES | NO |
| `sys/config/cors` | YES | NO |
| `sys/config/group-policy-application` | YES | YES |
| `sys/config/reload` | YES | NO |
| `sys/config/state` | YES | NO |
| `sys/config/ui` | YES | NO |
| `sys/decode-token` | YES | NO |
| `sys/experiments` | YES | NO |
| `sys/generate-recovery-token` | YES | NO |
| `sys/generate-root` | YES | NO |
| `sys/health` | YES | NO |
| `sys/host-info` | YES | NO |
| `sys/in-flight-req` | YES | NO |
| `sys/init` | YES | NO |
| `sys/internal/counters/activity` | YES | NO |
| `sys/internal/counters/activity/monthly` | YES | NO |
| `sys/internal/counters/config` | YES | NO |
| `sys/internal/inspect/router/*` | YES | NO |
| `sys/key-status` | YES | NO |
| `sys/loggers` | YES | NO |
| `sys/managed-keys/*` | YES | NO |
| `sys/metrics` | YES | NO |
| `sys/mfa/method/*` | YES | NO |
| `sys/monitor` | YES | YES |
| `sys/pprof/*` | YES | NO |
| `sys/quotas/config` | YES | YES |
| `sys/quotas/lease-count` | YES | YES |
| `sys/quotas/rate-limit` | YES | YES |
| `sys/raw` | YES | NO |
| `sys/rekey/*` | YES | NO |
| `sys/rekey-recovery-key` | YES | NO |
| `/sys/replication/dr/primary/*` | YES | NO |
| `/sys/replication/dr/secondary/*` | YES | NO |
| `/sys/replication/performance/primary/*` | YES | NO |
| `/sys/replication/performance/secondary/*` | YES | NO |
| `sys/replication/recover` | YES | NO |
| `sys/replication/reindex` | YES | NO |
| `sys/replication/status` | YES | NO |
| `sys/replication/merkle-check` | YES | NO |
| `sys/rotate/config` | YES | NO |
| `sys/rotate` | YES | NO |
| `sys/seal` | YES | NO |
| `sys/sealwrap/rewrap` | YES | NO |
| `sys/step-down` | YES | NO |
| `sys/storage` | YES | NO |
| `sys/sync/config | YES | YES |
| `sys/unseal` | YES | NO |

Privileged CLI commands without public API endpoints:

| CLI command | Root | Admin |
| --- | --- | --- |
| `vault plugin runtime` | YES | NO |

## Learn more

Refer to the following tutorials to learn more about Vault namespaces:

- [Secure Multi-Tenancy with Namespaces](/vault/tutorials/enterprise/namespaces)
- [Secrets Management Across Namespaces without Hierarchical
  Relationship](/vault/tutorials/enterprise/namespaces-secrets-sharing)
- [Vault Namespace and Mount Structuring
  Guide](/vault/tutorials/enterprise/namespace-structure)
- [HCP Vault Dedicated namespace
  considerations](/vault/tutorials/cloud-ops/hcp-vault-namespace-considerations)
- [Using many Namespaces](/vault/docs/enterprise/namespaces/namespace-limits)

[Edit this page on GitHub](https://github.com/hashicorp/web-unified-docs/blob/main/content/vault/v1.21.x/content/docs/enterprise/namespaces/index.mdx)