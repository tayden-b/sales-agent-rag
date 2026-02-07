# Source: https://developer.hashicorp.com/terraform/language/state/locking

v1.14.x (latest)

- Terraform
- [v1.15.x (alpha)](/terraform/language/v1.15.x/state/locking)
- [v1.13.x](/terraform/language/v1.13.x/state/locking)
- [v1.12.x](/terraform/language/v1.12.x/state/locking)
- [v1.11.x](/terraform/language/v1.11.x/state/locking)
- [v1.10.x](/terraform/language/v1.10.x/state/locking)
- [v1.9.x](/terraform/language/v1.9.x/state/locking)
- [v1.8.x](/terraform/language/v1.8.x/state/locking)
- [v1.7.x](/terraform/language/v1.7.x/state/locking)
- [v1.6.x](/terraform/language/v1.6.x/state/locking)
- [v1.5.x](/terraform/language/v1.5.x/state/locking)
- [v1.4.x](/terraform/language/v1.4.x/state/locking)
- [v1.3.x](/terraform/language/v1.3.x/state/locking)
- [v1.2.x](/terraform/language/v1.2.x/state/locking)
- [v1.1.x](/terraform/language/v1.1.x/state/locking)

# State Locking

If supported by your [backend](/terraform/language/backend), Terraform will lock your
state for all operations that could write state. This prevents
others from acquiring the lock and potentially corrupting your state.

State locking happens automatically on all operations that could write
state. You do not see any message that it happens. If state locking fails,
Terraform does not continue. You can disable state locking for most commands
with the `-lock=false` flag, but we do not recommend it.

If acquiring the lock takes longer than expected, Terraform outputs
a status message. If Terraform does not output a message, state locking is
still occurring if your backend supports it.

Not all backends support locking. The
[documentation for each backend](/terraform/language/backend)
includes details on whether it supports locking or not.

## Force Unlock

Terraform has a [force-unlock command](/terraform/cli/commands/force-unlock)
to manually unlock the state if unlocking failed.

**Be very careful with this command.** If you unlock the state when someone
else is holding the lock it could cause multiple writers. Force unlock should
only be used to unlock your own lock in the situation where automatic
unlocking failed.

To protect you, the `force-unlock` command requires a unique lock ID. Terraform
will output this lock ID if unlocking fails. This lock ID acts as a
[nonce](https://en.wikipedia.org/wiki/Cryptographic_nonce), ensuring
that locks and unlocks target the correct lock.

[Edit this page on GitHub](https://github.com/hashicorp/web-unified-docs/blob/main/content/terraform/v1.14.x/docs/language/state/locking.mdx)