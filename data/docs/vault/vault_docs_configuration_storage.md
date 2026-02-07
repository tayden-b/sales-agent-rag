# Source: https://developer.hashicorp.com/vault/docs/configuration/storage

v1.21.x (latest)

- Vault
- [v1.20.x](/vault/docs/v1.20.x/configuration/storage)
- [v1.19.x](/vault/docs/v1.19.x/configuration/storage)
- [v1.18.x](/vault/docs/v1.18.x/configuration/storage)
- [v1.17.x](/vault/docs/v1.17.x/configuration/storage)
- [v1.16.x](/vault/docs/v1.16.x/configuration/storage)
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

# storage stanza

The `storage` stanza configures the storage backend, which represents the
location for the durable storage of Vault's information. Each backend has pros,
cons, advantages, and trade-offs. For example, some backends support high
availability while others provide a more robust backup and restoration process.
For information about a specific backend, choose one from the navigation on the
left.

## Configuration

Storage backend configuration is done through the Vault configuration file using
the `storage` stanza:

```
storage [NAME] {
  [PARAMETERS...]
}
```

For example:

```
storage "file" {
  path = "/mnt/vault/data"
}
```

For configuration options which also read an environment variable, the
environment variable will take precedence over values in the configuration
file.

## Integrated storage vs. external storage

HashiCorp recommends using Vault's [integrated
storage](/vault/docs/configuration/storage/raft) for most use cases rather than
configuring another system to store Vault data externally. (Integrated Storage is
an **embedded Vault data storage** available in Vault 1.4 or later.) Prior to Vault 1.4, Consul was the recommended Vault storage.

**NOTE:** [HCP Vault Dedicated](https://cloud.hashicorp.com/products/vault) clusters
use Integrated Storage as their storage backend.

The table below compares the characteristics of Integrated Storage and External
Storage. Suppose you decide that the additional operational complexity of external storage is worth it for your use case. In that case, there are several external storage options to choose from (e.g., [Consul](/vault/docs/configuration/storage/consul), [DynamoDB](/vault/docs/configuration/storage/dynamodb), etc.).

|  | Integrated Storage | External Storage |
| --- | --- | --- |
| HashiCorp Supported | Yes | Limited support |
| Operation | Operationally simpler with no additional software installation required. | Must install and configure the external storage environment outside of Vault. For high availability, the external storage should be clustered. |
| Networking | One less network hop. | Extra network hop between Vault and the external storage system (e.g., Consul cluster). |
| Troubleshooting and monitoring | Integrated Storage is a part of Vault; therefore, Vault is the only system you need to monitor and troubleshoot. | The source of failure could be the external storage; therefore, you need to check the health of both Vault and the external storage. This requires expertise in the chosen storage backend and additional monitoring of that storage. |
| Data location | The encrypted Vault data is stored on the same host where the Vault server process runs. | The encrypted Vault data is stored where the external storage is located. Therefore, the Vault server and the data storage are hosted on physically separate hosts. |
| System requirements | Avoid "burstable" CPU and storage options. SSDs should be used for the hard drive.  See the [Reference Architecture](/vault/tutorials/day-one-raft/raft-reference-architecture#system-requirements) guide. | Follow the system requirements given by your chosen storage backend. |

### Integrated storage vs. consul as Vault storage

[HashiCorp Consul](/consul/docs/intro) is a comprehensive
multi-cloud service networking solution including service mesh, service
discovery, and network infrastructure automation. Vault can leverage
Consul's [KV Store](/consul/api-docs/kv) to persist Vault data.

The table below highlights the differences between Integrated Storage and
Consul.

|  | Integrated Storage | Consul |
| --- | --- | --- |
| Deployment | Vault cluster is all you need. | Vault cluster & Consul cluster.  Use a dedicated Consul cluster for Vault storage, and it should not be used for other purposes (e.g., service discovery, service mesh).  See the [Vault with Consul Storage Reference Architecture](/vault/tutorials/day-one-consul/reference-architecture#recommended-architecture) guide. |
| Data location | Data is on disk. | All data is in memory. |
| System requirements | [System requirements](/vault/tutorials/day-one-raft/raft-reference-architecture#system-requirements) | [System requirements](/vault/tutorials/day-one-consul/reference-architecture#hardware-sizing-for-vault-servers) |
| Snapshots | Normal data backup strategy of your organization. | More frequent snapshots are necessary since data is in memory. |
| Max message size | 1 MiB (Configurable using the [`max_entry_size`](/vault/docs/configuration/storage/raft#max_entry_size) parameter) | 512 KiB (Configurable using the [`kv_max_value_size`](/consul/docs/agent/config/config-files#kv_max_value_size) parameter) |

If you have a Vault cluster using Consul as its storage backend and wish to
migrate to Integrated Storage, read the following tutorials:

1. [Preflight Checklist - Migrating to Integrated
   Storage](/vault/tutorials/raft/storage-migration-checklist)
2. [Storage Migration tutorial - Consul to Integrated
   Storage](/vault/tutorials/raft/raft-migration)

## Tutorial

Refer to the [Integrated
Storage](/vault/tutorials/raft) tutorials
to learn more about Integrated Storage.

[Edit this page on GitHub](https://github.com/hashicorp/web-unified-docs/blob/main/content/vault/v1.21.x/content/docs/configuration/storage/index.mdx)