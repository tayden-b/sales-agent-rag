# Vault Enterprise Features

## Namespaces

Namespaces provide tenant isolation within a single Vault cluster. Each namespace acts as an isolated Vault environment with its own:
- Auth methods
- Secrets engines
- Policies
- Tokens
- Identity entities and groups

Use cases:
- Multi-tenant environments (each team or business unit gets a namespace)
- Environment isolation (dev/staging/prod within one cluster)
- Delegated administration (namespace admins manage their own space)

Configuration:
```
vault namespace create engineering
vault namespace create engineering/frontend
```

## Performance Replication

Performance replication allows Vault clusters to replicate data across data centers for read scaling and disaster preparedness.

Architecture:
- One primary cluster handles all writes
- Performance secondary clusters handle local reads
- Secrets engines and auth methods are replicated
- Tokens are local to each cluster (not replicated)

Benefits:
- Low-latency reads from geographically close clusters
- Horizontal read scaling
- Disaster preparedness (secondaries can be promoted)

## Disaster Recovery (DR) Replication

DR replication creates a hot standby cluster that can be promoted if the primary fails.

Key differences from performance replication:
- DR secondaries do not handle client requests
- DR secondaries replicate everything (including tokens)
- Promotion is manual (or automated via Vault Autopilot)
- Used for true disaster recovery, not read scaling

## Sentinel Policies

Sentinel is a policy-as-code framework that enables fine-grained, logic-based policy decisions.

Examples of Sentinel policies:
- Restrict secret access to business hours only
- Require MFA for accessing high-sensitivity secrets
- Limit certificate TTLs based on environment
- Enforce naming conventions for secrets paths

## Control Groups

Control groups add an additional authorization layer requiring multiple approvals before access is granted.

Workflow:
1. User requests access to a secret
2. Vault creates an authorization request
3. Designated approvers receive a notification
4. Required number of approvers grant authorization
5. User can access the secret with the authorized token

## Licensing

Vault Enterprise requires a license. License features are tiered:
- **Standard**: Namespaces, Sentinel, MFA
- **Plus**: Performance Replication, Read Replicas
- **Premium**: DR Replication, FIPS compliance, HSM support
