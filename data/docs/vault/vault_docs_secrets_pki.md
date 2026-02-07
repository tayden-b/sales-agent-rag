# Source: https://developer.hashicorp.com/vault/docs/secrets/pki

v1.21.x (latest)

- Vault
- [v1.20.x](/vault/docs/v1.20.x/secrets/pki)
- [v1.19.x](/vault/docs/v1.19.x/secrets/pki)
- [v1.18.x](/vault/docs/v1.18.x/secrets/pki)
- [v1.17.x](/vault/docs/v1.17.x/secrets/pki)
- [v1.16.x](/vault/docs/v1.16.x/secrets/pki)
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

# PKI secrets engine

Note

This engine can use external X.509 certificates as part of TLS or signature validation.
Verifying signatures against X.509 certificates that use SHA-1 is deprecated and is no longer
usable without a workaround starting in Vault 1.12. Refer to the
[deprecation notices](/vault/docs/updates/deprecation)
for more information.

Vault as Consul CA provider

If you are using Vault 1.11.0+ as a Connect CA, run a Consul version which
includes the fix for [GH-15525](https://github.com/hashicorp/consul/pull/15525).
Refer to this [Knowledge Base
article](https://support.hashicorp.com/hc/en-us/articles/11308460105491) for
more details.

The PKI secrets engine generates dynamic X.509 certificates. With this secrets
engine, services can get certificates without going through the usual manual
process of generating a private key and CSR, submitting to a CA, and waiting for
a verification and signing process to complete. Vault's built-in authentication
and authorization mechanisms provide the verification functionality.

By keeping TTLs relatively short, revocations are less likely to be needed,
keeping CRLs short and helping the secrets engine scale to large workloads. This
in turn allows each instance of a running application to have a unique
certificate, eliminating sharing and the accompanying pain of revocation and
rollover.

In addition, by allowing revocation to mostly be forgone, this secrets engine
allows for ephemeral certificates. Certificates can be fetched and stored in
memory upon application startup and discarded upon shutdown, without ever being
written to disk.

## Table of contents

The PKI Secrets Engine documentation is split into the following pieces:

- [Overview](/vault/docs/secrets/pki) - this document.
- [Setup and Usage](/vault/docs/secrets/pki/setup) - a brief description of setting
  up and using the PKI Secrets Engine to issue certificates.
- [Quick Start - Root CA Setup](/vault/docs/secrets/pki/quick-start-root-ca) - A
  quick start guide for setting up a root CA.
- [Quick Start - Intermediate CA Setup](/vault/docs/secrets/pki/quick-start-intermediate-ca) - A
  quick start guide for setting up an intermediate CA.
- [Considerations](/vault/docs/secrets/pki/considerations) - A list of helpful
  considerations to keep in mind when using and operating the PKI Secrets
  Engine.
- [Rotation Primitives](/vault/docs/secrets/pki/rotation-primitives) - A document
  which explains different types of certificates used to achieve rotation.
- [CIEPS Protocol 

  Enterprise](/vault/docs/secrets/pki/cieps) - A
  document which explains the Certificate Issuance External Policy Service (CIEPS)
  protocol (request and response structure), along with an overview of the difference
  between it and `/pki/sign-verbatim`.
- Issuance Protocols: Using standard certificate management protocols with Vault PKI.
  - [EST 

    Enterprise](/vault/docs/secrets/pki/est) -
    Explains Vault's implementation of the EST protocol, from configuration
    to limitations.
  - [CMPv2 

    Enterprise](/vault/docs/secrets/pki/cmpv2) -
    Explains Vault's implementation of the CMPv2 protocol, from configuration
    to limitations.
  - [SCEP 

    Enterprise](/vault/docs/secrets/pki/scep) -
    Explains Vault's implementation of the SCEP protocol, from configuration
    to limitations.
  - [Troubleshooting ACME](/vault/docs/secrets/pki/troubleshooting-acme) - A list of
    advice for troubleshooting failures with ACME issuance and Vault PKI.

## Tutorial

Refer to the following tutorials for PKI secrets engine usage examples:

- [Build Your Own Certificate Authority (CA)](/vault/tutorials/secrets-management/pki-engine)
- [Build Certificate Authority (CA) in Vault with an offline Root](/vault/tutorials/secrets-management/pki-engine-external-ca)
- [Enable ACME with PKI secrets engine](/vault/tutorials/secrets-management/pki-acme-caddy)
- [PKI Secrets Engine with Managed Keys](/vault/tutorials/enterprise/managed-key-pki)
- [PKI Unified CRL and OCSP With Cross Cluster
  Revocation](/vault/tutorials/secrets-management/pki-unified-crl-ocsp-cross-cluster)
- [Configure Vault as a Certificate Manager in Kubernetes with
  Helm](/vault/tutorials/kubernetes/kubernetes-cert-manager)
- [Generate mTLS Certificates for Nomad using
  Vault](/vault/tutorials/secrets-management/vault-pki-nomad)

## API

The PKI secrets engine has a full HTTP API. Please see the
[PKI secrets engine API](/vault/api-docs/secret/pki) for more
details.

[Edit this page on GitHub](https://github.com/hashicorp/web-unified-docs/blob/main/content/vault/v1.21.x/content/docs/secrets/pki/index.mdx)