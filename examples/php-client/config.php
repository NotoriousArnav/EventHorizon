<?php
/*
 * Event Horizon - Futuristic Event Management Platform
 * Copyright (C) 2025-2026 Arnav Ghosh
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

// Configuration for the Barebones PHP Client

// 1. Configuration from your Django Admin Panel (Django OAuth Toolkit)
// Go to http://127.0.0.1:8000/admin/oauth2_provider/application/ add a new application.
// Client Type: Confidential
// Authorization Grant Type: Authorization code
// Redirect URIs: http://localhost:8080/dashboard.php
/*
 * QvW6nBzZEzRMNs9Gc1kBWovw5BBzJqDjF2mwkTVL
 *  pbkdf2_sha256$1200000$QGu12X4X93RYzYn3BIrE5G$8M01CXqf4IdLzL+Gj17hh8+8REVhGvCD4qgcf5z0WqY=
* */
define('CLIENT_ID', 'QvW6nBzZEzRMNs9Gc1kBWovw5BBzJqDjF2mwkTVL');
define('CLIENT_SECRET', 'pbkdf2_sha256$1200000$QGu12X4X93RYzYn3BIrE5G$8M01CXqf4IdLzL+Gj17hh8+8REVhGvCD4qgcf5z0WqY=');

// 2. URLs
define('DJANGO_BASE_URL', 'http://127.0.0.1:8000'); // Address of your running Django server
define('REDIRECT_URI', 'http://localhost:8080/'); // Address of this PHP script

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
