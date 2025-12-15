<?php
require_once 'config.php';
session_start();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Event Horizon - Client Access</title>
    <style>
        body { font-family: 'Courier New', monospace; background: #0f172a; color: #e2e8f0; text-align: center; height: 100%; margin: 0; padding-top: 50px; }
        .terminal { 
            border: 1px solid #334155; 
            padding: 2rem; 
            background: #1e293b; 
            border-radius: 8px; /* CSS3 - degrades gracefully */
            width: 400px; 
            margin: 0 auto; 
            text-align: left;
        }
        h1 { color: #38bdf8; margin-top: 0; border-bottom: 1px solid #334155; padding-bottom: 10px; }
        .btn { display: block; width: 90%; padding: 10px; background: #0ea5e9; color: white; text-align: center; text-decoration: none; font-weight: bold; margin-top: 20px; border: 1px solid #0284c7; }
        .btn:hover { background: #0284c7; }
        .status { margin-top: 15px; font-size: 0.9em; color: #94a3b8; }
    </style>
</head>
<body>

<div class="terminal">
    <h1>&gt; TERMINAL_ACCESS</h1>
    <p>Connect to the Event Horizon Mainframe using your credentials.</p>
    
    <?php
    // Polyfill for random_bytes (PHP < 7)
    if (!function_exists('random_bytes')) {
        function random_bytes($length = 10) {
            if (function_exists('openssl_random_pseudo_bytes')) {
                return openssl_random_pseudo_bytes($length);
            }
            // Fallback for extremely old systems
            $result = '';
            for ($i = 0; $i < $length; $i++) {
                $result .= chr(mt_rand(0, 255));
            }
            return $result;
        }
    }

    // 1. Generate PKCE Verifier and Challenge
    // Always generate a fresh verifier to prevent stale session issues
    $random = bin2hex(random_bytes(32));
    $_SESSION['code_verifier'] = $random;
    $verifier = $_SESSION['code_verifier'];

    // Challenge = Base64Url(SHA256(verifier))
    $hash = hash('sha256', $verifier, true);
    $challenge = rtrim(strtr(base64_encode($hash), '+/', '-_'), '=');

    // 2. Construct the Authorization URL
    // This redirects the user to Django to say "Yes, I allow this app"
    $queryParams = http_build_query(array(
        'client_id' => CLIENT_ID,
        'redirect_uri' => REDIRECT_URI,
        'response_type' => 'code',
        'scope' => 'openid read write',
        'code_challenge' => $challenge,
        'code_challenge_method' => 'S256',
    ));
    
    $loginUrl = AUTHORIZE_URL . '?' . $queryParams;
    ?>

    <a href="<?php echo $loginUrl; ?>" class="btn">INITIALIZE_OAUTH_SEQUENCE [LOGIN]</a>

    <div class="status">
        Target: <?php echo DJANGO_BASE_URL; ?><br>
        Client ID: <?php echo substr(CLIENT_ID, 0, 5) . '...'; ?>
    </div>
</div>

</body>
</html>
