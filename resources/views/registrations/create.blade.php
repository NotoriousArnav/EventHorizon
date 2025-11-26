<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-white leading-tight">
            Register for {{ $event->title }}
        </h2>
    </x-slot>

    <div class="py-12">
        <div class="max-w-3xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-gray-800 overflow-hidden shadow-sm sm:rounded-lg border border-gray-700">
                <div class="p-6">
                    <!-- Event Info -->
                    <div class="mb-8">
                        <h3 class="text-2xl font-bold text-white mb-2">{{ $event->title }}</h3>
                        <div class="flex items-center text-white text-sm space-x-4">
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
                                </svg>
                                {{ $event->location }}
                            </span>
                            @endif
                        </div>
                    </div>

                    <form action="{{ route('registrations.store', $event) }}" method="POST" class="space-y-6">
                        @csrf

                        <!-- Ticket Selection -->
                        <div>
                            <label class="block text-sm font-medium text-white mb-3">Select Ticket Type *</label>
                            <div class="space-y-3">
                                @foreach($ticketTypes as $ticketType)
                                <label class="block cursor-pointer">
                                    <input type="radio" name="ticket_type_id" value="{{ $ticketType->id }}" required
                                        class="peer sr-only" />
                                    <div class="p-4 bg-gray-900 border-2 border-gray-700 rounded-lg peer-checked:border-purple-500 peer-checked:bg-gray-800 hover:border-gray-600 transition">
                                        <div class="flex justify-between items-start">
                                            <div class="flex-1">
                                                <h4 class="font-semibold text-white">{{ $ticketType->name }}</h4>
                                                @if($ticketType->description)
                                                <p class="text-sm text-gray-300 mt-1">{{ $ticketType->description }}</p>
                                                @endif
                                                @if($ticketType->quantity_total)
                                                <p class="text-xs text-gray-400 mt-2">
                                                    @if($ticketType->quantity_available > 0)
                                                        {{ $ticketType->quantity_available }} / {{ $ticketType->quantity_total }} available
                                                    @else
                                                        <span class="text-yellow-400">Waitlist Available</span>
                                                    @endif
                                                </p>
                                                @endif
                                            </div>
                                            <div class="text-right ml-4">
                                                @if($ticketType->is_free)
                                                <span class="text-xl font-bold text-green-400">FREE</span>
                                                @else
                                                <span class="text-xl font-bold text-white">{{ $ticketType->currency }} {{ number_format($ticketType->price, 2) }}</span>
                                                @endif
                                            </div>
                                        </div>
                                    </div>
                                </label>
                                @endforeach
                            </div>
                            @error('ticket_type_id')
                            <p class="mt-2 text-sm text-red-400">{{ $message }}</p>
                            @enderror
                        </div>

                        <!-- Attendee Information -->
                        <div class="border-t border-gray-700 pt-6">
                            <h4 class="text-lg font-semibold text-white mb-4">Your Information</h4>

                            <!-- Name -->
                            <div class="mb-4">
                                <label for="name" class="block text-sm font-medium text-white mb-2">Full Name *</label>
                                <input type="text" name="name" id="name" value="{{ old('name', session('supabase_user.user_metadata.name') ?? '') }}" required
                                    class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-purple-600 focus:border-transparent">
                                @error('name')
                                <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                                @enderror
                            </div>

                            <!-- Email -->
                            <div class="mb-4">
                                <label for="email" class="block text-sm font-medium text-white mb-2">Email Address *</label>
                                <input type="email" name="email" id="email" value="{{ old('email', session('supabase_user.email') ?? '') }}" required
                                    class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-purple-600 focus:border-transparent">
                                @error('email')
                                <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                                @enderror
                            </div>
                        </div>

                        <!-- Submit -->
                        <div class="flex justify-between items-center pt-6 border-t border-gray-700">
                            <a href="{{ route('events.show', $event) }}" class="text-gray-300 hover:text-white transition">
                                ← Back to Event
                            </a>
                            <button type="submit" class="px-8 py-3 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded-lg transition">
                                Complete Registration
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</x-app-layout>
