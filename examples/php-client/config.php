<?php
// Configuration for the Barebones PHP Client

// 1. Configuration from your Django Admin Panel (Django OAuth Toolkit)
// Go to http://127.0.0.1:8000/admin/oauth2_provider/application/ add a new application.
// Client Type: Confidential
// Authorization Grant Type: Authorization code
// Redirect URIs: http://localhost:8080/dashboard.php
define('CLIENT_ID', 'C3xHvWKvXPOc8P9HGwrwdC5CpLpbVv8TDp1FWg5g');
define('CLIENT_SECRET', 'rvbSZrCImRqoZXIGvBC11lD1vkZWtYEai97RKcpizbwB5pbDgVRUdGAFSiePsrkNgOiZLckO4TxqfD9WeLJC3hL9kjKMesuLtzTqR7Fyh0kualGEVp9iKOgKfo9mHzFL');

// 2. URLs
define('DJANGO_BASE_URL', 'http://127.0.0.1:8000'); // Address of your running Django server
define('REDIRECT_URI', 'http://localhost:8080/dashboard.php'); // Address of this PHP script

// 3. Endpoints (Standard OAuth2)
define('AUTHORIZE_URL', DJANGO_BASE_URL . '/o/authorize/');
define('TOKEN_URL', DJANGO_BASE_URL . '/o/token/');
define('API_BASE', DJANGO_BASE_URL . '/api/'); // Points to our new centralized API router

// Helper function for cURL requests
function make_request($url, $method = 'GET', $data = [], $accessToken = null) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    // Disable SSL verification for Lab/Dev environments
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

    $headers = [];
    if ($accessToken) {
        $headers[] = "Authorization: Bearer " . $accessToken;
    }

    if ($method === 'POST') {
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
    } elseif ($method === 'PUT' || $method === 'PATCH' || $method === 'DELETE') {
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
        if (!empty($data)) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
        }
    }

    if (!empty($headers)) {
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    }

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    
    if ($response === false) {
        return ['error' => 'cURL Error: ' . curl_error($ch)];
    }
    
    curl_close($ch);

    $decoded = json_decode($response, true);
    return ['code' => $httpCode, 'data' => $decoded];
}
?>
