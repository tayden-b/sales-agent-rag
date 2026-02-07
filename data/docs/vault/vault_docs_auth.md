# Source: https://developer.hashicorp.com/vault/docs/auth

v1.21.x (latest)

- Vault
- [v1.20.x](/vault/docs/v1.20.x/auth)
- [v1.19.x](/vault/docs/v1.19.x/auth)
- [v1.18.x](/vault/docs/v1.18.x/auth)
- [v1.17.x](/vault/docs/v1.17.x/auth)
- [v1.16.x](/vault/docs/v1.16.x/auth)
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

# Auth methods

Auth methods are the components in Vault that perform authentication and are
responsible for assigning identity and a set of policies to a user. In all cases,
Vault will enforce authentication as part of the request processing. In most cases,
Vault will delegate the authentication administration and decision to the relevant configured
external auth method (e.g., Amazon Web Services, GitHub, Google Cloud Platform, Kubernetes, Microsoft
Azure, Okta ...).

Having multiple auth methods enables you to use an auth method that makes the
most sense for your use case of Vault and your organization.

To learn more about authentication, see the
[authentication concepts page](/vault/docs/concepts/auth).

## Enabling/Disabling auth methods

Auth methods can be enabled/disabled using the CLI or the API.

```
$ vault auth enable userpass
```

When enabled, auth methods are similar to [secrets engines](/vault/docs/secrets):
they are mounted within the Vault mount table and can be accessed
and configured using the standard read/write API. All auth methods are mounted underneath the `auth/` prefix.

By default, auth methods are mounted to `auth/<type>`. For example, if you
enable "github", then you can interact with it at `auth/github`. However, this
path is customizable, allowing users with advanced use cases to mount a single
auth method multiple times.

```
$ vault auth enable -path=my-login userpass
```

When an auth method is disabled, all users authenticated via that method are
automatically logged out.

## External auth method considerations

When using an external auth method (e.g., GitHub), Vault will call the external service
at the time of authentication and for subsequent token renewals. If the status
of an entity changes in the external system (e.g., an account expires or is
disabled), Vault denies requests to **renew** tokens associated with the entity.
However, any existing token remain valid for the original grant period unless
they are explicitly revoked within Vault. Operators should set appropriate
[token TTLs](/vault/docs/concepts/tokens#the-general-case) when using external
authN methods.

[Edit this page on GitHub](https://github.com/hashicorp/web-unified-docs/blob/main/content/vault/v1.21.x/content/docs/auth/index.mdx)