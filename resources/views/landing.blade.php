<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}" class="dark">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Event Horizon - Event Management</title>
        <link rel="preconnect" href="https://fonts.bunny.net">
        <link href="https://fonts.bunny.net/css?family=inter:400,500,600,700&display=swap" rel="stylesheet" />
        @vite(['resources/css/app.css', 'resources/js/app.js'])
        <style>
            @keyframes rotate {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.6; }
            }

            @keyframes drift {
                0%, 100% { transform: translate(0, 0); }
                50% { transform: translate(20px, -20px); }
            }

            .black-hole {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 400px;
                height: 400px;
                pointer-events: none;
            }

            .black-hole-core {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 120px;
                height: 120px;
                background: radial-gradient(circle, rgba(0, 0, 0, 1) 0%, rgba(10, 10, 20, 0.95) 40%, transparent 70%);
                border-radius: 50%;
                box-shadow: 
                    0 0 40px 10px rgba(99, 102, 241, 0.4),
                    0 0 80px 20px rgba(99, 102, 241, 0.2),
                    inset 0 0 40px rgba(0, 0, 0, 0.8);
            }

            .accretion-disk {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 100%;
                height: 100%;
            }

            .disk-ring {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                border-radius: 50%;
                border: 2px solid;
                animation: rotate 20s linear infinite;
            }

            .disk-ring:nth-child(1) {
                width: 200px;
                height: 200px;
                border-color: rgba(99, 102, 241, 0.6);
                animation-duration: 15s;
            }

            .disk-ring:nth-child(2) {
                width: 260px;
                height: 260px;
                border-color: rgba(139, 92, 246, 0.5);
                animation-duration: 20s;
                animation-direction: reverse;
            }

            .disk-ring:nth-child(3) {
                width: 320px;
                height: 320px;
                border-color: rgba(99, 102, 241, 0.3);
                animation-duration: 25s;
            }

            .disk-ring:nth-child(4) {
                width: 380px;
                height: 380px;
                border-color: rgba(139, 92, 246, 0.2);
                animation-duration: 30s;
                animation-direction: reverse;
            }

            .particle {
                position: absolute;
                width: 3px;
                height: 3px;
                background: white;
                border-radius: 50%;
                animation: pulse 2s ease-in-out infinite;
            }

            .particle:nth-child(5) { top: 20%; left: 30%; animation-delay: 0s; }
            .particle:nth-child(6) { top: 40%; left: 70%; animation-delay: 0.5s; }
            .particle:nth-child(7) { top: 60%; left: 20%; animation-delay: 1s; }
            .particle:nth-child(8) { top: 80%; left: 60%; animation-delay: 1.5s; }
            .particle:nth-child(9) { top: 30%; left: 80%; animation-delay: 0.3s; }
            .particle:nth-child(10) { top: 70%; left: 40%; animation-delay: 0.8s; }

            .gravitational-lens {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 450px;
                height: 450px;
                border-radius: 50%;
                background: radial-gradient(circle, transparent 50%, rgba(99, 102, 241, 0.05) 60%, transparent 80%);
                animation: pulse 4s ease-in-out infinite;
            }

            .stars {
                position: absolute;
                inset: 0;
                overflow: hidden;
            }

            .star {
                position: absolute;
                width: 2px;
                height: 2px;
                background: white;
                border-radius: 50%;
                animation: pulse 3s ease-in-out infinite;
            }
        </style>
    </head>
    <body class="antialiased bg-gray-900 overflow-x-hidden">
        <!-- Navigation -->
        <nav class="fixed w-full z-50 bg-gray-900/80 backdrop-blur-lg border-b border-gray-800">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between items-center h-16">
                    <div class="flex items-center gap-2">
                        <svg class="w-8 h-8 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <circle cx="12" cy="12" r="9" stroke-width="2"/>
                            <circle cx="12" cy="12" r="4" fill="currentColor"/>
                        </svg>
                        <span class="text-xl font-bold text-white">Event Horizon</span>
                    </div>
                    <div class="flex items-center gap-4">
                        @if(session()->has('supabase_access_token'))
                            <a href="{{ url('/dashboard') }}" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition">Dashboard</a>
                        @else
                            <a href="{{ route('login') }}" class="text-gray-300 hover:text-indigo-400 transition">Login</a>
                            <a href="{{ route('register') }}" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition">Get Started</a>
                        @endif
                    </div>
                </div>
            </div>
        </nav>

        <!-- Hero Section with Black Hole -->
        <section class="relative min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8 overflow-hidden">
            <!-- Animated Stars Background -->
            <div class="stars">
                <div class="star" style="top: 10%; left: 15%; animation-delay: 0s;"></div>
                <div class="star" style="top: 20%; left: 80%; animation-delay: 0.5s;"></div>
                <div class="star" style="top: 30%; left: 30%; animation-delay: 1s;"></div>
                <div class="star" style="top: 40%; left: 60%; animation-delay: 1.5s;"></div>
                <div class="star" style="top: 50%; left: 90%; animation-delay: 0.3s;"></div>
                <div class="star" style="top: 60%; left: 20%; animation-delay: 0.8s;"></div>
                <div class="star" style="top: 70%; left: 70%; animation-delay: 1.2s;"></div>
                <div class="star" style="top: 80%; left: 40%; animation-delay: 0.6s;"></div>
                <div class="star" style="top: 15%; left: 50%; animation-delay: 1.8s;"></div>
                <div class="star" style="top: 85%; left: 85%; animation-delay: 0.4s;"></div>
            </div>

            <!-- Black Hole Animation -->
            <div class="black-hole">
                <div class="gravitational-lens"></div>
                <div class="accretion-disk">
                    <div class="disk-ring"></div>
                    <div class="disk-ring"></div>
                    <div class="disk-ring"></div>
                    <div class="disk-ring"></div>
                    <div class="particle"></div>
                    <div class="particle"></div>
                    <div class="particle"></div>
                    <div class="particle"></div>
                    <div class="particle"></div>
                    <div class="particle"></div>
                </div>
                <div class="black-hole-core"></div>
            </div>

            <!-- Hero Content -->
            <div class="relative z-10 max-w-7xl mx-auto text-center">
                <h1 class="text-5xl md:text-6xl lg:text-7xl font-bold text-white mb-6">
                    Manage Events at the
                    <span class="bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">Event Horizon</span>
                </h1>
                <p class="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">
                    The ultimate event management platform. Create, organize, and track events with ease.
                </p>
                <div class="flex gap-4 justify-center flex-wrap">
                    @if(session()->has('supabase_access_token'))
                        <a href="{{ url('/dashboard') }}" class="px-8 py-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-lg font-semibold transition shadow-lg shadow-indigo-500/50 hover:shadow-indigo-500/70">
                            Go to Dashboard
                        </a>
                    @else
                        <a href="{{ route('register') }}" class="px-8 py-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-lg font-semibold transition shadow-lg shadow-indigo-500/50 hover:shadow-indigo-500/70">
                            Start Free Trial
                        </a>
                        <a href="#features" class="px-8 py-4 bg-gray-800 hover:bg-gray-700 text-white rounded-lg text-lg font-semibold transition border border-gray-700">
                            Learn More
                        </a>
                    @endif
                </div>
            </div>
        </section>

        <!-- Features Section -->
        <section id="features" class="py-20 bg-gray-950 border-t border-gray-800">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="text-center mb-16">
                    <h2 class="text-4xl font-bold text-white mb-4">Everything You Need</h2>
                    <p class="text-xl text-gray-400">Powerful features to manage your events</p>
                </div>

                <div class="grid md:grid-cols-3 gap-8">
                    <!-- Feature 1 -->
                    <div class="bg-gray-800 p-8 rounded-xl shadow-lg hover:shadow-2xl transition border border-gray-700 hover:border-indigo-500/50">
                        <div class="w-12 h-12 bg-indigo-900 rounded-lg flex items-center justify-center mb-4">
                            <svg class="w-6 h-6 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                            </svg>
                        </div>
                        <h3 class="text-xl font-semibold text-white mb-2">Event Management</h3>
                        <p class="text-gray-400">Create and manage unlimited events with detailed information and customization.</p>
                    </div>

                    <!-- Feature 2 -->
                    <div class="bg-gray-800 p-8 rounded-xl shadow-lg hover:shadow-2xl transition border border-gray-700 hover:border-green-500/50">
                        <div class="w-12 h-12 bg-green-900 rounded-lg flex items-center justify-center mb-4">
                            <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                            </svg>
                        </div>
                        <h3 class="text-xl font-semibold text-white mb-2">Attendee Tracking</h3>
                        <p class="text-gray-400">Monitor attendee numbers and manage registrations efficiently.</p>
                    </div>

                    <!-- Feature 3 -->
                    <div class="bg-gray-800 p-8 rounded-xl shadow-lg hover:shadow-2xl transition border border-gray-700 hover:border-purple-500/50">
                        <div class="w-12 h-12 bg-purple-900 rounded-lg flex items-center justify-center mb-4">
                            <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                            </svg>
                        </div>
                        <h3 class="text-xl font-semibold text-white mb-2">Analytics Dashboard</h3>
                        <p class="text-gray-400">Get insights with comprehensive statistics and event analytics.</p>
                    </div>

                    <!-- Feature 4 -->
                    <div class="bg-gray-800 p-8 rounded-xl shadow-lg hover:shadow-2xl transition border border-gray-700 hover:border-yellow-500/50">
                        <div class="w-12 h-12 bg-yellow-900 rounded-lg flex items-center justify-center mb-4">
                            <svg class="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                            </svg>
                        </div>
                        <h3 class="text-xl font-semibold text-white mb-2">Location Management</h3>
                        <p class="text-gray-400">Organize events by location and venue information.</p>
                    </div>

                    <!-- Feature 5 -->
                    <div class="bg-gray-800 p-8 rounded-xl shadow-lg hover:shadow-2xl transition border border-gray-700 hover:border-red-500/50">
                        <div class="w-12 h-12 bg-red-900 rounded-lg flex items-center justify-center mb-4">
                            <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                            </svg>
                        </div>
                        <h3 class="text-xl font-semibold text-white mb-2">Real-time Updates</h3>
                        <p class="text-gray-400">Get instant updates on event changes and attendee activity.</p>
                    </div>

                    <!-- Feature 6 -->
                    <div class="bg-gray-800 p-8 rounded-xl shadow-lg hover:shadow-2xl transition border border-gray-700 hover:border-blue-500/50">
                        <div class="w-12 h-12 bg-blue-900 rounded-lg flex items-center justify-center mb-4">
                            <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                            </svg>
                        </div>
                        <h3 class="text-xl font-semibold text-white mb-2">Secure & Reliable</h3>
                        <p class="text-gray-400">Enterprise-grade security with Laravel and Supabase backend.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- CTA Section -->
        <section class="py-20 bg-gray-900 border-t border-gray-800">
            <div class="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
                <h2 class="text-4xl font-bold text-white mb-4">Ready to Get Started?</h2>
                <p class="text-xl text-gray-400 mb-8">Join thousands of event organizers using Event Horizon</p>
                @if(!session()->has('supabase_access_token'))
                    <a href="{{ route('register') }}" class="inline-block px-8 py-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-lg font-semibold transition shadow-lg shadow-indigo-500/50 hover:shadow-indigo-500/70">
                        Create Your Free Account
                    </a>
                @endif
            </div>
        </section>

        <!-- Footer -->
        <footer class="bg-gray-950 border-t border-gray-800 py-12">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                <p class="text-gray-500">&copy; 2025 Event Horizon. Built with Laravel & Alpine.js</p>
            </div>
        </footer>
    </body>
</html>
