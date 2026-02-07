# Source: https://developer.hashicorp.com/vault/docs/secrets/databases

v1.21.x (latest)

- Vault
- [v1.20.x](/vault/docs/v1.20.x/secrets/databases)
- [v1.19.x](/vault/docs/v1.19.x/secrets/databases)
- [v1.18.x](/vault/docs/v1.18.x/secrets/databases)
- [v1.17.x](/vault/docs/v1.17.x/secrets/databases)
- [v1.16.x](/vault/docs/v1.16.x/secrets/databases)
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

# Database secrets engine

The database secrets engine generates database credentials dynamically based on
configured roles. It works with a number of different databases through a plugin
interface. There are a number of built-in database types, and an exposed framework
for running custom database types for extendability. This means that services
that need to access a database no longer need to hardcode credentials: they can
request them from Vault, and use Vault's [leasing mechanism](/vault/docs/concepts/lease)
to more easily roll keys. These are referred to as "dynamic roles" or "dynamic
secrets".

Since every service is accessing the database with unique credentials, it makes
auditing much easier when questionable data access is discovered. You can track
it down to the specific instance of a service based on the SQL username.

Vault makes use of its own internal revocation system to ensure that users
become invalid within a reasonable time of the lease expiring.

### Static roles

Vault also supports **static roles** for all database secrets engines. Static
roles are a 1-to-1 mapping of Vault roles to usernames in a database. With
static roles, Vault stores and automatically rotates passwords for the
associated database user based on a configurable period of time or rotation
schedule.

