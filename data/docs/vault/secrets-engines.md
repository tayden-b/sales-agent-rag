# Vault Secrets Engines

## Overview

Secrets engines are components which store, generate, or encrypt data. Secrets engines are enabled at a "path" in Vault. When a request comes to Vault, the router automatically routes anything with the route prefix to the secrets engine.

## Key-Value Secrets Engine

The KV secrets engine is used to store arbitrary secrets within the configured physical storage for Vault. Writing to a key in the kv backend will replace the old value; sub-fields are not merged together.

### KV Version 2

KV v2 provides versioning of secrets. This allows you to maintain a configurable number of secret versions. The default is 10 versions.

To enable KV v2:
```
vault secrets enable -version=2 kv
```

Key features:
- Secret versioning (configurable number of versions)
- Check-and-set operations to prevent overwriting
- Soft deletes with undelete capability
- Metadata tracking per secret version

### Secret Rotation

Vault can automatically rotate secrets for supported backends. Dynamic secrets are generated on-demand and automatically revoked after a configurable lease period.

Benefits of dynamic secrets:
- No long-lived credentials to manage
- Automatic revocation reduces blast radius
- Audit trail for every credential issued
- Unique credentials per application/service

## Database Secrets Engine

The database secrets engine generates database credentials dynamically based on configured roles. It works with PostgreSQL, MySQL, MongoDB, MSSQL, and many other databases.

Configuration steps:
1. Enable the database secrets engine
2. Configure the database connection
3. Create roles that define credential parameters
4. Applications request credentials through Vault

Example for PostgreSQL:
```
vault write database/config/my-postgresql-database \
    plugin_name=postgresql-database-plugin \
    connection_url="postgresql://{{username}}:{{password}}@localhost:5432/mydb" \
    allowed_roles="my-role" \
    username="vault_admin" \
    password="vault_password"
```

## Transit Secrets Engine

The transit secrets engine handles cryptographic functions on data in-transit. Vault doesn't store the data sent to the transit engine — it only encrypts and returns the ciphertext.

Use cases:
- Encryption as a service
- Data tokenization
- Key management and rotation
- Signing and verification

## PKI Secrets Engine

The PKI secrets engine generates dynamic X.509 certificates. This removes the need for manual certificate management and allows for short-lived certificates.

Benefits:
- Automated certificate issuance
- Short-lived certificates reduce risk
- No manual CSR/signing workflow
- Integration with service mesh (Consul Connect)
