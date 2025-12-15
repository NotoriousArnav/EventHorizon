# Client Integration Guide

This guide explains how to integrate external applications (Clients) with the Event Horizon platform using OAuth 2.0.

## Prerequisites

1.  **Register your Application:**
    *   Log in to the Event Horizon Admin Panel (e.g., `/admin/`).
    *   Navigate to **Django OAuth Toolkit** > **Applications**.
    *   Create a new Application:
        *   **Client Type:** Confidential (or Public for SPAs/Mobile)
        *   **Authorization Grant Type:** Authorization code
        *   **Redirect URIs:** The URL where your client will handle the callback (e.g., `http://localhost:8080/callback.php`).
        *   **Algorithm:** RSA (if using OIDC) or HMAC.

2.  **Obtain Credentials:**
    *   Note down the `Client ID` and `Client Secret`.

## PHP Client Example

The project includes a reference PHP client in the `php-client/` directory.

### 1. Configuration (`config.php`)

Edit `config.php` to match your environment:

```php
define('CLIENT_ID', 'your_client_id_from_django');
define('CLIENT_SECRET', 'your_client_secret_from_django');
define('DJANGO_BASE_URL', 'http://127.0.0.1:8000');
define('REDIRECT_URI', 'http://localhost:8080/callback.php');
```

### 2. Authorization Flow (PKCE)

The client implements the **Proof Key for Code Exchange (PKCE)** flow for enhanced security.

#### Step A: Generate Code Verifier & Challenge
1.  Generate a random string (Code Verifier).
2.  Hash it using SHA256 and Base64-URL encode it (Code Challenge).

#### Step B: Redirect to Authorization URL
Redirect the user to the Event Horizon authorization endpoint:
`GET /o/authorize/?response_type=code&client_id=...&redirect_uri=...&code_challenge=...&code_challenge_method=S256`

#### Step C: Handle Callback
When the user approves access, Event Horizon redirects back to your `REDIRECT_URI` with a `code` parameter.

#### Step D: Exchange Code for Token
Make a POST request to `/o/token/` to exchange the code for an access token. You must verify the `code_verifier` used in Step A.

```bash
POST /o/token/
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&code=RECEIVED_CODE
&client_id=YOUR_CLIENT_ID
&client_secret=YOUR_CLIENT_SECRET
&redirect_uri=YOUR_REDIRECT_URI
&code_verifier=ORIGINAL_VERIFIER_STRING
```

### 3. Accessing the API

Once you have the `access_token`, use it to make authorized requests:

```php
$headers = [
    "Authorization: Bearer " . $access_token
];
// Make Request...
```

See `php-client/callback.php` for a complete implementation reference.
