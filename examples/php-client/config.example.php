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
