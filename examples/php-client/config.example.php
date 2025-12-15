<?php
// Configuration for the Event Horizon PHP Client

// 1. Configuration from your Django Admin Panel (Django OAuth Toolkit)
// These values should be updated with the credentials from your registered application
define('CLIENT_ID', 'YOUR_CLIENT_ID_HERE');
define('CLIENT_SECRET', 'YOUR_CLIENT_SECRET_HERE');

// 2. URLs
define('DJANGO_BASE_URL', 'http://127.0.0.1:8000'); // Address of your running Django server
define('REDIRECT_URI', 'http://localhost:8080/callback.php'); // Address of this PHP script

// 3. Endpoints (Standard OAuth2)
define('AUTHORIZE_URL', DJANGO_BASE_URL . '/o/authorize/');
define('TOKEN_URL', DJANGO_BASE_URL . '/o/token/');
define('API_URL', DJANGO_BASE_URL . '/accounts/api/'); 
?>
