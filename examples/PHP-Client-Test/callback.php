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
    // curl_close($ch);
    return json_decode($response, true);
}

function make_get_request($url, $accessToken) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "Authorization: Bearer " . $accessToken
    ]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    $response = curl_exec($ch);
    // curl_close($ch);
    return json_decode($response, true);
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
        // STEP 1: Exchange the Authorization Code for an Access Token
        echo "<div class='card'>";
        echo "<h2>1. Code Exchange Protocol</h2>";
        echo "<p>Received Authorization Code: " . htmlspecialchars($_GET['code']) . "</p>";

        $tokenResponse = make_post_request(TOKEN_URL, [
            'grant_type' => 'authorization_code',
            'code' => $_GET['code'],
            'redirect_uri' => REDIRECT_URI,
            'client_id' => CLIENT_ID,
            'client_secret' => CLIENT_SECRET,
        ]);

        if (isset($tokenResponse['access_token'])) {
            $accessToken = $tokenResponse['access_token'];
            echo "<p style='color: #4ade80'>[✓] Access Token Acquired</p>";
            echo "<pre>" . $accessToken . "</pre>";
            
            // STEP 2: Use Token to Fetch Data from Django API
            echo "</div><div class='card'>";
            echo "<h2>2. Data Retrieval Protocol</h2>";
            echo "<p>Fetching user data from <code>/api/users/me/</code>...</p>";

            // NOTE: You might need to adjust this endpoint based on your exact URL structure in 'users/urls.py'
            // Commonly it might be '/api/auth/user/', '/api/users/profile/', or similar.
            // Using a generic guess here, you might need to update this line.
            $apiEndpoint = API_URL . 'users/me/'; 
            
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
