# Source: https://developer.hashicorp.com/vault/docs/auth/userpass

v1.21.x (latest)

- Vault
- [v1.20.x](/vault/docs/v1.20.x/auth/userpass)
- [v1.19.x](/vault/docs/v1.19.x/auth/userpass)
- [v1.18.x](/vault/docs/v1.18.x/auth/userpass)
- [v1.17.x](/vault/docs/v1.17.x/auth/userpass)
- [v1.16.x](/vault/docs/v1.16.x/auth/userpass)
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

# Userpass auth method

Supports custom GUI login

This method can be chosen as a default or backup login method for Vault Enterprise GUI users.
Refer to the [Manage custom login options](/vault/docs/ui/custom-login) guide for more details.

The `userpass` auth method allows users to authenticate with Vault using
a username and password combination.

The username/password combinations are configured directly to the auth
method using the `users/` path. This method cannot read usernames and
passwords from an external source.

The method lowercases all submitted usernames, e.g. `Mary` and `mary` are the
same entry.

This documentation assumes the Username & Password method is mounted at the default `/auth/userpass`
path in Vault. Since it is possible to enable auth methods at any location,
please update your CLI calls accordingly with the `-path` flag.

## Authentication

### Via the CLI

```
$ vault login -method=userpass \
    username=mitchellh \
    password=foo
```

### Via the API

```
$ curl \
    --request POST \
    --data '{"password": "foo"}' \
    http://127.0.0.1:8200/v1/auth/userpass/login/mitchellh
```

The response will contain the token at `auth.client_token`:

```
{
  "lease_id": "",
  "renewable": false,
  "lease_duration": 0,
  "data": null,
  "auth": {
    "client_token": "c4f280f6-fdb2-18eb-89d3-589e2e834cdb",
    "policies": ["admins"],
    "metadata": {
      "username": "mitchellh"
    },
    "lease_duration": 0,
    "renewable": false
  }
}
```

## Configuration

Auth methods must be configured in advance before users or machines can
authenticate. These steps are usually completed by an operator or configuration
management tool.

1. Enable the userpass auth method:

   ```
   $ vault auth enable userpass
   ```

   Enable the `userpass` auth method at the default `auth/userpass` path.
   You can choose to enable the auth method at a different path with the `-path` flag:

   ```
   $ vault auth enable -path=<path> userpass
   ```
2. Configure it with users that are allowed to authenticate:

   ```
   $ vault write auth/<userpass:path>/users/mitchellh \
       password=foo \
       policies=admins
   ```

   This creates a new user "mitchellh" with the password "foo" that will be
   associated with the "admins" policy. This is the only configuration
   necessary.

## User lockout

If a user provides bad credentials several times in quick succession,
Vault will stop trying to validate their credentials for a while, instead returning immediately
with a permission denied error. We call this behavior "user lockout". The time for which
a user will be locked out is called “lockout duration”. The user will be able to login after the lockout
duration has passed. The number of failed login attempts after which the user is locked out is called
“lockout threshold”. The lockout threshold counter is reset to zero after a few minutes without login attempts,
or upon a successful login attempt. The duration after which the counter will be reset to zero
after no login attempts is called "lockout counter reset". This can defeat both automated and targeted requests
i.e, user-based password guessing attacks as well as automated attacks.

Note

User lockout occurs early in request processing and may leak
information about the validity or existence of valid, existing user account
names.

The user lockout feature is enabled by default. The default values for "lockout threshold" is 5 attempts,
"lockout duration" is 15 minutes, "lockout counter reset" is 15 minutes.

The user lockout feature can be disabled as follows:

- It can be disabled globally using environment variable `VAULT_DISABLE_USER_LOCKOUT`.
- It can be disabled for all supported auth methods (ldap, userpass and approle) or a specific supported auth method using the `disable_lockout`
  parameter within `user_lockout` stanza in configuration file.
  Please see [user lockout configuration](/vault/docs/configuration/user-lockout#user_lockout-stanza) for more details.
- It can be disabled for a specific auth mount using "auth tune". Please see [auth tune command](/vault/docs/commands/auth/tune)
  or [auth tune api](/vault/api-docs/system/auth#tune-auth-method) for more details.

**NOTE**: This feature is available from Vault version 1.13 and is only supported by the userpass, ldap, and approle auth methods.

## API

The Userpass auth method has a full HTTP API. Please see the [Userpass auth
method API](/vault/api-docs/auth/userpass) for more details.

[Edit this page on GitHub](https://github.com/hashicorp/web-unified-docs/blob/main/content/vault/v1.21.x/content/docs/auth/userpass.mdx)