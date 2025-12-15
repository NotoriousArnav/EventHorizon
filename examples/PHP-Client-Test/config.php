<?php
// Configuration for the Barebones PHP Client

// 1. Configuration from your Django Admin Panel (Django OAuth Toolkit)
// Go to http://127.0.0.1:8000/admin/oauth2_provider/application/ add a new application.
// Client Type: Confidential
// Authorization Grant Type: Authorization code
// Redirect URIs: http://localhost:8080/callback.php
define('CLIENT_ID', 'CHANGE_ME_TO_YOUR_CLIENT_ID');
define('CLIENT_SECRET', 'CHANGE_ME_TO_YOUR_CLIENT_SECRET');

// 2. URLs
define('DJANGO_BASE_URL', 'http://127.0.0.1:8000'); // Address of your running Django server
define('REDIRECT_URI', 'http://localhost:8080/callback.php'); // Address of this PHP script

// 3. Endpoints (Standard OAuth2)
define('AUTHORIZE_URL', DJANGO_BASE_URL . '/o/authorize/');
define('TOKEN_URL', DJANGO_BASE_URL . '/o/token/');
define('API_URL', DJANGO_BASE_URL . '/api/'); // Or wherever your User Profile API is located
?>
