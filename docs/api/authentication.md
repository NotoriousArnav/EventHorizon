# Authentication

## Bearer Token Authentication

All API requests (except public GET requests) require an `Authorization` header.

```http
Authorization: Bearer <access_token>
```

## Obtaining Tokens

### 1. Authorization Request
Redirect the user to:
```
/o/authorize/?response_type=code&client_id=<your_client_id>&redirect_uri=<your_redirect_uri>
```

### 2. Token Exchange
Exchange the returned `code` for an access token via `POST /o/token/`:
```json
{
    "grant_type": "authorization_code",
    "code": "received_code",
    "redirect_uri": "your_redirect_uri",
    "client_id": "your_client_id",
    "client_secret": "your_client_secret"
}
```

## Session Authentication
For browser-based clients on the same domain, standard Django session cookies are used automatically.
