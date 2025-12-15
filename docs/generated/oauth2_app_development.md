# OAuth2 Application Development Guide

This guide details how to build applications that integrate with Event Horizon using OAuth2. Event Horizon acts as an OAuth2 Provider (powered by Django OAuth Toolkit) and supports OpenID Connect (OIDC), allowing third-party applications to authenticate users and access API resources on their behalf.

## 1. Introduction

Event Horizon provides a secure and standard way for your applications to access user data. By using OAuth2, you can request specific permissions (scopes) from users without handling their credentials directly.

Key features:
- **OAuth2 Provider**: Support for standard OAuth2 flows.
- **OpenID Connect**: Support for identity verification.
- **PKCE Support**: Enhanced security for public clients (like mobile or single-page apps).

## 2. App Registration

Before your application can interact with Event Horizon, it must be registered.

1.  **Log in** to the Event Horizon Admin Panel.
2.  Navigate to **Django OAuth Toolkit** > **Applications** (or visit `/admin/oauth2_provider/application/`).
3.  Click **Add Application**.
4.  Fill in the form:
    *   **User**: Select the owner of the application (usually your user).
    *   **Client Type**:
        *   **Confidential**: For server-side apps that can keep the client secret safe (e.g., Web apps).
        *   **Public**: For apps that cannot store secrets securely (e.g., Mobile apps, SPAs).
    *   **Authorization Grant Type**: Select **Authorization code** (recommended for most use cases).
    *   **Redirect URIs**: Enter the allowed callback URLs for your app.
        *   Example: `http://localhost:3000/callback`
        *   Note: Must match exactly what you send in the authorization request.
    *   **Algorithm**: Choose `RSA` or `HMAC` (defaults are usually fine).
5.  Click **Save**.
6.  **Important**: Note down the `Client ID` and `Client Secret` (if confidential). You will need these later.

## 3. Endpoints Reference

Base URL: `http://127.0.0.1:8000` (or your production domain)

| Endpoint | Path | Description |
| :--- | :--- | :--- |
| **Authorization** | `/o/authorize/` | Used to start the authorization flow. |
| **Token** | `/o/token/` | Used to exchange the authorization code for an access token. |
| **Revoke** | `/o/revoke_token/` | Used to invalidate an access token. |
| **UserInfo** | `/o/userinfo/` | (OIDC) Returns information about the authenticated user. |
| **Profile API** | `/accounts/api/me/` | Custom endpoint for detailed user profile (requires `read` scope). |

## 4. Scopes

Scopes define what access your application is requesting. Event Horizon defines the following scopes in `settings.py`:

*   `read`: Read-only access to resources.
*   `write`: Write access to resources.
*   `groups`: Access to user groups.
*   `openid`: Required for OpenID Connect (returns an `id_token`).

## 5. The Authorization Flow (Deep Dive)

We recommend the **Authorization Code Flow with PKCE** (Proof Key for Code Exchange) for maximum security, especially for public clients.

### Step 1: Generate Code Verifier and Challenge
PKCE prevents authorization code interception attacks.
1.  **Code Verifier**: A high-entropy random string (43-128 chars, alphanumeric + `-._~`).
2.  **Code Challenge**: BASE64-URL-encoded SHA256 hash of the code verifier.

### Step 2: Construct the Authorization URL
Redirect the user to this URL in their browser:

```
GET /o/authorize/?
    response_type=code
    &client_id=YOUR_CLIENT_ID
    &redirect_uri=YOUR_REDIRECT_URI
    &scope=read write openid
    &code_challenge=YOUR_CODE_CHALLENGE
    &code_challenge_method=S256
```

### Step 3: Handle the Callback
The user logs in and approves access. Event Horizon redirects back to your `redirect_uri`:

```
http://localhost:3000/callback?code=AUTHORIZATION_CODE&state=...
```

### Step 4: Exchange Code for Token
Make a POST request to `/o/token/` to get the access token.

**Headers**: `Content-Type: application/x-www-form-urlencoded`

