# Source: https://developer.hashicorp.com/vault/docs/auth/ldap

v1.21.x (latest)

- Vault
- [v1.20.x](/vault/docs/v1.20.x/auth/ldap)
- [v1.19.x](/vault/docs/v1.19.x/auth/ldap)
- [v1.18.x](/vault/docs/v1.18.x/auth/ldap)
- [v1.17.x](/vault/docs/v1.17.x/auth/ldap)
- [v1.16.x](/vault/docs/v1.16.x/auth/ldap)
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

# LDAP auth method

Supports custom GUI login

This method can be chosen as a default or backup login method for Vault Enterprise GUI users.
Refer to the [Manage custom login options](/vault/docs/ui/custom-login) guide for more details.

Note

This engine can use external X.509 certificates as part of TLS or signature validation.
Verifying signatures against X.509 certificates that use SHA-1 is deprecated and is no longer
usable without a workaround starting in Vault 1.12. Refer to the
[deprecation notices](/vault/docs/updates/deprecation)
for more information.

The `ldap` auth method allows authentication using an existing LDAP
server and user/password credentials. This allows Vault to be integrated
into environments using LDAP without duplicating the user/pass configuration
in multiple places.

The mapping of groups and users in LDAP to Vault policies is managed by using
the `users/` and `groups/` paths.

## A note on escaping

**It is up to the administrator** to provide properly escaped DNs. This
includes the user DN, bind DN for search, and so on.

The only DN escaping performed by this method is on usernames given at login
time when they are inserted into the final bind DN, and uses escaping rules
defined in RFC 4514.

Additionally, Active Directory has escaping rules that differ slightly from the
RFC; in particular it requires escaping of '#' regardless of position in the DN
(the RFC only requires it to be escaped when it is the first character), and
'=', which the RFC indicates can be escaped with a backslash, but does not
contain in its set of required escapes. If you are using Active Directory and
these appear in your usernames, please ensure that they are escaped, in
addition to being properly escaped in your configured DNs.

