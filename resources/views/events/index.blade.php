<x-app-layout>
    <x-slot name="header">
        <div class="flex justify-between items-center">
            <h2 class="font-semibold text-xl text-gray-200 leading-tight">
                Discover Events
            </h2>
            @auth
            <a href="{{ route('events.create') }}" class="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition">
                Create Event
            </a>
            @endauth
        </div>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            @if(session('success'))
            <div class="mb-6 bg-green-900/50 border border-green-700 text-green-200 px-4 py-3 rounded-lg">
                {{ session('success') }}
            </div>
            @endif

            @if($events->isEmpty())
            <div class="bg-gray-800 rounded-lg p-12 text-center">
                <div class="text-gray-400 text-lg mb-4">No upcoming events yet</div>
                @auth
                <a href="{{ route('events.create') }}" class="inline-block px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition">
                    Create the First Event
                </a>
                @endauth
            </div>
            @else
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                @foreach($events as $event)
                <a href="{{ route('events.show', $event) }}" class="group">
                    <div class="bg-gray-800 rounded-lg overflow-hidden border border-gray-700 hover:border-purple-600 transition">
                        @if($event->cover_image_url)
                        <div class="aspect-video bg-gray-900">
                            <img src="{{ $event->cover_image_url }}" alt="{{ $event->title }}" class="w-full h-full object-cover">
                        </div>
                        @else
                        <div class="aspect-video bg-gradient-to-br from-purple-900/50 to-blue-900/50 flex items-center justify-center">
                            <svg class="w-16 h-16 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                            </svg>
                        </div>
                        @endif
                        
                        <div class="p-5">
                            <h3 class="text-lg font-semibold text-gray-100 group-hover:text-purple-400 transition mb-2">
                                {{ $event->title }}
                            </h3>
                            
                            <div class="space-y-2 text-sm text-gray-400">
                                <div class="flex items-center">
                                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                    </svg>
                                    {{ $event->start_datetime->format('M d, Y - g:i A') }}
                                </div>
                                
                                @if($event->location)
                                <div class="flex items-center">
                                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                    </svg>
                                    {{ $event->location }}
                                </div>
                                @endif

                                @if($event->capacity)
                                <div class="flex items-center">
                                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                                    </svg>
                                    {{ $event->availableSpots() ?? $event->capacity }} spots left
                                </div>
                                @endif
                            </div>
                        </div>
                    </div>
                </a>
                @endforeach
            </div>

            <div class="mt-8">
                {{ $events->links() }}
            </div>
            @endif
        </div>
    </div>
</x-app-layout>
