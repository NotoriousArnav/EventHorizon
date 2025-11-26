<x-app-layout>
    <div class="min-h-screen bg-gray-900">
        <!-- Cover Image -->
        @if($event->cover_image_url)
        <div class="w-full h-96 bg-gray-800">
            <img src="{{ $event->cover_image_url }}" alt="{{ $event->title }}" class="w-full h-full object-cover">
        </div>
        @else
        <div class="w-full h-96 bg-gradient-to-br from-purple-900/50 to-blue-900/50"></div>
        @endif

        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 -mt-20">
            <div class="bg-gray-800 rounded-lg shadow-2xl border border-gray-700 overflow-hidden">
                <div class="p-8">
                    <!-- Title & Actions -->
                    <div class="flex justify-between items-start mb-6">
                        <div class="flex-1">
                            <h1 class="text-4xl font-bold text-gray-100 mb-2">{{ $event->title }}</h1>
                            
                            @if($event->community)
                            <p class="text-purple-400">
                                by {{ $event->community->name }}
                            </p>
                            @endif
                        </div>

                        @auth
                        @can('update', $event)
                        <div class="flex space-x-2">
                            <a href="{{ route('events.edit', $event) }}" class="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-gray-200 rounded-lg transition">
                                Edit
                            </a>
                            <form action="{{ route('events.destroy', $event) }}" method="POST" onsubmit="return confirm('Are you sure?')">
                                @csrf
                                @method('DELETE')
                                <button type="submit" class="px-4 py-2 bg-red-900 hover:bg-red-800 text-red-200 rounded-lg transition">
                                    Delete
                                </button>
                            </form>
                        </div>
                        @endcan
                        @endauth
                    </div>

                    <!-- Event Info Grid -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                        <!-- Date & Time -->
                        <div class="flex items-start space-x-3">
                            <div class="flex-shrink-0 w-12 h-12 bg-purple-900/50 rounded-lg flex items-center justify-center">
                                <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                </svg>
                            </div>
                            <div>
                                <p class="text-sm text-gray-400">Date & Time</p>
                                <p class="text-gray-200 font-medium">{{ $event->start_datetime->format('l, F j, Y') }}</p>
                                <p class="text-gray-300">{{ $event->start_datetime->format('g:i A') }} - {{ $event->end_datetime->format('g:i A') }}</p>
                                <p class="text-xs text-gray-500">{{ $event->timezone }}</p>
                            </div>
                        </div>

                        <!-- Location -->
                        <div class="flex items-start space-x-3">
                            <div class="flex-shrink-0 w-12 h-12 bg-purple-900/50 rounded-lg flex items-center justify-center">
                                <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                </svg>
                            </div>
                            <div>
                                <p class="text-sm text-gray-400">Location</p>
                                <p class="text-gray-200 font-medium capitalize">{{ $event->location_type }}</p>
                                @if($event->location)
                                <p class="text-gray-300">{{ $event->location }}</p>
                                @endif
                            </div>
                        </div>

                        <!-- Capacity -->
                        @if($event->capacity)
                        <div class="flex items-start space-x-3">
                            <div class="flex-shrink-0 w-12 h-12 bg-purple-900/50 rounded-lg flex items-center justify-center">
                                <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                                </svg>
                            </div>
                            <div>
                                <p class="text-sm text-gray-400">Capacity</p>
                                <p class="text-gray-200 font-medium">
                                    @if($event->isAtCapacity())
                                        <span class="text-red-400">Sold Out</span>
                                    @else
                                        {{ $event->availableSpots() }} / {{ $event->capacity }} spots available
                                    @endif
                                </p>
                            </div>
                        </div>
                        @endif

                        <!-- Status Badge -->
                        <div class="flex items-start space-x-3">
                            <div class="flex-shrink-0 w-12 h-12 bg-purple-900/50 rounded-lg flex items-center justify-center">
                                <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                            </div>
                            <div>
                                <p class="text-sm text-gray-400">Status</p>
                                <span class="inline-block px-3 py-1 text-sm font-medium rounded-full
                                    @if($event->status === 'published') bg-green-900/50 text-green-300
                                    @elseif($event->status === 'draft') bg-yellow-900/50 text-yellow-300
                                    @elseif($event->status === 'cancelled') bg-red-900/50 text-red-300
                                    @else bg-gray-700 text-gray-300
                                    @endif">
                                    {{ ucfirst($event->status) }}
                                </span>
                            </div>
                        </div>
                    </div>

                    <!-- Description -->
                    @if($event->description)
                    <div class="border-t border-gray-700 pt-6 mb-8">
                        <h2 class="text-2xl font-semibold text-gray-100 mb-4">About This Event</h2>
                        <div class="text-gray-300 prose prose-invert max-w-none">
                            {!! nl2br(e($event->description)) !!}
                        </div>
                    </div>
                    @endif

                    <!-- Ticket Types -->
                    <div class="border-t border-gray-700 pt-6">
                        <div class="flex justify-between items-center mb-4">
                            <h2 class="text-2xl font-semibold text-gray-100">Tickets</h2>
                            @auth
                            @can('update', $event)
                            <a href="{{ route('events.tickets.create', $event) }}" class="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition text-sm">
                                + Add Ticket Type
                            </a>
                            @endcan
                            @endauth
                        </div>

                        @if($event->ticketTypes->isNotEmpty())
                        <div class="space-y-4">
                            @foreach($event->ticketTypes as $ticket)
                            <div class="bg-gray-900 border border-gray-700 rounded-lg p-4">
                                <div class="flex justify-between items-start">
                                    <div class="flex-1">
                                        <h3 class="text-lg font-medium text-gray-200">{{ $ticket->name }}</h3>
                                        @if($ticket->description)
                                        <p class="text-sm text-gray-400 mt-1">{{ $ticket->description }}</p>
                                        @endif
                                        <div class="flex items-center gap-4 mt-2 text-xs text-gray-500">
                                            @if($ticket->quantity_total)
                                            <span>{{ $ticket->quantity_available }} / {{ $ticket->quantity_total }} available</span>
                                            @endif
                                            @if($ticket->sales_start)
                                            <span>Sales start: {{ $ticket->sales_start->format('M d, Y g:i A') }}</span>
                                            @endif
                                            @if($ticket->requires_approval)
                                            <span class="text-yellow-400">Requires Approval</span>
                                            @endif
                                        </div>
                                    </div>
                                    <div class="text-right flex items-center space-x-3">
                                        <div>
                                            @if($ticket->is_free)
                                            <p class="text-xl font-bold text-green-400">FREE</p>
                                            @else
                                            <p class="text-xl font-bold text-gray-200">{{ $ticket->currency }} {{ number_format($ticket->price, 2) }}</p>
                                            @endif
                                        </div>
                                        @auth
                                        @can('update', $event)
                                        <div class="flex space-x-2">
                                            <a href="{{ route('events.tickets.edit', [$event, $ticket]) }}" class="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-gray-200 rounded text-sm transition">
                                                Edit
                                            </a>
                                            <form action="{{ route('events.tickets.destroy', [$event, $ticket]) }}" method="POST" onsubmit="return confirm('Delete this ticket type?')">
                                                @csrf
                                                @method('DELETE')
                                                <button type="submit" class="px-3 py-1 bg-red-900 hover:bg-red-800 text-red-200 rounded text-sm transition">
                                                    Delete
                                                </button>
                                            </form>
                                        </div>
                                        @endcan
                                        @endauth
                                    </div>
                                </div>
                            </div>
                            @endforeach
                        </div>
                        @else
                        <div class="bg-gray-900 border border-gray-700 rounded-lg p-8 text-center">
                            <p class="text-gray-400 mb-4">No ticket types yet</p>
                            @auth
                            @can('update', $event)
                            <a href="{{ route('events.tickets.create', $event) }}" class="inline-block px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition">
                                Add Your First Ticket Type
                            </a>
                            @endcan
                            @endauth
                        </div>
                        @endif
                    </div>

                    <!-- RSVP Button -->
                    @if($event->status === 'published' && !$event->isAtCapacity())
                    <div class="border-t border-gray-700 pt-6 mt-8">
                        <button class="w-full py-4 bg-purple-600 hover:bg-purple-700 text-white text-lg font-semibold rounded-lg transition">
                            Register for This Event
                        </button>
                        <p class="text-center text-sm text-gray-400 mt-2">Registration coming in Phase 2</p>
                    </div>
                    @endif
                </div>
            </div>

            <!-- Back to Events -->
            <div class="mt-8 mb-12 text-center">
                <a href="{{ route('events.index') }}" class="text-purple-400 hover:text-purple-300 transition">
                    ← Back to Events
                </a>
            </div>
        </div>
    </div>
</x-app-layout>