When the database user is onboarded into Vault via the
[Create static role](/vault/api-docs/secret/databases#create-static-role) API,
the user's password is automatically rotated. Automatic rotation can be
disabled for all roles at the config-level with the
[skip\_static\_role\_import\_rotation](/vault/api-docs/secret/databases#skip_static_role_import_rotation)
field or per role with the [skip\_import\_rotation](/vault/api-docs/secret/databases#skip_import_rotation)
field.

When a client requests credentials for the static role, Vault returns the
current password for whichever database user is mapped to the requested role.
With static roles, anyone with the proper Vault policies can access the
associated user account in the database.

Do not use static roles for root database credentials

Do not manage the same root database credentials that you provide to Vault in

config/ with static roles.

Vault does not distinguish between standard credentials and root credentials
when rotating passwords. If you assign your root credentials to a static
role, any dynamic or static users managed by that database configuration will
fail after rotation because the password for config/ is no longer
valid.

If you need to rotate root credentials, use the
[Rotate root credentials](/vault/api-docs/secret/databases#rotate-root-credentials)
API endpoint.

### Schedule-based root credential rotation

Enterprise

Appropriate [Vault Enterprise](https://www.hashicorp.com/products/vault/pricing)  license required

Use the [`rotation_schedule`](/vault/api-docs/secret/databases#rotation_schedule) field
to configure schedule-based, automatic credential rotation for root credentials in
the DB Secrets engine. For example, the following command set the rotation to
occur every Saturday at midnight (00:00):

```
$ vault write database/config/my-mssql-database \
  ...
  rotation_schedule="0 * * * SAT"
  ...
```

Scheduled root credential rotation can also set a
[rotation\_window](/vault/api-docs/secret/databases#rotation_window) during which the
scheduled rotation is allowed to occur. Vault will stop trying to rotate the
credential once the window expires. For example, the following command tells
Vault to rotate the credential on Saturday at midnight, but only within the span
of an hour. If Vault cannot rotate the credential by 1:00, due to a failure
or otherwise, Vault will stop trying to rotate the credential until the next
scheduled rotation.

```
$ vault write database/config/my-mssql-database \
  ...
  rotation_window="1h" \
  rotation_schedule="0 * * * SAT"
...
```

You can temporarily disable root rotation by setting
[`disable_automated_rotation`](/vault/api-docs/secret/databases#disable_automated_rotation)
to `true`. Setting the `disable_automated_rotation` field prevent any rotation
of the root credential until the field is reset to `false`. If you use
`rotation_period`, setting `disable_automated_rotation` also resets the credential
TTL.

For more details on rotating root credentials in the DB Secrets engine, refer to the
[Rotate Root credentials](/vault/api-docs/secret/databases#rotate-root-credentials) API docs.

### Rotation logging

The rotation manager emits logs to the standard `vault.log` on any successful or
failed rotation.

In the case of success, Vault notes:

- the rotated credential as the first parameter, `rotationID`.
- the anticipated time of the next rotation as `expire_time`.

In the case of failure, Vault sets `rotationID` to `err` and may emit additional
logs depending on the configured log level.

## Setup

Most secrets engines must be configured in advance before they can perform their
functions. These steps are usually completed by an operator or configuration
management tool.

CLIGUI

Enable the database secrets engine.

```
$ vault secrets enable database
Success! Enabled the database secrets engine at: database/
```

By default, the secrets engine will enable at the name of the engine. To
enable the secrets engine at a different path, use the `-path` argument.

![Partial screenshot of the Vault GUI showing the "Enable database" page](https://web-unified-docs-hashicorp.vercel.app/api/assets/vault/latest/img/gui/databases/enableDatabase.png)

- Open the **Enable a Secrets Engine** page:

  1. Open the GUI for your Vault instance.
  2. Log in under the namespace for the plugin or select the namespace from the
     selector at the bottom of the left-hand menu and re-authenticate.
  3. Select **Secrets Engines** from the left-hand menu.
  4. Click **Enable new engine +** on the **Secrets Engines** page.

- Select **Databases**.
- Click **Enable engine**.
- Click **Save** to enable the plugin.

CLIGUI

Configure Vault with the proper plugin and connection information.

```
$ vault write database/config/my-database \
    plugin_name="..." \
    connection_url="..." \
    allowed_roles="..." \
    username="..." \
    password="..." \
```

It is highly recommended a user within the database is created
specifically for Vault to use. This user will be used to manipulate
dynamic and static users within the database. This user is called the
"root" user within the documentation.

Vault will use the user specified here to create/update/revoke database
credentials. That user must have the appropriate permissions to perform
actions upon other database users (create, update credentials, delete, etc.).

This secrets engine can configure multiple database connections. For details
on the specific configuration options, please see the database-specific
documentation.

![Partial screenshot of the Vault GUI showing the "Create connection" page](https://web-unified-docs-hashicorp.vercel.app/api/assets/vault/latest/img/gui/databases/configureDBConnection.png)

1. Select **Secret Engines** from the navigation menu.
2. Select the **`database/`** mount path.
3. Select the **Connections** tab.
4. Click **Create connection +**
5. Click on the **Database plugin** dropdown and select your database.

CLIGUI

After configuration, we strongly recommend rotating the root user password such that the vault user is not accessible by any users other than
Vault itself:

```
$ vault write -force database/rotate-root/my-database
```

When this is done, the password for the user specified in the previous step
is no longer accessible. Because of this, it is highly recommended that a
user is created specifically for Vault to use to manage database
users.

![Partial screenshot of the Vault GUI showing the populated "Plugin config" section](https://web-unified-docs-hashicorp.vercel.app/api/assets/vault/latest/img/gui/databases/pluginConfig.png)

1. Provide the database configuration details.
2. Click **Create database** to create the database connection.
3. Select **Secret Engines** from the navigation menu.
4. Select the **`database/`** mount path.
5. Select the **Roles** tab.
6. Click **Create role +**.

CLIGUI

Configure a role that maps a name in Vault to a set of creation statements to
create the database credential:

```
$ vault write database/roles/my-role \
    db_name=my-database \
    creation_statements="..." \
    default_ttl="1h" \
    max_ttl="24h"
Success! Data written to: database/roles/my-role
```

The `{{username}}` and `{{password}}` fields will be populated by the plugin
with dynamically generated values. In some plugins the `{{expiration}}` field is also supported.

![Screenshot of the Vault GUI showing the "Create Role" page](https://web-unified-docs-hashicorp.vercel.app/api/assets/vault/latest/img/gui/databases/roleDefaultState.png)

1. Set **Role name** to a human-readable name for the role.
2. Click on the **Connection name** dropdown, and select a DB connection you
   want associated with the new role.
3. Click on the **Type of role** dropdown, and select `static` or `dynamic`.
4. Configure the role.
   - For static roles:
     - Set the DB username associated with the role.
     - Set a DB password for the role (or leave blank).
     - Set the **Rotation period** for the role password. By default, Vault
       rotates passwords every 24 hours.
     - If you want to bypass an initial rotation on creation, toggle
       **Rotate immediately** to off.
   - For dynamic roles:
     - Set the TTL and max TTL expiry times. By default, TTL is 1 hour and max TTL is 24 hours.
     - Add any customized creation, revocation, rollback, or renew DB
       statements for the role.
5. Click **Create role** to create the role.

## Usage

After the secrets engine is configured and a user/machine has a Vault token with
the proper permission, it can generate credentials.

1. Generate a new credential by reading from the `/creds` endpoint with the name
   of the role:

   ```
   $ vault read database/creds/my-role
   Key                Value
   ---                -----
   lease_id           database/creds/my-role/2f6a614c-4aa2-7b19-24b9-ad944a8d4de6
   lease_duration     1h
   lease_renewable    true
   password           FSREZ1S0kFsZtLat-y94
   username           v-vaultuser-e2978cd0-ugp7iqI2hdlff5hfjylJ-1602537260
   ```

## Database capabilities

As of Vault 1.6, all databases support dynamic roles and static roles. All plugins except MongoDB Atlas support rotating
the root user's credentials. MongoDB Atlas cannot support rotating the root user's credentials because it uses a public
and private key pair to authenticate.

| Database | UI support | Root Credential Rotation | Dynamic Roles | Static Roles | Username Customization | Credential Types |
| --- | --- | --- | --- | --- | --- | --- |
| [Cassandra](/vault/docs/secrets/databases/cassandra) | No | Yes | Yes | Yes (1.6+) | Yes (1.7+) | password |
| [Couchbase](/vault/docs/secrets/databases/couchbase) | No | Yes | Yes | Yes | Yes (1.7+) | password |
| [Elasticsearch](/vault/docs/secrets/databases/elasticdb) | Yes (1.9+) | Yes | Yes | Yes (1.6+) | Yes (1.8+) | password |
| [HanaDB](/vault/docs/secrets/databases/hanadb) | No | Yes (1.6+) | Yes | Yes (1.6+) | Yes (1.12+) | password |
| [InfluxDB](/vault/docs/secrets/databases/influxdb) | No | Yes | Yes | Yes (1.6+) | Yes (1.8+) | password |
| [MongoDB](/vault/docs/secrets/databases/mongodb) | Yes (1.7+) | Yes | Yes | Yes | Yes (1.7+) | password |
| [MongoDB Atlas](/vault/docs/secrets/databases/mongodbatlas) | No | No | Yes | Yes | Yes (1.8+) | password, client\_certificate |
| [MSSQL](/vault/docs/secrets/databases/mssql) | Yes (1.8+) | Yes | Yes | Yes | Yes (1.7+) | password |
| [MySQL/MariaDB](/vault/docs/secrets/databases/mysql-maria) | Yes (1.8+) | Yes | Yes | Yes | Yes (1.7+) | password, gcp\_iam |
| [Oracle](/vault/docs/secrets/databases/oracle) | Yes (1.9+) | Yes | Yes | Yes | Yes (1.7+) | password |
| [PostgreSQL](/vault/docs/secrets/databases/postgresql) | Yes (1.9+) | Yes | Yes | Yes | Yes (1.7+) | password, gcp\_iam |
| [Redis](/vault/docs/secrets/databases/redis) | No | Yes | Yes | Yes | No | password |
| [Redis ElastiCache](/vault/docs/secrets/databases/rediselasticache) | No | No | No | Yes | No | password |
| [Redshift](/vault/docs/secrets/databases/redshift) | No | Yes | Yes | Yes | Yes (1.8+) | password |
| [Snowflake](/vault/docs/secrets/databases/snowflake) | No | Yes | Yes | Yes | Yes (1.8+) | password(deprecated), rsa\_private\_key |

## Custom plugins

This secrets engine allows custom database types to be run through the exposed
plugin interface. Please see the [custom database plugin](/vault/docs/secrets/databases/custom)
for more information.

## Credential types

Database systems support a variety of authentication methods and credential types.
The database secrets engine supports management of credentials alternative to usernames
and passwords. The [credential\_type](/vault/api-docs/secret/databases#credential_type)
and [credential\_config](/vault/api-docs/secret/databases#credential_config) parameters
of dynamic and static roles configure the credential that Vault will generate and
make available to database plugins. See the documentation of individual database
plugins for the credential types they support and usage examples.

## Onboarding static database users

When a static database user is onboarded to the database secrets engine, by
default Vault immediately and automatically rotates the database user's
password. This immediate rotation can add additional operational overhead to
the onboarding process and has proven challenging for some organizations. To
address these challenges, you can configure one or more of the following options:

APIGUI

- Disable the automatic rotation of static role passwords during Vault
  onboarding. This will allow you to enroll the static database user in Vault before
  you do the actual cutover of the application to consume the credential from
  Vault. You can configure this for all roles associated with a database connection with
  [skip\_static\_role\_import\_rotation](/vault/api-docs/secret/databases#skip_static_role_import_rotation)
  or on a per-role basis with [skip\_import\_rotation](/vault/api-docs/secret/databases#skip_import_rotation).
- Set the initial static role password during Vault onboarding. Setting the
  static role's [password](/vault/api-docs/secret/databases#password)
  gives you the ability to retrieve the static user's existing password
  after onboarding and before the first rotation. This capability enables Vault
  to be ready for the client application when it begins to look to Vault for
  its passwords, and enables multiple clients using the same static role to
  transition slowly.

![Partial screenshot of the Vault GUI showing the database level "Rotate static roles immediately" toggle](https://web-unified-docs-hashicorp.vercel.app/api/assets/vault/latest/img/gui/databases/databaseRotation.png)
On the DB connection creation page and the static role creation page, turning off the **Rotate static roles immediately** toggle lets you bypass an initial rotation on role creation.

To set an initial password during static role creation, provide a password and toggle **Rotate immediately** off before saving.

## Schedule-based static role rotation

The database secrets engine supports configuring schedule-based automatic
credential rotation for static roles with the
[rotation\_schedule](/vault/api-docs/secret/databases#rotation_schedule) field.
For example:

```
$ vault write database/static-roles/my-role \
    db_name=my-database \
    username="vault" \
    rotation_schedule="0 * * * SAT"
```

This configuration will set the role's credential rotation to occur on Saturday
at 00:00.

Additionally, this schedule-based approach allows for optionally configuring a
[rotation\_window](/vault/api-docs/secret/databases#rotation_window) in which
the automatic rotation is allowed to occur. For example:

```
$ vault write database/static-roles/my-role \
    db_name=my-database \
    username="vault" \
    rotation_window="1h" \
    rotation_schedule="0 * * * SAT"
```

This configuration will set rotations to occur on Saturday at 00:00. The 1
hour `rotation_window` will prevent the rotation from occuring after 01:00. If
the static role's credential is not rotated during this window, due to a failure
or otherwise, it will not be rotated until the next scheduled rotation.

The `rotation_period` and `rotation_schedule` fields are
mutually exclusive. One of them must be set but not both.

Vault logs rotations with reference to the `name` of the role and `error` if the rotation failed. The logs also indicate if the rotation was part of a `periodic function`.

## Password generation

Passwords are generated via [Password Policies](/vault/docs/concepts/password-policies).
Databases can optionally set a password policy for use across all roles or at the
individual role level for that database. For example, each time you call
`vault write database/config/my-database` you can specify a password policy for all
roles using `my-database`. Each database has a default password policy defined as:
20 characters with at least 1 uppercase character, at least 1 lowercase character,
at least 1 number, and at least 1 dash character.

The default password generation can be represented as the following password policy:

```
length = 20

rule "charset" {
    charset = "abcdefghijklmnopqrstuvwxyz"
    min-chars = 1
}
rule "charset" {
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    min-chars = 1
}
rule "charset" {
    charset = "0123456789"
    min-chars = 1
}
rule "charset" {
    charset = "-"
    min-chars = 1
}
```

## Disable character escaping

As of Vault 1.10, you can now specify the option `disable_escaping` with a value of `true`  in
some secrets engines to prevent Vault from escaping special characters in the username and password
fields. This is necessary for some alternate connection string formats, such as ADO with MSSQL or Azure
SQL. See the [databases secrets engine API docs](/vault/api-docs/secret/databases#common-fields) and reference
individual plugin documentation to determine support for this parameter.

For example, when the password contains URL-escaped characters like `#` or `%` they will
remain as so instead of becoming `%23` and `%25` respectively.

```
$ vault write database/config/my-mssql-database \
plugin_name="mssql-database-plugin" \
connection_url='server=localhost;port=1433;user id={{username}};password={{password}};database=mydb;' \
username="root" \
password='your#StrongPassword%' \
disable_escaping="true"
```

## Unsupported databases

### AWS DynamoDB

Amazon Web Services (AWS) DynamoDB is a fully managed, serverless, key-value NoSQL database service. While
DynamoDB is not supported by the database secrets engine, you can use the [AWS secrets engine](/vault/docs/secrets/aws)
to provision dynamic credentials capable of accessing DynamoDB.

1. Verify you have the AWS secrets engine enabled and configured.
2. Create a role with the necessary permissions for your users to access DynamoDB. For example:

   ```
   $ vault write aws/roles/aws-dynamodb-read \
           credential_type=iam_user \
           policy_document=-<<EOF
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "dynamodb:DescribeTable",
                   "dynamodb:GetItem",
                   "dynamodb:GetRecords"
               ],
               "Resource": "arn:aws:dynamodb:us-east-1:1234567891:table/example-table"
           },
           {
               "Effect": "Allow",
               "Action": "dynamodb:ListTables",
               "Resource": "*"
           }
       ]
   }
   EOF
   ```
3. Generate dynamic credentials for DynamoDB using the `aws-dynamodb-read` role:

   ```
   $ vault read aws/creds/aws-dynamodb-read
   Key                Value
   ---                -----
   lease_id           aws/creds/my-role/kbSnl9WSDzOXQerd8GiVh75N.DACNl
   lease_duration     1h
   lease_renewable    true
   access_key         AKALMNOP123456
   secret_key         xY4XhS3AsM3s+R33tCaybsT2XI6BVL+vF+khbbYD
   security_token     <nil>
   ```
4. Use the dynamic credentials generated by Vault to access DynamoDB. For example, to connect with the
   the [AWS CLI](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/).

   ```
   $ aws dynamodb list-tables --region us-east-1
   {
       "TableNames": [
           "example-table"
       ]
   }
   ```

## Tutorial

Refer to the [database credential management](/vault/tutorials/db-credentials)
tutorials to learn how to manage database credential lifecycle with Vault.

## API

The database secrets engine has a full HTTP API. Please see the [Database secret
secrets engine API](/vault/api-docs/secret/databases) for more details.

[Edit this page on GitHub](https://github.com/hashicorp/web-unified-docs/blob/main/content/vault/v1.21.x/content/docs/secrets/databases/index.mdx)