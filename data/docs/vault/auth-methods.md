# Vault Authentication Methods

## Overview

Auth methods are the components in Vault that perform authentication and are responsible for assigning identity and a set of policies to a user. Vault supports multiple auth methods simultaneously, and you can mount the same type multiple times.

## Token Auth Method

The token auth method is built-in and automatically available. It allows users to authenticate using a token. Tokens can be created manually, by another auth method, or via the Vault API.

Token types:
- **Service tokens**: Full-featured tokens with accessor, renewal, and child token support
- **Batch tokens**: Lightweight tokens for high-performance workloads, not stored in backend

## AppRole Auth Method

AppRole is a mechanism for machine-to-machine authentication. It is designed for automated workflows (CI/CD, scripts, applications).

How it works:
1. Admin creates a role with policies
2. Role ID is shared with the application (like a username)
3. Secret ID is generated and securely delivered (like a password)
4. Application authenticates with Role ID + Secret ID
5. Vault returns a token with the configured policies

Best practices:
- Use CIDR binding to restrict Secret ID usage by IP
- Set Secret ID TTL and usage limits
- Rotate Secret IDs regularly
- Use response wrapping for Secret ID delivery

## LDAP Auth Method

The LDAP auth method allows authentication using an existing LDAP server. Users authenticate with their LDAP credentials and Vault maps LDAP groups to Vault policies.

Configuration:
- URL of the LDAP server
- User DN format
- Group search base and filter
- TLS settings (strongly recommended)

## Kubernetes Auth Method

The Kubernetes auth method can be used to authenticate with Vault using a Kubernetes Service Account Token. This method of authentication makes it easy to introduce a Vault token into a Kubernetes Pod.

How it works:
1. Configure Vault with Kubernetes cluster details
2. Create roles that map Kubernetes service accounts to Vault policies
3. Pods authenticate using their service account token
4. Vault validates the token with the Kubernetes API
5. Pod receives a Vault token with appropriate policies

## OIDC Auth Method

The OIDC auth method allows authentication via an OpenID Connect provider. This is commonly used for human users authenticating through SSO providers (Okta, Azure AD, Google).

Setup requirements:
- OIDC provider configuration (client ID, client secret)
- Redirect URIs for the callback
- Claims mapping to Vault policies
- Optional: group claims for team-based access
