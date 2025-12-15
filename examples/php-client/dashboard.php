<?php
require_once 'config.php';
session_start();

// Handle Logout
if (isset($_GET['action']) && $_GET['action'] === 'logout') {
    session_destroy();
    header('Location: index.php');
    exit;
}

// Handle OAuth Callback
if (isset($_GET['code'])) {
    if (!isset($_SESSION['code_verifier'])) {
        die("Error: Code verifier missing from session. Restart the flow from <a href='index.php'>index.php</a>.");
    }
    $verifier = $_SESSION['code_verifier'];
    
    // Exchange code for token
    $tokenResponse = make_request(TOKEN_URL, 'POST', [
        'grant_type' => 'authorization_code',
        'code' => $_GET['code'],
        'redirect_uri' => REDIRECT_URI,
        'client_id' => CLIENT_ID,
        'client_secret' => CLIENT_SECRET,
        'code_verifier' => $verifier,
    ]);

    if ($tokenResponse['code'] == 200 && isset($tokenResponse['data']['access_token'])) {
        $_SESSION['access_token'] = $tokenResponse['data']['access_token'];
        // Remove code from URL
        header('Location: dashboard.php');
        exit;
    } else {
        die("Token Exchange Failed: " . json_encode($tokenResponse));
    }
}

// Check Authentication
if (!isset($_SESSION['access_token'])) {
    header('Location: index.php');
    exit;
}

$accessToken = $_SESSION['access_token'];
$action = isset($_GET['action']) ? $_GET['action'] : 'list';
$error = null;
$message = null;

// --- ACTION HANDLERS ---

// Create Event
if ($action === 'create' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $payload = [
        'title' => $_POST['title'],
        'description' => $_POST['description'],
        'start_time' => $_POST['start_time'],
        'end_time' => $_POST['end_time'],
        'location' => $_POST['location'],
        'capacity' => $_POST['capacity'],
    ];
    $response = make_request(API_BASE . 'events/', 'POST', $payload, $accessToken);
    if ($response['code'] == 201) {
        $message = "Event created successfully!";
        $action = 'list';
    } else {
        $error = "Failed to create event: " . json_encode($response['data']);
    }
}

// Update Event
if ($action === 'edit' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $id = $_POST['id'];
    $payload = [
        'title' => $_POST['title'],
        'description' => $_POST['description'],
        'start_time' => $_POST['start_time'],
        'end_time' => $_POST['end_time'],
        'location' => $_POST['location'],
        'capacity' => $_POST['capacity'],
    ];
    // Using PUT for full update, or PATCH for partial. DRF supports both usually.
    $response = make_request(API_BASE . "events/$id/", 'PUT', $payload, $accessToken);
    if ($response['code'] == 200) {
        $message = "Event updated successfully!";
        $action = 'list';
    } else {
        $error = "Failed to update event: " . json_encode($response['data']);
    }
}

// Delete Event
if ($action === 'delete' && isset($_GET['id'])) {
    $id = $_GET['id'];
    $response = make_request(API_BASE . "events/$id/", 'DELETE', [], $accessToken);
    if ($response['code'] == 204) {
        $message = "Event deleted successfully!";
    } else {
        $error = "Failed to delete event: " . json_encode($response['data']);
    }
    $action = 'list';
}

// Fetch Events for List
$events = [];
if ($action === 'list') {
    $response = make_request(API_BASE . 'events/', 'GET', [], $accessToken);
    if ($response['code'] == 200) {
        $events = $response['data'];
    } else {
        $error = "Failed to fetch events: " . json_encode($response['data']);
    }
}

// Fetch Single Event for Edit
$editEvent = null;
if ($action === 'edit' && isset($_GET['id']) && $_SERVER['REQUEST_METHOD'] !== 'POST') {
    $id = $_GET['id'];
    $response = make_request(API_BASE . "events/$id/", 'GET', [], $accessToken);
    if ($response['code'] == 200) {
        $editEvent = $response['data'];
    } else {
        $error = "Failed to fetch event details: " . json_encode($response['data']);
        $action = 'list';
    }
}

