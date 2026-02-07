# Source: https://developer.hashicorp.com/vault/docs/use-cases

v1.21.x (latest)

- Vault
- [v1.20.x](/vault/docs/v1.20.x/about-vault/why-use-vault)
- [v1.19.x](/vault/docs/v1.19.x/about-vault/why-use-vault)
- [v1.18.x](/vault/docs/v1.18.x/about-vault/why-use-vault)
- [v1.17.x](/vault/docs/v1.17.x/about-vault/why-use-vault)
- [v1.16.x](/vault/docs/v1.16.x/about-vault/why-use-vault)
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

# Why use Vault?

Modern software works because of **secrets**. Secrets are sensitive, discrete
pieces of information like credentials, encryption keys, authentication
certificates, and other critical pieces of information your applications need
to run consistently and securely.

Use Vault to centralizing secret management and harden your application
deployments.

|  |  |
| --- | --- |
| TBD TBD | Manage 3rd-party secrets [Manage 3rd-party secrets](/vault/docs/about-vault/why-use-vault/3rd-party-secrets) by integrating Vault with the other elements of your development environment. Generate and revoke on-demand credentials for database systems and cloud providers like AWS, and control access to external information like encryption keys and cloud credentials. |

|  |  |
| --- | --- |
| TBD TBD | Manage certificates [Manage certificates](/vault/docs/about-vault/why-use-vault/certificates) by configuring Vault to work with certificate authorities like KMIP and PKI to manage certificate life cycles and authenticate clients. |

|  |  |
| --- | --- |
| TBD TBD | Manage identities and authentication [Manage identities and authentication](/vault/docs/about-vault/why-use-vault/identities) and control client access to sensitive information with managed entities, identity tokens, OIDC workflows, and workload identity federation (WIF). |

|  |  |
| --- | --- |
| TBD TBD | Manage static secrets [Manage static secrets](/vault/docs/about-vault/why-use-vault/static-secrets) by storing and rotating arbitrary secrets in Vault with the Key/Value and Cubbyhole plugins. Vault encrypts data before writing out to persistent storage, so accessing the raw storage is insufficient to access the information. |

|  |  |
| --- | --- |
| TBD TBD | Secure sensitive data [Secure sensitive data](/vault/docs/about-vault/why-use-vault/sensitive-data) by defining custom parameters to encrypt or tokenize sensitive data in transit and at rest without storing the data in Vault. |

|  |  |
| --- | --- |
| TBD TBD | Support regulatory compliance [Support regulatory compliance](/vault/docs/about-vault/why-use-vault/regulatory-compliance) by configuring Vault as part of an HSM solution, FIPS compliant architecture, or PKCS11 authN workflow. |

[Edit this page on GitHub](https://github.com/hashicorp/web-unified-docs/blob/main/content/vault/v1.21.x/content/docs/about-vault/why-use-vault/index.mdx)