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
                            <h1 class="text-4xl font-bold text-white mb-2">{{ $event->title }}</h1>
                            
                            @if($event->community)
                            <p class="text-purple-400">
                                by {{ $event->community->name }}
                            </p>
                            @endif
                        </div>

                        @auth
                        @can('update', $event)
                        <div class="flex space-x-2">
                            <a href="{{ route('events.edit', $event) }}" class="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition">
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
                                <p class="text-sm text-gray-300">Date & Time</p>
                                <p class="text-white font-medium">{{ $event->start_datetime->format('l, F j, Y') }}</p>
                                <p class="text-white">{{ $event->start_datetime->format('g:i A') }} - {{ $event->end_datetime->format('g:i A') }}</p>
                                <p class="text-xs text-gray-400">{{ $event->timezone }}</p>
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
                                <p class="text-sm text-gray-300">Location</p>
                                <p class="text-white font-medium capitalize">{{ $event->location_type }}</p>
                                @if($event->location)
                                <p class="text-white">{{ $event->location }}</p>
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
                                <p class="text-sm text-gray-300">Capacity</p>
                                <p class="text-white font-medium">
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
                                <p class="text-sm text-gray-300">Status</p>
                                <span class="inline-block px-3 py-1 text-sm font-medium rounded-full
                                    @if($event->status === 'published') bg-green-900/50 text-green-300
                                    @elseif($event->status === 'draft') bg-yellow-900/50 text-yellow-300
                                    @elseif($event->status === 'cancelled') bg-red-900/50 text-red-300
                                    @else bg-gray-700 text-white
                                    @endif">
                                    {{ ucfirst($event->status) }}
                                </span>
                            </div>
                        </div>
                    </div>

                    <!-- Description -->
                    @if($event->description)
                    <div class="border-t border-gray-700 pt-6 mb-8">
                        <h2 class="text-2xl font-semibold text-white mb-4">About This Event</h2>
                        <div class="text-white prose prose-invert max-w-none">
                            {!! nl2br(e($event->description)) !!}
                        </div>
                    </div>
                    @endif

                    <!-- Share Buttons -->
                    <div class="border-t border-gray-700 pt-6 mb-8">
                        <h2 class="text-2xl font-semibold text-white mb-4">Share This Event</h2>
                        <div class="flex flex-wrap gap-3">
                            <!-- Twitter -->
                            <a href="https://twitter.com/intent/tweet?text={{ urlencode($event->title) }}&url={{ urlencode(route('events.show', $event)) }}" 
                                target="_blank" 
                                class="flex items-center space-x-2 px-4 py-2 bg-[#1DA1F2] hover:bg-[#1a8cd8] text-white rounded-lg transition">
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                                </svg>
                                <span>Twitter</span>
                            </a>

                            <!-- Facebook -->
                            <a href="https://www.facebook.com/sharer/sharer.php?u={{ urlencode(route('events.show', $event)) }}" 
                                target="_blank" 
                                class="flex items-center space-x-2 px-4 py-2 bg-[#1877F2] hover:bg-[#166fe5] text-white rounded-lg transition">
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                                </svg>
                                <span>Facebook</span>
                            </a>

                            <!-- LinkedIn -->
                            <a href="https://www.linkedin.com/shareArticle?mini=true&url={{ urlencode(route('events.show', $event)) }}&title={{ urlencode($event->title) }}" 
                                target="_blank" 
                                class="flex items-center space-x-2 px-4 py-2 bg-[#0A66C2] hover:bg-[#095196] text-white rounded-lg transition">
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                                </svg>
                                <span>LinkedIn</span>
                            </a>

                            <!-- WhatsApp -->
                            <a href="https://wa.me/?text={{ urlencode($event->title . ' - ' . route('events.show', $event)) }}" 
                                target="_blank" 
                                class="flex items-center space-x-2 px-4 py-2 bg-[#25D366] hover:bg-[#20bd5a] text-white rounded-lg transition">
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                                </svg>
                                <span>WhatsApp</span>
                            </a>

                            <!-- Copy Link -->
                            <button 
                                onclick="copyEventLink()" 
                                id="copy-link-btn"
                                class="flex items-center space-x-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                                </svg>
                                <span id="copy-link-text">Copy Link</span>
                            </button>
                        </div>
                    </div>

                    <script>
                        function copyEventLink() {
                            const url = '{{ route('events.show', $event) }}';
                            navigator.clipboard.writeText(url).then(() => {
                                const btn = document.getElementById('copy-link-btn');
                                const text = document.getElementById('copy-link-text');
                                const originalText = text.textContent;
                                
                                text.textContent = 'Copied!';
                                btn.classList.remove('bg-gray-700', 'hover:bg-gray-600');
                                btn.classList.add('bg-green-700');
                                
                                setTimeout(() => {
                                    text.textContent = originalText;
                                    btn.classList.remove('bg-green-700');
                                    btn.classList.add('bg-gray-700', 'hover:bg-gray-600');
                                }, 2000);
                            }).catch(err => {
                                alert('Failed to copy link');
                            });
                        }
                    </script>

                    <!-- Ticket Types -->
                    <div class="border-t border-gray-700 pt-6">
                        <div class="flex justify-between items-center mb-4">
                            <h2 class="text-2xl font-semibold text-white">Tickets</h2>
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
                                        <h3 class="text-lg font-medium text-white">{{ $ticket->name }}</h3>
                                        @if($ticket->description)
                                        <p class="text-sm text-gray-300 mt-1">{{ $ticket->description }}</p>
                                        @endif
                                        <div class="flex items-center gap-4 mt-2 text-xs text-gray-400">
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
                                            <p class="text-xl font-bold text-white">{{ $ticket->currency }} {{ number_format($ticket->price, 2) }}</p>
                                            @endif
                                        </div>
                                        @auth
                                        @can('update', $event)
                                        <div class="flex space-x-2">
                                            <a href="{{ route('events.tickets.edit', [$event, $ticket]) }}" class="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-white rounded text-sm transition">
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
                            <p class="text-gray-300 mb-4">No ticket types yet</p>
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
                        <p class="text-center text-sm text-gray-300 mt-2">Registration coming in Phase 2</p>
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