// Determine Current User ID (for ownership checks) - simple check
$meResponse = make_request(DJANGO_BASE_URL . '/accounts/api/me/', 'GET', [], $accessToken);
$myUserData = isset($meResponse['data']) ? $meResponse['data'] : [];
$myUserId = isset($myUserData['id']) ? $myUserData['id'] : null;
$firstName = isset($myUserData['first_name']) ? $myUserData['first_name'] : '';
$lastName = isset($myUserData['last_name']) ? $myUserData['last_name'] : '';
$myFullName = trim($firstName . ' ' . $lastName);
if (empty($myFullName)) {
    $myFullName = isset($myUserData['username']) ? $myUserData['username'] : 'Unknown User';
}

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Event Horizon - Dashboard</title>
    <style>
        body { font-family: 'Courier New', monospace; background: #0f172a; color: #e2e8f0; margin: 0; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; }
        h1, h2 { color: #38bdf8; border-bottom: 1px solid #334155; padding-bottom: 10px; }
        a { color: #38bdf8; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .btn { display: inline-block; padding: 8px 16px; background: #0ea5e9; color: white; border-radius: 4px; border: none; cursor: pointer; font-family: inherit; font-weight: bold; }
        .btn:hover { background: #0284c7; }
        .btn-danger { background: #ef4444; }
        .btn-danger:hover { background: #b91c1c; }
        .card { background: #1e293b; border: 1px solid #334155; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem; }
        .event-item { border-bottom: 1px dashed #475569; padding: 15px 0; }
        .event-item:last-child { border-bottom: none; }
        .meta { color: #94a3b8; font-size: 0.9em; margin-bottom: 5px; }
        .actions { margin-top: 10px; }
        .alert { padding: 10px; margin-bottom: 20px; border-radius: 4px; }
        .alert-success { background: #064e3b; color: #a7f3d0; border: 1px solid #059669; }
        .alert-error { background: #450a0a; color: #fecaca; border: 1px solid #dc2626; }
        form label { display: block; margin-top: 10px; color: #94a3b8; }
        form input, form textarea { width: 100%; padding: 8px; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 4px; margin-top: 5px; font-family: inherit; }
        .header-row { display: flex; justify-content: space-between; align-items: center; }
        .share-link { 
            background: #334155; 
            padding: 4px 8px; 
            border-radius: 4px; 
            font-size: 0.85em; 
            color: #cbd5e1; 
            cursor: pointer;
            transition: all 0.2s;
            display: inline-block;
            user-select: none;
        }
        .share-link:hover {
            background: #475569;
            color: white;
        }
        .share-link:active {
            transform: scale(0.98);
        }
    </style>
    <script>
        function copyToClipboard(text, element) {
            navigator.clipboard.writeText(text).then(function() {
                const originalText = element.innerText;
                element.innerText = "✓ Copied to Clipboard!";
                element.style.background = "#059669"; // Green
                element.style.color = "#ffffff";
                
                setTimeout(() => {
                    element.innerText = originalText;
                    element.style.background = ""; 
                    element.style.color = "";
                }, 2000);
            }).catch(function(err) {
                console.error('Failed to copy: ', err);
                alert("Failed to copy to clipboard. Please copy manually.");
            });
        }
    </script>
</head>
<body>
<div class="container">
    <div class="header-row">
        <h1>> DASHBOARD_ACCESS</h1>
        <div>
            <span style="color: #94a3b8; margin-right: 10px;">User: <?php echo htmlspecialchars($myFullName); ?></span>
            <a href="?action=logout" class="btn btn-danger">LOGOUT</a>
        </div>
    </div>
    </div>

    <?php if ($message): ?>
        <div class="alert alert-success"><?php echo htmlspecialchars($message); ?></div>
    <?php endif; ?>
    <?php if ($error): ?>
        <div class="alert alert-error"><?php echo htmlspecialchars($error); ?></div>
    <?php endif; ?>

    <?php if ($action === 'list'): ?>
        <div class="card">
            <div class="header-row">
                <h2>Available Events</h2>
                <a href="?action=create" class="btn">Create New Event</a>
            </div>
            
            <?php if (empty($events)): ?>
                <p>No events found. System idle.</p>
            <?php else: ?>
                <?php foreach ($events as $event): ?>
                    <div class="event-item">
                        <h3><?php echo htmlspecialchars($event['title']); ?></h3>
                        <div class="meta">
                            Date: <?php echo date('Y-m-d H:i', strtotime($event['start_time'])); ?> | 
                            Loc: <?php echo htmlspecialchars($event['location']); ?> |
                            Organizer: <?php 
                                $orgFirst = isset($event['organizer']['first_name']) ? $event['organizer']['first_name'] : '';
                                $orgLast = isset($event['organizer']['last_name']) ? $event['organizer']['last_name'] : '';
                                $orgName = trim($orgFirst . ' ' . $orgLast);
                                echo htmlspecialchars(empty($orgName) ? $event['organizer']['username'] : $orgName); 
                            ?>
                        </div>
                        <p><?php echo nl2br(htmlspecialchars($event['description'])); ?></p>
<?php 
                        /* <div class="actions"> */
                        /*     <?php if (isset($event['organizer']['id']) && $event['organizer']['id'] == $myUserId): ?> */
                        /*         <a href="?action=edit&id=<?php echo $event['id']; ?>" class="btn">Edit</a> */
                        /*         <a href="?action=delete&id=<?php echo $event['id']; ?>" class="btn btn-danger" onclick="return confirm('Are you sure? This cannot be undone.');">Delete</a> */
                        /*     <?php endif; ?> */
                        /*     <span class="share-link" onclick="copyToClipboard('<?php echo DJANGO_BASE_URL . '/events/' . $event['slug']; ?>', this)">Share: <?php echo DJANGO_BASE_URL . '/events/' . $event['slug']; ?></span> */
                                /* </div> */
 /*                       <p><?php echo nl2br(htmlspecialchars($event['description'])); ?></p>*/
                        ?>
                        
                        <div class="actions">
                            <?php if (isset($event['organizer']['id']) && $event['organizer']['id'] == $myUserId): ?>
                                <a href="?action=edit&id=<?php echo $event['id']; ?>" class="btn">Edit</a>
                                <a href="?action=delete&id=<?php echo $event['id']; ?>" class="btn btn-danger" onclick="return confirm('Are you sure? This cannot be undone.');">Delete</a>
                            <?php endif; ?>
                            <span class="share-link" onclick="copyToClipboard('<?php echo DJANGO_BASE_URL . '/events/' . $event['slug']; ?>', this)">Share: <?php echo DJANGO_BASE_URL . '/events/' . $event['slug']; ?></span>
                        </div>
                    </div>
                <?php endforeach; ?>
            <?php endif; ?>
        </div>
    <?php elseif ($action === 'create' || $action === 'edit'): ?>
        <div class="card">
            <h2><?php echo $action === 'create' ? 'Create New Event' : 'Edit Event'; ?></h2>
            <form method="POST" action="?action=<?php echo $action; ?>">
                <?php if ($action === 'edit'): ?>
                    <input type="hidden" name="id" value="<?php echo htmlspecialchars($editEvent['id']); ?>">
                <?php endif; ?>

                <label>Title</label>
                <input type="text" name="title" required value="<?php echo isset($editEvent['title']) ? $editEvent['title'] : ''; ?>">

                <label>Description</label>
                <textarea name="description" rows="4" required><?php echo isset($editEvent['description']) ? $editEvent['description'] : ''; ?></textarea>

                <label>Start Time</label>
                <input type="datetime-local" name="start_time" required value="<?php echo isset($editEvent['start_time']) ? date('Y-m-d\TH:i', strtotime($editEvent['start_time'])) : ''; ?>">

                <label>End Time</label>
                <input type="datetime-local" name="end_time" required value="<?php echo isset($editEvent['end_time']) ? date('Y-m-d\TH:i', strtotime($editEvent['end_time'])) : ''; ?>">

                <label>Location</label>
                <input type="text" name="location" required value="<?php echo isset($editEvent['location']) ? $editEvent['location'] : ''; ?>">

                <label>Capacity</label>
                <input type="number" name="capacity" required value="<?php echo isset($editEvent['capacity']) ? $editEvent['capacity'] : ''; ?>">

                <div style="margin-top: 20px;">
                    <button type="submit" class="btn">Save Event</button>
                    <a href="?action=list" class="btn btn-danger" style="background: #475569;">Cancel</a>
                </div>
            </form>
        </div>
    <?php endif; ?>

</div>
</body>
</html>
