<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>Completing Sign In...</title>
    @vite(['resources/css/app.css'])
    <style>
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .spinner {
            animation: spin 1s linear infinite;
        }
    </style>
</head>
<body class="antialiased bg-gray-900 min-h-screen flex items-center justify-center">
    <div class="text-center">
        <div class="inline-block w-16 h-16 border-4 border-indigo-500 border-t-transparent rounded-full spinner mb-4"></div>
        <h1 class="text-2xl font-bold text-white mb-2">Completing Sign In...</h1>
        <p class="text-gray-400" id="status">Processing authentication...</p>
    </div>

    <script>
        (function() {
            const statusEl = document.getElementById('status');
            
            // Extract tokens from URL hash
            const hashParams = new URLSearchParams(window.location.hash.substring(1));
            const accessToken = hashParams.get('access_token');
            const refreshToken = hashParams.get('refresh_token');
            const expiresIn = hashParams.get('expires_in');
            const providerToken = hashParams.get('provider_token');

            console.log('OAuth Callback - Hash Params:', {
                accessToken: accessToken ? 'present' : 'missing',
                refreshToken: refreshToken ? 'present' : 'missing'
            });

            if (!accessToken) {
                statusEl.textContent = 'Authentication failed - no access token';
                setTimeout(() => {
                    window.location.href = '/login?error=no_token';
                }, 2000);
                return;
            }

            // Send tokens to server
            statusEl.textContent = 'Saving authentication...';
            
            fetch('/auth/oauth/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content
                },
                body: JSON.stringify({
                    access_token: accessToken,
                    refresh_token: refreshToken,
                    expires_in: expiresIn,
                    provider_token: providerToken
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    statusEl.textContent = 'Success! Redirecting...';
                    window.location.href = data.redirect || '/dashboard';
                } else {
                    statusEl.textContent = 'Authentication failed: ' + (data.message || 'Unknown error');
                    setTimeout(() => {
                        window.location.href = '/login?error=' + encodeURIComponent(data.message || 'auth_failed');
                    }, 2000);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                statusEl.textContent = 'Network error occurred';
                setTimeout(() => {
                    window.location.href = '/login?error=network_error';
                }, 2000);
            });
        })();
    </script>
</body>
</html>
