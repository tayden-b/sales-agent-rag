# Source: https://developer.hashicorp.com/vault/docs/secrets/kv/kv-v2

v1.21.x (latest)

- Vault
- [v1.20.x](/vault/docs/v1.20.x/secrets/kv/kv-v2)
- [v1.19.x](/vault/docs/v1.19.x/secrets/kv/kv-v2)
- [v1.18.x](/vault/docs/v1.18.x/secrets/kv/kv-v2)
- [v1.17.x](/vault/docs/v1.17.x/secrets/kv/kv-v2)
- [v1.16.x](/vault/docs/v1.16.x/secrets/kv/kv-v2)
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

# Key/Value v2 plugin

The key/value (`kv`) secrets engine stores and versions arbitrary static secrets
stored in Vault physical storage.

The `kv` v2 plugin uses soft deletes to make data inaccessible while allowing
data recovery. When an entry is permanently deleted, Vault purges the underlying
version data and marks the key metadata as destroyed.

How-to guidesCookbookReferenceTutorials

Step-by-step instructions:

- [Upgrade from `kv` v1](/vault/docs/secrets/kv/kv-v2/upgrade)
- [Set up the `kv` v2 plugin](/vault/docs/secrets/kv/kv-v2/setup)

Basic examples:

- [Read data](/vault/docs/secrets/kv/kv-v2/cookbook/read-data)
- [Set max data versions](/vault/docs/secrets/kv/kv-v2/cookbook/max-versions)
- [Write data](/vault/docs/secrets/kv/kv-v2/cookbook/write-data)
- [Patch and update data](/vault/docs/secrets/kv/kv-v2/cookbook/patch-data)
- [Read subkeys](/vault/docs/secrets/kv/kv-v2/cookbook/read-subkey)
- [Soft delete data](/vault/docs/secrets/kv/kv-v2/cookbook/delete-data)
- [Restore soft deleted data](/vault/docs/secrets/kv/kv-v2/cookbook/undelete-data)
- [Destroy data](/vault/docs/secrets/kv/kv-v2/cookbook/destroy-data)
- [Write custom metadata](/vault/docs/secrets/kv/kv-v2/cookbook/custom-metadata)

Technical references:

- [KV v2 CLI commands](/vault/docs/commands/kv)
- [KV v2 plugin API docs](/vault/api-docs/secret/kv/kv-v2)

Detailed tutorials:

- [Versioned Key Value Secrets Engine](/vault/tutorials/secrets-management/versioned-kv) -
  Learn how to compare data in the KV v2 secrets engine and protect data from
  accidental deletion.

[Edit this page on GitHub](https://github.com/hashicorp/web-unified-docs/blob/main/content/vault/v1.21.x/content/docs/secrets/kv/kv-v2/index.mdx)