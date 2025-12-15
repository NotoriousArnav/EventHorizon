# OAuth2 Provider

Event Horizon acts as an OAuth2 Provider, allowing third-party applications (like the PHP CLI client) to authenticate users securely.

## Supported Grants

- **Authorization Code:** For server-side apps (confidential clients).
- **Client Credentials:** For machine-to-machine communication.

## Setup for Developers

1.  Go to the **Django Admin** > **Django OAuth Toolkit** > **Applications**.
2.  Create a new Application.
3.  **Client Type:** Confidential (for server-side apps) or Public (for SPAs/Mobile).
4.  **Authorization Grant Type:** Authorization code.
5.  **Redirect URIs:** The callback URL of your application (e.g., `http://localhost:8080/callback.php`).

## OIDC Support
OpenID Connect (OIDC) is supported for identity verification, providing the `id_token` alongside access tokens.
