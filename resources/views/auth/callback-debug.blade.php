<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>OAuth Callback Debug - Event Horizon</title>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="antialiased bg-gray-900 min-h-screen flex items-center justify-center px-4">
    <div class="max-w-4xl w-full bg-gray-800 rounded-xl shadow-2xl border border-gray-700 p-8">
        <h1 class="text-3xl font-bold text-white mb-6">🔍 OAuth Callback Debug</h1>
        
        <div class="space-y-6">
            <!-- URL Query Parameters -->
            <div>
                <h2 class="text-xl font-semibold text-indigo-400 mb-3">URL Query Parameters (?param=value)</h2>
                <pre id="query-params" class="bg-gray-900 text-green-400 p-4 rounded-lg overflow-x-auto text-sm">Checking...</pre>
            </div>

            <!-- URL Hash Parameters -->
            <div>
                <h2 class="text-xl font-semibold text-purple-400 mb-3">URL Hash Parameters (#param=value)</h2>
                <pre id="hash-params" class="bg-gray-900 text-purple-400 p-4 rounded-lg overflow-x-auto text-sm">Checking...</pre>
            </div>

            <!-- Server-Side Data -->
            <div>
                <h2 class="text-xl font-semibold text-yellow-400 mb-3">Server Received (Laravel)</h2>
                <pre class="bg-gray-900 text-yellow-400 p-4 rounded-lg overflow-x-auto text-sm">{{ json_encode(request()->all(), JSON_PRETTY_PRINT) ?: 'Nothing received' }}</pre>
            </div>

            <div class="flex gap-4">
                <a href="{{ route('login') }}" class="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition">
                    Back to Login
                </a>
                <button onclick="copyDebugInfo()" class="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition">
                    Copy Debug Info
                </button>
            </div>
        </div>
    </div>

    <script>
        // Parse URL query parameters
        const urlParams = new URLSearchParams(window.location.search);
        const queryParams = {};
        for (const [key, value] of urlParams) {
            queryParams[key] = value;
        }
        document.getElementById('query-params').textContent = JSON.stringify(queryParams, null, 2) || 'No query parameters found';

        // Parse URL hash parameters
        const hashParams = new URLSearchParams(window.location.hash.substring(1));
        const hash = {};
        for (const [key, value] of hashParams) {
            hash[key] = value;
        }
        document.getElementById('hash-params').textContent = JSON.stringify(hash, null, 2) || 'No hash parameters found';

        // Log everything
        console.log('Full URL:', window.location.href);
        console.log('Query Params:', queryParams);
        console.log('Hash Params:', hash);

        // If we have tokens in hash, try to process them
        if (hash.access_token) {
            console.log('✅ Found access_token in hash!');
            console.log('We need to handle hash-based OAuth flow');
            
            // Show alert
            alert('Found tokens in URL hash! This means Supabase is using implicit flow. We need to update the code to handle this.');
        }

        function copyDebugInfo() {
            const info = {
                url: window.location.href,
                query: queryParams,
                hash: hash,
                server: {{ Js::from(request()->all()) }}
            };
            navigator.clipboard.writeText(JSON.stringify(info, null, 2));
            alert('Debug info copied to clipboard!');
        }

        // Auto-redirect if we have hash tokens
        if (hash.access_token && hash.refresh_token) {
            setTimeout(() => {
                // Send to server via AJAX
                fetch('{{ route("wallet.login") }}', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content
                    },
                    body: JSON.stringify({
                        access_token: hash.access_token,
                        refresh_token: hash.refresh_token,
                        provider: 'github'
                    })
                }).then(() => {
                    window.location.href = '/dashboard';
                });
            }, 3000);
        }
    </script>
</body>
</html>
