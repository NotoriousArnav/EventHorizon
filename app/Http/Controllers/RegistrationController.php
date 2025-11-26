<?php

namespace App\Http\Controllers;

use App\Http\Requests\RegistrationRequest;
use App\Models\Event;
use App\Models\Registration;
use App\Services\SupabaseService;
use Illuminate\Http\Request;

class RegistrationController extends Controller
{
    public function create(Event $event)
    {
        // Check if event is published and accepting registrations
        if ($event->status !== 'published') {
            abort(404);
        }

        // Get available ticket types
        $ticketTypes = $event->ticketTypes()
            ->where(function($query) {
                $query->whereNull('sales_start')
                    ->orWhere('sales_start', '<=', now());
            })
            ->where(function($query) {
                $query->whereNull('sales_end')
                    ->orWhere('sales_end', '>=', now());
            })
            ->orderBy('sort_order')
            ->get();

        // If no ticket types, create a default free ticket
        if ($ticketTypes->isEmpty()) {
            $ticketTypes = collect([
                $event->ticketTypes()->create([
                    'name' => 'General Admission',
                    'description' => 'Free event registration',
                    'price' => 0,
                    'currency' => 'USD',
                    'is_free' => true,
                    'requires_approval' => false,
                    'sort_order' => 0,
                ])
            ]);
        }

        return view('registrations.create', compact('event', 'ticketTypes'));
    }

    public function store(RegistrationRequest $request, Event $event)
    {
        $data = $request->validated();
        
        // Get user info (if authenticated)
        $userId = null;
        if (session()->has('supabase_access_token')) {
            try {
                $supabase = app(SupabaseService::class);
                $accessToken = session('supabase_access_token');
                $user = $supabase->getUser($accessToken);
                $userId = $user['id'];
            } catch (\Exception $e) {
                // Guest registration
            }
        }

        // Get selected ticket type
        $ticketType = $event->ticketTypes()->findOrFail($data['ticket_type_id']);

        // Check capacity
        if ($ticketType->quantity_total) {
            if ($ticketType->quantity_available <= 0) {
                // Add to waitlist
                $status = 'waitlist';
            } else {
                $status = $ticketType->requires_approval ? 'pending' : 'confirmed';
                
                // Decrement available quantity
                $ticketType->decrement('quantity_available');
            }
        } else {
            // Unlimited capacity
            $status = $ticketType->requires_approval ? 'pending' : 'confirmed';
        }

        // Create registration
        $registration = Registration::create([
            'event_id' => $event->id,
            'user_id' => $userId,
            'ticket_type_id' => $ticketType->id,
            'status' => $status,
            'registration_data' => [
                'name' => $data['name'],
                'email' => $data['email'],
                'custom_answers' => $data['custom_answers'] ?? null,
            ],
        ]);

        return redirect()
            ->route('registrations.confirmation', $registration)
            ->with('success', 'Registration successful!');
    }

    public function confirmation(Registration $registration)
    {
        return view('registrations.confirmation', compact('registration'));
    }
}
