# Source: https://developer.hashicorp.com/vault/docs/secrets/kv

v1.21.x (latest)

- Vault
- [v1.20.x](/vault/docs/v1.20.x/secrets/kv)
- [v1.19.x](/vault/docs/v1.19.x/secrets/kv)
- [v1.18.x](/vault/docs/v1.18.x/secrets/kv)
- [v1.17.x](/vault/docs/v1.17.x/secrets/kv)
- [v1.16.x](/vault/docs/v1.16.x/secrets/kv)
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

# KV secrets engine

The `kv` secrets engine is a generic key-value store used to store arbitrary
secrets within the configured physical storage for Vault. This secrets engine
can run in one of two modes; store a single value for a key, or store a number
of versions for each key and maintain the record of them.

## KV version 1

When running the `kv` secrets engine non-versioned, it stores the most recently
written value for a key. Any update will overwrite the original value and not
recoverable. The benefits of non-versioned `kv` is a reduced storage size for
each key since no additional metadata or history is stored. Additionally, it
gives better runtime performance because the requests require fewer storage
calls and no locking.

Refer to the [KV version 1 Docs](/vault/docs/secrets/kv/kv-v1) for more
information.

## KV version 2

When running v2 of the `kv` secrets engine, a key can retain a configurable
number of versions. The default is 10 versions. The older versions' metadata and
data can be retrieved. Additionally, it provides check-and-set operations to
prevent overwriting data unintentionally.

When a version is deleted, the underlying data is not removed, rather it is
marked as deleted. Deleted versions can be undeleted. To permanently remove a
version's data, use the `vault kv destroy` command or the API endpoint. You can
delete all versions and metadata for a key by deleting the metadata using the
`vault kv metadata delete` command or the API endpoint with DELETE verb. You can
restrict who has permissions to soft delete, undelete, or fully remove data with
[Vault policies](/vault/docs/concepts/policies).

Refer to the [KV version 2 Docs](/vault/docs/secrets/kv/kv-v2) for more
information.

## Version comparison

Regardless of its version, you use the [`vault kv`](/vault/docs/commands/kv)
command to interact with KV secrets engine. However, the API endpoint are
different. You must be aware of those differences to write policies as intended.

The following table lists the `vault kv` sub-commands and their respective API
endpoints assuming the KV secrets engine is enabled at `secret/`.

| Command | KV v1 endpoint | KV v2 endpoint |
| --- | --- | --- |
| `vault kv get` | secret/<key\_path> | secret/**data**/<key\_path> |
| `vault kv put` | secret/<key\_path> | secret/**data**/<key\_path> |
| `vault kv list` | secret/<key\_path> | secret/**metadata**/<key\_path> |
| `vault kv delete` | secret/<key\_path> | secret/**data**/<key\_path> |

In addition, KV v2 has sub-commands to handle versioning of secrets.

| Command | KV v2 endpoint |
| --- | --- |
| `vault kv patch` | secret/**data**/<key\_path> |
| `vault kv rollback` | secret/**data**/<key\_path> |
| `vault kv undelete` | secret/**undelete**/<key\_path> |
| `vault kv destroy` | secret/**destroy**/<key\_path> |
| `vault kv metadata` | secret/**metadata**/<key\_path> |

To reduce confusion, the CLI command outputs the secret path when you are
working with KV v2.

**Example:**

```
$ vault kv put secret/web-app api-token="WEOIRJ13895130WENJWEFN"

=== Secret Path ===
secret/data/web-app

======= Metadata =======
Key                Value
---                -----
created_time       2024-07-02T00:34:58.074825Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            1
```

You can use `-mount` flag if omitting `/data/` in the CLI command is confusing.

```
$ vault kv put -mount=secret web-app api-token="WEOIRJ13895130WENJWEFN"
```

[Edit this page on GitHub](https://github.com/hashicorp/web-unified-docs/blob/main/content/vault/v1.21.x/content/docs/secrets/kv/index.mdx)