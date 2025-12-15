# PHP OAuth2 Client Example

This directory contains a simple, dependency-free PHP client demonstrating how to authenticate with Event Horizon using OAuth 2.0 (Authorization Code Flow with PKCE).

## Setup

1.  **Register your App:**
    *   Go to your Event Horizon Admin Panel (`/admin/oauth2_provider/application/`).
    *   Create a **Confidential** application with **Authorization code** grant type.
    *   Set **Redirect URI** to: `http://localhost:8080/callback.php`

2.  **Configure the Client:**
    *   Copy `config.example.php` to `config.php`:
        ```bash
        cp config.example.php config.php
        ```
    *   Edit `config.php` and add your **Client ID** and **Client Secret**.

3.  **Run the Client:**
    *   Start the built-in PHP server:
        ```bash
        php -S localhost:8080
        ```
    *   Open `http://localhost:8080` in your browser.

## Files

*   `index.php`: The login page. Generates PKCE challenge and redirects to Event Horizon.
*   `callback.php`: Handles the redirect from Event Horizon. Exchanges code for token and fetches user profile.
*   `config.php`: Configuration file (Git ignored).
*   `config.example.php`: Template for configuration.
