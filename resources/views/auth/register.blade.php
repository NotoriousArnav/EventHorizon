<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}" class="dark">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>Register - Event Horizon</title>
    <link rel="preconnect" href="https://fonts.bunny.net">
    <link href="https://fonts.bunny.net/css?family=inter:400,500,600,700&display=swap" rel="stylesheet" />
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="antialiased bg-gray-900 min-h-screen flex items-center justify-center px-4 py-12">
    <!-- Background Stars -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
        <div class="absolute w-1 h-1 bg-white rounded-full opacity-70" style="top: 10%; left: 15%;"></div>
        <div class="absolute w-1 h-1 bg-white rounded-full opacity-50" style="top: 20%; left: 80%;"></div>
        <div class="absolute w-1 h-1 bg-white rounded-full opacity-60" style="top: 30%; left: 30%;"></div>
        <div class="absolute w-1 h-1 bg-white rounded-full opacity-80" style="top: 70%; left: 70%;"></div>
        <div class="absolute w-1 h-1 bg-white rounded-full opacity-40" style="top: 85%; left: 20%;"></div>
    </div>

    <div class="relative z-10 w-full max-w-md">
        <!-- Logo -->
        <div class="text-center mb-8">
            <a href="/" class="inline-flex items-center gap-2 text-white hover:text-indigo-400 transition">
                <svg class="w-10 h-10 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="9" stroke-width="2"/>
                    <circle cx="12" cy="12" r="4" fill="currentColor"/>
                </svg>
                <span class="text-2xl font-bold">Event Horizon</span>
            </a>
            <h1 class="text-2xl font-bold text-white mt-4">Create Account</h1>
            <p class="text-gray-400 mt-2">Start managing your events today</p>
        </div>

        <!-- Register Card -->
        <div class="bg-gray-800 rounded-xl shadow-2xl border border-gray-700 p-8">
            <!-- Errors -->
            @if ($errors->any())
                <div class="mb-4 p-4 bg-red-900/50 border border-red-700 text-red-300 rounded-lg text-sm">
                    <ul class="list-disc list-inside">
                        @foreach ($errors->all() as $error)
                            <li>{{ $error }}</li>
                        @endforeach
                    </ul>
                </div>
            @endif

            <form method="POST" action="{{ route('supabase.register') }}">
                @csrf

                <!-- Name -->
                <div class="mb-4">
                    <label for="name" class="block text-sm font-medium text-gray-300 mb-2">Name</label>
                    <input id="name" type="text" name="name" value="{{ old('name') }}" required autofocus
                        class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition">
                </div>

                <!-- Email -->
                <div class="mb-4">
                    <label for="email" class="block text-sm font-medium text-gray-300 mb-2">Email</label>
                    <input id="email" type="email" name="email" value="{{ old('email') }}" required
                        class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition">
                </div>

                <!-- Password -->
                <div class="mb-4">
                    <label for="password" class="block text-sm font-medium text-gray-300 mb-2">Password</label>
                    <input id="password" type="password" name="password" required
                        class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition">
                    <p class="mt-1 text-xs text-gray-400">Must be at least 6 characters</p>
                </div>

                <!-- Confirm Password -->
                <div class="mb-6">
                    <label for="password_confirmation" class="block text-sm font-medium text-gray-300 mb-2">Confirm Password</label>
                    <input id="password_confirmation" type="password" name="password_confirmation" required
                        class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition">
                </div>

                <!-- Submit Button -->
                <button type="submit" class="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg transition shadow-lg shadow-indigo-500/50 hover:shadow-indigo-500/70">
                    Create Account
                </button>
            </form>

            <!-- Divider -->
            <div class="relative my-6">
                <div class="absolute inset-0 flex items-center">
                    <div class="w-full border-t border-gray-700"></div>
                </div>
                <div class="relative flex justify-center text-sm">
                    <span class="px-4 bg-gray-800 text-gray-400">Or continue with</span>
                </div>
            </div>

            <!-- OAuth Buttons -->
            <div class="grid grid-cols-2 gap-3">
                <button @click="connectWallet()" type="button" class="flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 border border-purple-500 rounded-lg text-white font-medium transition shadow-lg shadow-purple-500/50">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M20 7h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2zM10 4h4v3h-4V4zm10 16H4V9h16v11z"/>
                        <path d="M9 12h2v2H9v-2zm4 0h2v2h-2v-2z"/>
                    </svg>
                    Web3 Wallet
                </button>
                <a href="{{ route('supabase.oauth', 'github') }}" class="flex items-center justify-center gap-2 px-4 py-3 bg-gray-700 hover:bg-gray-600 border border-gray-600 rounded-lg text-white font-medium transition">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
                    </svg>
                    GitHub
                </a>
            </div>

            <!-- Login Link -->
            <p class="mt-6 text-center text-sm text-gray-400">
                Already have an account?
                <a href="{{ route('login') }}" class="text-indigo-400 hover:text-indigo-300 font-medium transition">
                    Sign in
                </a>
            </p>
        </div>
    </div>
</body>
</html>

    <script>
        function connectWallet() {
            if (typeof window.ethereum !== 'undefined') {
                window.ethereum.request({ method: 'eth_requestAccounts' })
                    .then(accounts => {
                        const address = accounts[0];
                        // Send wallet address to backend for authentication
                        fetch('/auth/wallet/register', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content
                            },
                            body: JSON.stringify({ address: address })
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                window.location.href = '/dashboard';
                            } else {
                                alert('Wallet authentication failed. Please try again.');
                            }
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            alert('An error occurred. Please try again.');
                        });
                    })
                    .catch(error => {
                        console.error('User rejected connection:', error);
                        alert('Please connect your wallet to continue.');
                    });
            } else {
                alert('Please install MetaMask or another Web3 wallet to continue.');
                window.open('https://metamask.io/download/', '_blank');
            }
        }
    </script>
</body>
</html>
