<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-200 leading-tight">
            Dashboard
        </h2>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <!-- Stats Cards -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <!-- Total Events -->
                <div class="bg-gray-800 overflow-hidden shadow-sm sm:rounded-lg border border-gray-700">
                    <div class="p-6">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm text-gray-400">Total Events</p>
                                <p class="text-3xl font-bold text-gray-100">{{ $totalEvents }}</p>
                            </div>
                            <div class="p-3 bg-purple-900/50 rounded-full">
                                <svg class="w-8 h-8 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Upcoming Events -->
                <div class="bg-gray-800 overflow-hidden shadow-sm sm:rounded-lg border border-gray-700">
                    <div class="p-6">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm text-gray-400">Upcoming Events</p>
                                <p class="text-3xl font-bold text-gray-100">{{ $upcomingEvents }}</p>
                            </div>
                            <div class="p-3 bg-green-900/50 rounded-full">
                                <svg class="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Total Registrations -->
                <div class="bg-gray-800 overflow-hidden shadow-sm sm:rounded-lg border border-gray-700">
                    <div class="p-6">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm text-gray-400">Total Registrations</p>
                                <p class="text-3xl font-bold text-gray-100">{{ $totalRegistrations }}</p>
                            </div>
                            <div class="p-3 bg-blue-900/50 rounded-full">
                                <svg class="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Quick Actions -->
            <div class="bg-gray-800 overflow-hidden shadow-sm sm:rounded-lg border border-gray-700 mb-8">
                <div class="p-6">
                    <h3 class="text-lg font-semibold text-gray-100 mb-4">Quick Actions</h3>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <a href="{{ route('events.create') }}" class="flex items-center space-x-3 p-4 bg-purple-900/30 hover:bg-purple-900/50 border border-purple-700 rounded-lg transition">
                            <svg class="w-8 h-8 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                            </svg>
                            <div>
                                <p class="text-sm font-medium text-gray-200">Create Event</p>
                                <p class="text-xs text-gray-400">Start a new event</p>
                            </div>
                        </a>

                        <a href="{{ route('events.index') }}" class="flex items-center space-x-3 p-4 bg-blue-900/30 hover:bg-blue-900/50 border border-blue-700 rounded-lg transition">
                            <svg class="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                            </svg>
                            <div>
                                <p class="text-sm font-medium text-gray-200">Browse Events</p>
                                <p class="text-xs text-gray-400">View all events</p>
                            </div>
                        </a>

                        <a href="{{ route('profile.edit') }}" class="flex items-center space-x-3 p-4 bg-gray-700/50 hover:bg-gray-700 border border-gray-600 rounded-lg transition">
                            <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                            </svg>
                            <div>
                                <p class="text-sm font-medium text-gray-200">Profile Settings</p>
                                <p class="text-xs text-gray-400">Update your profile</p>
                            </div>
                        </a>
                    </div>
                </div>
            </div>

            <!-- Your Events -->
            <div class="bg-gray-800 overflow-hidden shadow-sm sm:rounded-lg border border-gray-700">
                <div class="p-6">
                    <div class="flex justify-between items-center mb-6">
                        <h3 class="text-lg font-semibold text-gray-100">Your Events</h3>
                        <a href="{{ route('events.create') }}" class="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition text-sm">
                            + Create Event
                        </a>
                    </div>

                    @if($recentEvents->isEmpty())
                    <div class="text-center py-12">
                        <svg class="w-16 h-16 mx-auto mb-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                        </svg>
                        <p class="text-gray-400 mb-4">You haven't created any events yet</p>
                        <a href="{{ route('events.create') }}" class="inline-block px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition">
                            Create Your First Event
                        </a>
                    </div>
                    @else
                    <div class="space-y-4">
                        @foreach($recentEvents as $event)
                        <div class="border border-gray-700 rounded-lg p-4 hover:border-purple-600 transition">
                            <div class="flex justify-between items-start">
                                <div class="flex-1">
                                    <div class="flex items-center space-x-2 mb-2">
                                        <h4 class="text-lg font-semibold text-gray-100">{{ $event->title }}</h4>
                                        <span class="px-2 py-1 text-xs rounded-full
                                            @if($event->status === 'published') bg-green-900/50 text-green-300
                                            @elseif($event->status === 'draft') bg-yellow-900/50 text-yellow-300
                                            @else bg-gray-700 text-gray-300
                                            @endif">
                                            {{ ucfirst($event->status) }}
                                        </span>
                                    </div>
                                    
                                    <div class="flex flex-wrap gap-4 text-sm text-gray-400">
                                        <span class="flex items-center">
                                            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                                            </svg>
                                            {{ $event->start_datetime->format('M d, Y - g:i A') }}
                                        </span>
                                        
                                        @if($event->location)
                                        <span class="flex items-center">
                                            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                                            </svg>
                                            {{ $event->location }}
                                        </span>
                                        @endif

                                        <span class="flex items-center">
                                            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"/>
                                            </svg>
                                            {{ $event->ticketTypes->count() }} ticket type(s)
                                        </span>

                                        <span class="flex items-center">
                                            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                                            </svg>
                                            {{ $event->registrations()->where('status', 'confirmed')->count() }} registrations
                                        </span>
                                    </div>
                                </div>
                                
                                <div class="flex space-x-2">
                                    <a href="{{ route('events.show', $event) }}" class="px-3 py-2 bg-gray-700 hover:bg-gray-600 text-gray-200 rounded-lg transition text-sm">
                                        View
                                    </a>
                                    <a href="{{ route('events.edit', $event) }}" class="px-3 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition text-sm">
                                        Edit
                                    </a>
                                </div>
                            </div>
                        </div>
                        @endforeach
                    </div>

                    @if($events->count() > 5)
                    <div class="mt-6 text-center">
                        <a href="{{ route('events.index') }}" class="text-purple-400 hover:text-purple-300 transition">
                            View All Events →
                        </a>
                    </div>
                    @endif
                    @endif
                </div>
            </div>
        </div>
    </div>
</x-app-layout>
