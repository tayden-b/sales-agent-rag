# Source: https://developer.hashicorp.com/vault/docs/secrets

v1.21.x (latest)

- Vault
- [v1.20.x](/vault/docs/v1.20.x/secrets)
- [v1.19.x](/vault/docs/v1.19.x/secrets)
- [v1.18.x](/vault/docs/v1.18.x/secrets)
- [v1.17.x](/vault/docs/v1.17.x/secrets)
- [v1.16.x](/vault/docs/v1.16.x/secrets)
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

# Secrets engines

Secrets engines are components which store, generate, or encrypt data. Secrets
engines are incredibly flexible, so it is easiest to think about them in terms
of their function. Secrets engines are provided some set of data, they take some
action on that data, and they return a result.

Some secrets engines simply store and read data - like encrypted
Redis/Memcached. Other secrets engines connect to other services and generate
dynamic credentials on demand. Other secrets engines provide encryption as a
service, totp generation, certificates, and much more.

Secrets engines are enabled at a **path** in Vault. When a request comes to
Vault, the router automatically routes anything with the route prefix to the
secrets engine. In this way, each secrets engine defines its own paths and
properties. To the user, secrets engines behave similar to a virtual filesystem,
supporting operations like read, write, and delete.

## Secrets engines lifecycle

Most secrets engines can be enabled, disabled, tuned, and moved via the CLI or
API.

- [Enable](/vault/docs/commands/secrets/enable) - This enables a secrets engine at
  a given path. With a few exceptions, secrets engines can be enabled at multiple
  paths. Each secrets engine is isolated to its path. By default, they are
  enabled at their "type" (e.g. "aws" enables at `aws/`).

  **Case-sensitive:** The path where you enable secrets engines is case-sensitive. For
  example, the KV secrets engine enabled at `kv/` and `KV/` are treated as two
  distinct instances of KV secrets engine.
- [Disable](/vault/docs/commands/secrets/disable) - This disables an existing
  secrets engine. When a secrets engine is disabled, all of its secrets are
  revoked (if they support it), and all the data stored for that engine in
  the physical storage layer is deleted.
- [Move](/vault/docs/commands/secrets/move) - This moves the path for an existing
  secrets engine. This process revokes all secrets, since secret leases are tied
  to the path where they were created. The configuration data stored for the engine
  persists through the move.
- [Tune](/vault/docs/commands/secrets/tune) - This tunes global configuration for
  the secrets engine such as the TTLs.

Once a secrets engine is enabled, you can interact with it directly at its path
according to its own API. Use `vault path-help` to determine the paths it
responds to.

Note that mount points cannot conflict with each other in Vault. There are
two broad implications of this fact. The first is that you cannot have
a mount which is prefixed with an existing mount. The second is that you
cannot create a mount point that is named as a prefix of an existing mount.
As an example, the mounts `foo/bar` and `foo/baz` can peacefully coexist
with each other whereas `foo` and `foo/baz` cannot

## Barrier view

Secrets engines receive a *barrier view* to the configured Vault physical
storage. This is a lot like a [chroot](https://en.wikipedia.org/wiki/Chroot).

When a secrets engine is enabled, a random UUID is generated. This becomes the
data root for that engine. Whenever that engine writes to the physical storage
layer, it is prefixed with that UUID folder. Since the Vault storage layer
doesn't support relative access (such as `../`), this makes it impossible for an
enabled secrets engine to access other data.

This is an important security feature in Vault - even a malicious engine
cannot access the data from any other engine.

[Edit this page on GitHub](https://github.com/hashicorp/web-unified-docs/blob/main/content/vault/v1.21.x/content/docs/secrets/index.mdx)