For reference, see [RFC 4514](https://www.ietf.org/rfc/rfc4514.txt) and this
[TechNet post on characters to escape in Active
Directory](http://social.technet.microsoft.com/wiki/contents/articles/5312.active-directory-characters-to-escape.aspx).

## Authentication

### Via the CLI

```
$ vault login -method=ldap username=mitchellh
Password (will be hidden):
Successfully authenticated! The policies that are associated
with this token are listed below:

admins
```

### Via the API

```
$ curl \
    --request POST \
    --data '{"password": "foo"}' \
    http://127.0.0.1:8200/v1/auth/ldap/login/mitchellh
```

The response will be in JSON. For example:

```
{
  "lease_id": "",
  "renewable": false,
  "lease_duration": 0,
  "data": null,
  "auth": {
    "client_token": "c4f280f6-fdb2-18eb-89d3-589e2e834cdb",
    "policies": [
      "admins"
    ],
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

1. Enable the ldap auth method:

   ```
   $ vault auth enable ldap
   ```
2. Configure connection details for your LDAP server, information on how to
   authenticate users, and instructions on how to query for group membership. The
   configuration options are categorized and detailed below.

### Connection parameters

- [`url`](/vault/docs/auth/ldap#url) (string, required) - The LDAP server to connect to. Examples: `ldap://ldap.myorg.com`, `ldaps://ldap.myorg.com:636`. This can also be a comma-delineated list of URLs, e.g. `ldap://ldap.myorg.com,ldaps://ldap.myorg.com:636`, in which case the servers will be tried in-order if there are errors during the connection process.
- [`starttls`](/vault/docs/auth/ldap#starttls) (bool, optional) - If true, issues a `StartTLS` command after establishing an unencrypted connection.
- [`insecure_tls`](/vault/docs/auth/ldap#insecure_tls) - (bool, optional) - If true, skips LDAP server SSL certificate verification - insecure, use with caution!
- [`certificate`](/vault/docs/auth/ldap#certificate) - (string, optional) - CA certificate to use when verifying LDAP server certificate, must be x509 PEM encoded.
- [`client_tls_cert`](/vault/docs/auth/ldap#client_tls_cert) - (string, optional) - Client certificate to provide to the LDAP server, must be x509 PEM encoded.
- [`client_tls_key`](/vault/docs/auth/ldap#client_tls_key) - (string, optional) - Client certificate key to provide to the LDAP server, must be x509 PEM encoded.

### Binding parameters

The LDAP auth method supports the following methods for resolving the user object used to authenticate the end user:

- **Search** - Searches the LDAP server directory for the user object based on the provided username. Vault can search in two ways:
  - Authenticated search - The bind user must be set using `binddn` and `bindpass`
  - Anonymous search - `discoverdn` must be set to `true`
- **User Principal Name (UPN)** - UPN is a method of specifying users supported
  by Active Directory. Refer to the
  [User Naming Attributes](https://msdn.microsoft.com/en-us/library/ms677605(v=vs.85).aspx#userPrincipalName)
  page in the Active Directory Domain Services documentation for more UPN
  information.

#### Binding - authenticated search

- [`binddn`](/vault/docs/auth/ldap#binddn) (string, optional) - Distinguished name of object to bind when performing user and group search. Example: `cn=vault,ou=Users,dc=example,dc=com`
- [`bindpass`](/vault/docs/auth/ldap#bindpass) (string, optional) - Password to use along with `binddn` when performing user search.
- [`userdn`](/vault/docs/auth/ldap#userdn) (string, optional) - Base DN under which to perform user search. Example: `ou=Users,dc=example,dc=com`
- [`userattr`](/vault/docs/auth/ldap#userattr) (string, optional) - Attribute on user attribute object matching the username passed when authenticating. Examples: `sAMAccountName`, `cn`, `uid`
- [`userfilter`](/vault/docs/auth/ldap#userfilter) (string, optional) - Go template used to construct a ldap user search filter. The template can access the following context variables: [`UserAttr`, `Username`]. The default userfilter is `({{.UserAttr}}={{.Username}})` or `(userPrincipalName={{.Username}}@UPNDomain)` if the `upndomain` parameter is set. The user search filter can be used to restrict what user can attempt to log in. For example, to limit login to users that are not contractors, you could write `(&(objectClass=user)({{.UserAttr}}={{.Username}})(!(employeeType=Contractor)))`.

When specifying a `userfilter`, either the templated value `{{.UserAttr}}` or
the literal value that matches `userattr` should be present in the filter to
ensure that the search returns a unique result that takes `userattr` into
consideration for entity alias mapping purposes and avoid possible collisions on login.

#### Binding - anonymous search

- [`discoverdn`](/vault/docs/auth/ldap#discoverdn) (bool, optional) - If true, use anonymous bind to discover the bind DN of a user
- [`userdn`](/vault/docs/auth/ldap#userdn-1) (string, optional) - Base DN under which to perform user search. Example: `ou=Users,dc=example,dc=com`
- [`userattr`](/vault/docs/auth/ldap#userattr-1) (string, optional) - Attribute on user attribute object matching the username passed when authenticating. Examples: `sAMAccountName`, `cn`, `uid`
- [`userfilter`](/vault/docs/auth/ldap#userfilter-1) (string, optional) - Go template used to construct a ldap user search filter. The template can access the following context variables: [`UserAttr`, `Username`]. The default userfilter is `({{.UserAttr}}={{.Username}})` or `(userPrincipalName={{.Username}}@UPNDomain)` if the `upndomain` parameter is set. The user search filter can be used to restrict what user can attempt to log in. For example, to limit login to users that are not contractors, you could write `(&(objectClass=user)({{.UserAttr}}={{.Username}})(!(employeeType=Contractor)))`.
- [`anonymous_group_search`](/vault/docs/auth/ldap#anonymous_group_search) (bool, optional) - Use anonymous binds when performing LDAP group searches. Defaults to `false`.

When specifying a `userfilter`, either the templated value `{{.UserAttr}}` or
the literal value that matches `userattr` should be present in the filter to
ensure that the search returns a unique result that takes `userattr` into
consideration for entity alias mapping purposes and avoid possible collisions on login.

#### Alias dereferencing

- [`dereference_aliases`](/vault/docs/auth/ldap#dereference_aliases) (string, optional) - Control how aliases are dereferenced when performing the search. Possible values are: `never`, `finding`, `searching`, and `always`. `finding` will only dereference aliases during name resolution of the base. `searching` will dereference aliases after name resolution.

#### Binding - user principal name (AD)

- [`upndomain`](/vault/docs/auth/ldap#upndomain) (string, optional) - userPrincipalDomain used to construct the UPN string for the authenticating user. The constructed UPN will appear as `[username]@UPNDomain`. Example: `example.com`, which will cause vault to bind as `username@example.com`.
- [`enable_samaccountname_login`](/vault/docs/auth/ldap#enable_samaccountname_login) `(bool: false)` - (Optional) Lets Active Directory
  LDAP users log in using `sAMAccountName` or `userPrincipalName` when the
  `upndomain` parameter is set.

### Certificates

At startup, Vault can read LDAP certificates from the operating systems (OS)
certificate trust store instead of reading CA certificates from the
certificate parameter. After startup, you need to restart Vault to read in
new certificates before the LDAP plugin can use the information to establish new
LDAP connections to the configured server address.

### Group membership resolution

Once a user has been authenticated, the LDAP auth method must know how to resolve which groups the user is a member of. The configuration for this can vary depending on your LDAP server and your directory schema. There are two main strategies when resolving group membership - the first is searching for the authenticated user object and following an attribute to groups it is a member of. The second is to search for group objects of which the authenticated user is a member of. Both methods are supported.

- [`groupfilter`](/vault/docs/auth/ldap#groupfilter) (string, optional) - Go template used when constructing the group membership query. The template can access the following context variables: [`UserDN`, `Username`]. The default is `(|(memberUid={{.Username}})(member={{.UserDN}})(uniqueMember={{.UserDN}}))`, which is compatible with several common directory schemas. To support nested group resolution for Active Directory, instead use the following query: `(&(objectClass=group)(member:1.2.840.113556.1.4.1941:={{.UserDN}}))`.
- [`groupdn`](/vault/docs/auth/ldap#groupdn) (string, required) - LDAP search base to use for group membership search. This can be the root containing either groups or users. Example: `ou=Groups,dc=example,dc=com`
- [`groupattr`](/vault/docs/auth/ldap#groupattr) (string, optional) - LDAP attribute to follow on objects returned by `groupfilter` in order to enumerate user group membership. Examples: for groupfilter queries returning *group* objects, use: `cn`. For queries returning *user* objects, use: `memberOf`. The default is `cn`.

*Note*: When using *Authenticated Search* for binding parameters (see above) the distinguished name defined for `binddn` is used for the group search. Otherwise, the authenticating user is used to perform the group search.

Use `vault path-help` for more details.

### Root secret rotation

Enterprise

Appropriate [Vault Enterprise](https://www.hashicorp.com/products/vault/pricing)  license required

- [`rotation_schedule`](/vault/docs/auth/ldap#rotation_schedule) (string: "") - The schedule, in
  [cron-style time format](https://en.wikipedia.org/wiki/Cron), defining the
  schedule on which Vault should rotate the root token.
- [`rotation_window`](/vault/docs/auth/ldap#rotation_window) (string: "") - The maximum amount of time, in
  [duration format](https://pkg.go.dev/time#ParseDuration), allowed to complete
  a rotation when a scheduled token rotation occurs.
- [`rotation_period`](/vault/docs/auth/ldap#rotation_period) (string: "") - The amount of time, in
  [duration format](https://pkg.go.dev/time#ParseDuration), Vault should wait
  before rotating the root credential.
- [`rotation_url`](/vault/docs/auth/ldap#rotation_url) `(string: "")` – The LDAP server to perform a root config password
  rotation on if it is different from the `url` parameter. See (#rotation-url) for more details.

### Other

- [`username_as_alias`](/vault/docs/auth/ldap#username_as_alias) (bool, optional) - If set to true, forces the auth method to use the username passed by the user as the alias name.
- [`max_page_size`](/vault/docs/auth/ldap#max_page_size) (int, optional) - If set to a value greater than 0, the LDAP backend will use the LDAP server's paged search control to request pages of up to the given size. This can be used to avoid hitting the LDAP server's maximum result size limit. Otherwise, the LDAP backend will not use the paged search control.

## Root credential rotation

The root bindpass can be rotated to a Vault-generated value that is not accessible by the operator.
This will ensure that only Vault is able to access the "root" user that Vault uses to manipulate credentials.

Manual root rotations will be logged to the vault.log and state that the rotation was `on user request`.

```
vault write -f auth/ldap/config/rotate-root
```

Vault logs manual root rotations to `vault.log` with a note that the rotation was `on user request`.

### Schedule-based root credential rotation

Enterprise

Appropriate [Vault Enterprise](https://www.hashicorp.com/products/vault/pricing)  license required

Use the [`rotation_schedule`](/vault/api-docs/auth/ldap#rotation_schedule) field
to configure schedule-based, automatic credential rotation for root credentials in
the LDAP auth engine. For example, the following command set the rotation to
occur every Saturday at midnight (00:00):

```
$ vault write auth/ldap/config \
    ...
    rotation_schedule="0 * * * SAT"
    ...
```

Scheduled root credential rotation can also set a
[rotation\_window](/vault/api-docs/auth/ldap#rotation_window) during which the
scheduled rotation is allowed to occur. Vault will stop trying to rotate the
credential once the window expires. For example, the following command tells
Vault to rotate the credential on Saturday at midnight, but only within the span
of an hour. If Vault cannot rotate the credential by 1:00, due to a failure
or otherwise, Vault will stop trying to rotate the credential until the next
scheduled rotation.

```
$ vault write auth/ldap/config \
    ...
    rotation_window="1h" \
    rotation_schedule="0 * * * SAT"
    ...
```

You can temporarily disable root rotation by setting
[`disable_automated_rotation`](/vault/api-docs/auth/ldap#disable_automated_rotation)
to `true`. Setting the `disable_automated_rotation` field prevent any rotation
of the root credential until the field is reset to `false`. If you use
`rotation_period`, setting `disable_automated_rotation` also resets the credential
TTL.

#### Rotation URL

Use [`rotation_url`](/vault/api-docs/auth/ldap#rotation_url) to provide the
specific LDAP server URL that the bind account belongs to for rotating its
credential. By default, `rotation_url` uses the value of `url`. Setting an
explicit `rotation_url` parameter is useful when you need to configure an LDAP
forest where the bind account belongs to only a single domain behind a
load-balancer.

For more details on rotating root credentials in the LDAP plugin, refer to the
[Root credential rotation](/vault/api-docs/auth/ldap#rotate-root) API docs.

### Rotation logging

The rotation manager emits logs to the standard `vault.log` on any successful or
failed rotation.

In the case of success, Vault notes:

- the rotated credential as the first parameter, `rotationID`.
- the anticipated time of the next rotation as `expire_time`.

In the case of failure, Vault sets `rotationID` to `err` and may emit additional
logs depending on the configured log level.

## Examples scenarios

### Scenario 1

- LDAP server running on `ldap.example.com`, port 389.
- Server supports `STARTTLS` command to initiate encryption on the standard port.
- CA Certificate stored in file named `ldap_ca_cert.pem`
- Server is Active Directory supporting the userPrincipalName attribute. Users are identified as `username@example.com`.
- Groups are nested, we will use `LDAP_MATCHING_RULE_IN_CHAIN` to walk the ancestry graph.
- Group search will start under `ou=Groups,dc=example,dc=com`. For all group objects under that path, the `member` attribute will be checked for a match against the authenticated user.
- Group names are identified using their `cn` attribute.

```
$ vault write auth/ldap/config \
    url="ldap://ldap.example.com" \
    userdn="ou=Users,dc=example,dc=com" \
    groupdn="ou=Groups,dc=example,dc=com" \
    groupfilter="(&(objectClass=group)(member:1.2.840.113556.1.4.1941:={{.UserDN}}))" \
    groupattr="cn" \
    upndomain="example.com" \
    certificate=@ldap_ca_cert.pem \
    insecure_tls=false \
    starttls=true
...
```

### Scenario 2

- LDAP server running on `ldap.example.com`, port 389.
- Server supports `STARTTLS` command to initiate encryption on the standard port.
- CA Certificate stored in file named `ldap_ca_cert.pem`
- Server does not allow anonymous binds for performing user search.
- Bind account used for searching is `cn=vault,ou=users,dc=example,dc=com` with password `My$ecrt3tP4ss`.
- User objects are under the `ou=Users,dc=example,dc=com` organizational unit.
- Username passed to vault when authenticating maps to the `sAMAccountName` attribute.
- Group membership will be resolved via the `memberOf` attribute of *user* objects. That search will begin under `ou=Users,dc=example,dc=com`.

```
$ vault write auth/ldap/config \
    url="ldap://ldap.example.com" \
    userattr=sAMAccountName \
    userdn="ou=Users,dc=example,dc=com" \
    groupdn="ou=Users,dc=example,dc=com" \
    groupfilter="(&(objectClass=person)(uid={{.Username}}))" \
    groupattr="memberOf" \
    binddn="cn=vault,ou=users,dc=example,dc=com" \
    bindpass='My$ecrt3tP4ss' \
    certificate=@ldap_ca_cert.pem \
    insecure_tls=false \
    starttls=true
...
```

### Scenario 3

- LDAP server running on `ldap.example.com`, port 636 (LDAPS)
- CA Certificate stored in file named `ldap_ca_cert.pem`
- User objects are under the `ou=Users,dc=example,dc=com` organizational unit.
- Username passed to vault when authenticating maps to the `uid` attribute.
- User bind DN will be auto-discovered using anonymous binding.
- Group membership will be resolved via any one of `memberUid`, `member`, or `uniqueMember` attributes. That search will begin under `ou=Groups,dc=example,dc=com`.
- Group names are identified using the `cn` attribute.

```
$ vault write auth/ldap/config \
    url="ldaps://ldap.example.com" \
    userattr="uid" \
    userdn="ou=Users,dc=example,dc=com" \
    discoverdn=true \
    groupdn="ou=Groups,dc=example,dc=com" \
    certificate=@ldap_ca_cert.pem \
    insecure_tls=false \
    starttls=true
...
```

## LDAP group -> policy mapping

Next we want to create a mapping from an LDAP group to a Vault policy:

```
$ vault write auth/ldap/groups/scientists policies=foo,bar
```

This maps the LDAP group "scientists" to the "foo" and "bar" Vault policies.
We can also add specific LDAP users to additional (potentially non-LDAP)
groups. Note that policies can also be specified on LDAP users as well.

```
$ vault write auth/ldap/groups/engineers policies=foobar
$ vault write auth/ldap/users/tesla groups=engineers policies=zoobar
```

This adds the LDAP user "tesla" to the "engineers" group, which maps to
the "foobar" Vault policy. User "tesla" itself is associated with "zoobar"
policy.

Finally, we can test this by authenticating:

```
$ vault login -method=ldap username=tesla
Password (will be hidden):
Successfully authenticated! The policies that are associated
with this token are listed below:

default, foobar, zoobar
```

## Note on policy mapping

It should be noted that user -> policy mapping happens at token creation time. And changes in group membership on the LDAP server will not affect tokens that have already been provisioned. To see these changes, old tokens should be revoked and the user should be asked to reauthenticate.

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

The LDAP auth method has a full HTTP API. Please see the
[LDAP auth method API](/vault/api-docs/auth/ldap) for more
details.

[Edit this page on GitHub](https://github.com/hashicorp/web-unified-docs/blob/main/content/vault/v1.21.x/content/docs/auth/ldap.mdx)