**Body**:
```
grant_type=authorization_code
code=AUTHORIZATION_CODE
client_id=YOUR_CLIENT_ID
redirect_uri=YOUR_REDIRECT_URI
code_verifier=YOUR_CODE_VERIFIER
```
*(If confidential client, also include `client_secret`)*

## 6. Code Examples

### Python Example
Using `requests` and `pkce` (install via `pip install requests pkce`).

```python
import requests
import pkce
import webbrowser

# Config
CLIENT_ID = "your_client_id"
REDIRECT_URI = "http://localhost:8000/callback"
AUTH_URL = "http://127.0.0.1:8000/o/authorize/"
TOKEN_URL = "http://127.0.0.1:8000/o/token/"

# 1. Generate PKCE Code
code_verifier, code_challenge = pkce.generate_pkce_pair()

# 2. Construct Auth URL
params = {
    "client_id": CLIENT_ID,
    "response_type": "code",
    "scope": "read write openid",
    "redirect_uri": REDIRECT_URI,
    "code_challenge": code_challenge,
    "code_challenge_method": "S256",
}
auth_request = requests.Request("GET", AUTH_URL, params=params).prepare()
print(f"Go to: {auth_request.url}")

# 3. Get Code (Manually copy from browser redirect for this script)
code = input("Enter the code from the callback URL: ")

# 4. Exchange for Token
data = {
    "grant_type": "authorization_code",
    "code": code,
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "code_verifier": code_verifier,
}
response = requests.post(TOKEN_URL, data=data)
print(response.json())
```

### JavaScript Example (Vanilla JS)
Suitable for a conceptual Single Page Application (SPA).

```javascript
const clientId = "your_client_id";
const redirectUri = "http://localhost:3000/callback";
const authEndpoint = "http://127.0.0.1:8000/o/authorize/";
const tokenEndpoint = "http://127.0.0.1:8000/o/token/";

// Helper: Generate Random String
function generateRandomString(length) {
    let text = "";
    const possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~";
    for (let i = 0; i < length; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}

// Helper: SHA256
async function sha256(plain) {
    const encoder = new TextEncoder();
    const data = encoder.encode(plain);
    const hash = await window.crypto.subtle.digest('SHA-256', data);
    return hash;
}

// Helper: Base64URL
function base64urlencode(a) {
    return btoa(String.fromCharCode.apply(null, new Uint8Array(a)))
        .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

// 1. Start Auth Flow
async function startAuth() {
    const codeVerifier = generateRandomString(128);
    // Store verifier in localStorage for step 2
    localStorage.setItem("code_verifier", codeVerifier);

    const hashed = await sha256(codeVerifier);
    const codeChallenge = base64urlencode(hashed);

    const params = new URLSearchParams({
        response_type: "code",
        client_id: clientId,
        scope: "read write openid",
        redirect_uri: redirectUri,
        code_challenge: codeChallenge,
        code_challenge_method: "S256"
    });

    window.location.href = `${authEndpoint}?${params.toString()}`;
}

// 2. Handle Callback (on callback page)
async function handleCallback() {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");
    const codeVerifier = localStorage.getItem("code_verifier");

    if (!code || !codeVerifier) return;

    const response = await fetch(tokenEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
            grant_type: "authorization_code",
            code: code,
            client_id: clientId,
            redirect_uri: redirectUri,
            code_verifier: codeVerifier
        })
    });

    const data = await response.json();
    console.log("Tokens:", data);
}
```

## 7. Best Practices

1.  **Never commit secrets**: If using a confidential client, do not commit the `client_secret` to version control. Use environment variables.
2.  **Use HTTPS**: In production, always use HTTPS to protect the token exchange and user credentials.
3.  **Validate State**: Always use the `state` parameter to prevent Cross-Site Request Forgery (CSRF) attacks. Generate a random state string, send it in the auth request, and verify it matches the state returned in the callback.
4.  **Least Privilege**: Only request the scopes your application actually needs.
