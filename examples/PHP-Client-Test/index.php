<?php
require_once 'config.php';
session_start();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Event Horizon - Lab Client</title>
    <style>
        body { font-family: monospace; background: #0f172a; color: #e2e8f0; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .terminal { border: 1px solid #334155; padding: 2rem; background: #1e293b; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); max-width: 400px; width: 100%; }
        h1 { color: #38bdf8; margin-top: 0; border-bottom: 1px solid #334155; padding-bottom: 10px; }
        .btn { display: block; width: 100%; padding: 10px; background: #0ea5e9; color: white; text-align: center; text-decoration: none; border-radius: 4px; font-weight: bold; margin-top: 20px; transition: background 0.2s; }
        .btn:hover { background: #0284c7; }
        .status { margin-top: 15px; font-size: 0.9em; color: #94a3b8; }
    </style>
</head>
<body>

<div class="terminal">
    <h1>> TERMINAL_ACCESS</h1>
    <p>Connect to the Event Horizon Mainframe using your credentials.</p>
    
    <?php
    // Construct the Authorization URL
    // This redirects the user to Django to say "Yes, I allow this app"
    $queryParams = http_build_query([
        'client_id' => CLIENT_ID,
        'redirect_uri' => REDIRECT_URI,
        'response_type' => 'code',
        // 'scope' => 'read write' // Optional: depending on your Django setup
    ]);
    
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
