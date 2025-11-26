<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-white leading-tight">
            Registration Confirmed
        </h2>
    </x-slot>

    <div class="py-12">
        <div class="max-w-2xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-gray-800 overflow-hidden shadow-sm sm:rounded-lg border border-gray-700">
                <div class="p-8 text-center">
                    <!-- Success Icon -->
                    <div class="mb-6">
                        <div class="w-20 h-20 bg-green-900/50 rounded-full flex items-center justify-center mx-auto">
                            <svg class="w-10 h-10 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                            </svg>
                        </div>
                    </div>

                    <h2 class="text-3xl font-bold text-white mb-2">
                        @if($registration->status === 'confirmed')
                            You're Registered!
                        @elseif($registration->status === 'pending')
                            Registration Pending
                        @else
                            Added to Waitlist
                        @endif
                    </h2>

                    <p class="text-gray-300 mb-8">
                        @if($registration->status === 'confirmed')
                            Your registration for <strong>{{ $registration->event->title }}</strong> has been confirmed.
                        @elseif($registration->status === 'pending')
                            Your registration for <strong>{{ $registration->event->title }}</strong> is pending organizer approval.
                        @else
                            You've been added to the waitlist for <strong>{{ $registration->event->title }}</strong>. We'll notify you if a spot opens up.
                        @endif
                    </p>

                    <!-- Event Details -->
                    <div class="bg-gray-900 rounded-lg p-6 mb-8 text-left">
                        <h3 class="text-lg font-semibold text-white mb-4">Event Details</h3>
                        <div class="space-y-3 text-white">
                            <div class="flex items-start">
                                <svg class="w-5 h-5 mr-3 mt-0.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                                </svg>
                                <div>
                                    <p class="font-medium">{{ $registration->event->start_datetime->format('l, F j, Y') }}</p>
                                    <p class="text-sm text-gray-400">{{ $registration->event->start_datetime->format('g:i A') }} - {{ $registration->event->end_datetime->format('g:i A') }}</p>
                                </div>
                            </div>

                            @if($registration->event->location)
                            <div class="flex items-start">
                                <svg class="w-5 h-5 mr-3 mt-0.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                                </svg>
                                <p>{{ $registration->event->location }}</p>
                            </div>
                            @endif

                            <div class="flex items-start">
                                <svg class="w-5 h-5 mr-3 mt-0.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"/>
                                </svg>
                                <p>{{ $registration->ticketType->name }}</p>
                            </div>
                        </div>
                    </div>

                    <!-- Attendee Info -->
                    <div class="bg-gray-900 rounded-lg p-6 mb-8 text-left">
                        <h3 class="text-lg font-semibold text-white mb-4">Your Information</h3>
                        <div class="space-y-2 text-white">
                            <p><span class="text-gray-400">Name:</span> {{ $registration->registration_data['name'] ?? 'N/A' }}</p>
                            <p><span class="text-gray-400">Email:</span> {{ $registration->registration_data['email'] ?? 'N/A' }}</p>
                        </div>
                    </div>

                    <!-- What's Next -->
                    <div class="bg-purple-900/30 border border-purple-700 rounded-lg p-6 mb-8 text-left">
                        <h3 class="text-lg font-semibold text-white mb-3">What's Next?</h3>
                        <ul class="space-y-2 text-white text-sm">
                            <li class="flex items-start">
                                <svg class="w-5 h-5 mr-2 mt-0.5 text-purple-400" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                                </svg>
                                <span>You'll receive a confirmation email shortly</span>
                            </li>
                            <li class="flex items-start">
                                <svg class="w-5 h-5 mr-2 mt-0.5 text-purple-400" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                                </svg>
                                <span>We'll send you a reminder before the event</span>
                            </li>
                            @if($registration->status === 'confirmed')
                            <li class="flex items-start">
                                <svg class="w-5 h-5 mr-2 mt-0.5 text-purple-400" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                                </svg>
                                <span>Your ticket will be ready for check-in at the event</span>
                            </li>
                            @endif
                        </ul>
                    </div>

                    <!-- Actions -->
                    <div class="flex flex-col sm:flex-row gap-4 justify-center">
                        <a href="{{ route('events.show', $registration->event) }}" class="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition">
                            View Event Details
                        </a>
                        <a href="{{ route('events.index') }}" class="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition">
                            Browse More Events
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</x-app-layout>
