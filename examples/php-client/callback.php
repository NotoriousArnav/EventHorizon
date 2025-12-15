<?php
require_once 'config.php';
session_start();

// Helper function for cURL requests to keep code clean
function make_post_request($url, $params) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($params));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    // Disable SSL verification for Lab/Dev environments (NOT FOR PRODUCTION)
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    $response = curl_exec($ch);
    
    if ($response === false) {
        return array('error' => 'cURL Error: ' . curl_error($ch));
    }
    
    // Attempt decode
    $decoded = json_decode($response, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        return array('error' => 'JSON Decode Error', 'raw_response' => $response);
    }
    
    return $decoded;
}

function make_get_request($url, $accessToken) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        "Authorization: Bearer " . $accessToken
    ));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    $response = curl_exec($ch);
    
    if ($response === false) {
        return array('error' => 'cURL Error: ' . curl_error($ch));
    }
    
    // Attempt decode
    $decoded = json_decode($response, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        return array('error' => 'JSON Decode Error', 'raw_response' => $response);
    }
    
    return $decoded;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Event Horizon - Access Granted</title>
    <style>
        body { font-family: monospace; background: #0f172a; color: #e2e8f0; padding: 2rem; }
        .container { max-width: 800px; margin: 0 auto; }
        .card { background: #1e293b; border: 1px solid #334155; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem; }
        h1 { color: #4ade80; border-bottom: 1px dashed #4ade80; padding-bottom: 10px; }
        h2 { color: #38bdf8; margin-top: 0; }
        pre { background: #0f172a; padding: 10px; border-radius: 4px; overflow-x: auto; color: #fbbf24; }
        .error { color: #ef4444; }
    </style>
</head>
<body>
<div class="container">

    <h1>> ACCESS_GRANTED</h1>

    <?php
    if (isset($_GET['code'])) {
        // Retrieve the verifier we stored before redirecting
        if (!isset($_SESSION['code_verifier'])) {
            die("Error: Code verifier missing from session. Restart the flow.");
        }
        $verifier = $_SESSION['code_verifier'];

        // STEP 1: Exchange the Authorization Code for an Access Token
        echo "<div class='card'>";
        echo "<h2>1. Code Exchange Protocol</h2>";
        echo "<p>Received Authorization Code: " . htmlspecialchars($_GET['code']) . "</p>";

        $tokenResponse = make_post_request(TOKEN_URL, array(
            'grant_type' => 'authorization_code',
            'code' => $_GET['code'],
            'redirect_uri' => REDIRECT_URI,
            'client_id' => CLIENT_ID,
            'client_secret' => CLIENT_SECRET,
            'code_verifier' => $verifier,
        ));

        if (isset($tokenResponse['access_token'])) {
            $accessToken = $tokenResponse['access_token'];
            echo "<p style='color: #4ade80'>[✓] Access Token Acquired</p>";
            echo "<pre>" . $accessToken . "</pre>";
            
            // STEP 2: Use Token to Fetch Data from Django API
            echo "</div><div class='card'>";
            echo "<h2>2. Data Retrieval Protocol</h2>";
            echo "<p>Fetching user data from <code>/api/me/</code>...</p>";

            // Update this endpoint to match your 'users/urls.py'
            // The default accounts/api/me/ is used in dashboard.php
            $apiEndpoint = DJANGO_BASE_URL . '/accounts/api/me/'; 
            
            $userData = make_get_request($apiEndpoint, $accessToken);

            echo "<p>Server Response:</p>";
            echo "<pre>";
            print_r($userData);
            echo "</pre>";
            echo "</div>";

        } else {
            echo "<div class='error'>[!] Token Exchange Failed</div>";
            echo "<pre>";
            print_r($tokenResponse);
            echo "</pre>";
            echo "</div>";
        }
    } else {
        echo "<div class='card error'>[!] No Authorization Code received. Initialize sequence from index.php.</div>";
    }
    ?>

    <p><a href="index.php" style="color: #94a3b8"><< Return to Login</a></p>
</div>
</body>
</html>
