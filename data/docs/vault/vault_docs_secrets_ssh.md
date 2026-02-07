# Source: https://developer.hashicorp.com/vault/docs/secrets/ssh

v1.21.x (latest)

- Vault
- [v1.20.x](/vault/docs/v1.20.x/secrets/ssh)
- [v1.19.x](/vault/docs/v1.19.x/secrets/ssh)
- [v1.18.x](/vault/docs/v1.18.x/secrets/ssh)
- [v1.17.x](/vault/docs/v1.17.x/secrets/ssh)
- [v1.16.x](/vault/docs/v1.16.x/secrets/ssh)
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

# SSH secrets engine

The Vault SSH secrets engine provides secure authentication and authorization
for access to machines via the SSH protocol. The Vault SSH secrets engine helps
manage access to machine infrastructure, providing several ways to issue SSH
credentials.

The Vault SSH secrets engine supports the following modes. Each mode is
individually documented on its own page.

- [Signed SSH Certificates](/vault/docs/secrets/ssh/signed-ssh-certificates)
- [One-time SSH Passwords](/vault/docs/secrets/ssh/one-time-ssh-passwords)

All guides assume a basic familiarity with the SSH protocol.

## Removal of dynamic keys feature

Per [Vault 1.12's deprecation notice page](/vault/docs/v1.12.x/deprecation),
the dynamic keys functionality of this engine has been removed in Vault 1.13.

## API

The SSH secrets engine has a full HTTP API. Please see the
[SSH secrets engine API](/vault/api-docs/secret/ssh) for more
details.

[Edit this page on GitHub](https://github.com/hashicorp/web-unified-docs/blob/main/content/vault/v1.21.x/content/docs/secrets/ssh/index.mdx)