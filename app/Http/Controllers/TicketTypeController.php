<?php

namespace App\Http\Controllers;

use App\Http\Requests\TicketTypeRequest;
use App\Models\Event;
use App\Models\TicketType;
use Illuminate\Http\Request;
use Illuminate\Foundation\Auth\Access\AuthorizesRequests;

class TicketTypeController extends Controller
{
    use AuthorizesRequests;

    public function create(Event $event)
    {
        $supabase = app(SupabaseService::class);
        $accessToken = session('supabase_access_token');
        $user = $supabase->getUser($accessToken);
        
        // Check if user is the organizer
        if ($event->organizer_id !== $user['id']) {
            abort(403, 'Unauthorized');
        }

        return view('ticket-types.create', compact('event'));
    }

    public function store(TicketTypeRequest $request, Event $event)
    {
        $supabase = app(SupabaseService::class);
        $accessToken = session('supabase_access_token');
        $user = $supabase->getUser($accessToken);
        
        // Check if user is the organizer
        if ($event->organizer_id !== $user['id']) {
            abort(403, 'Unauthorized');
        }

        $data = $request->validated();
        
        // Set quantity_available to quantity_total if not set
        if (isset($data['quantity_total']) && !isset($data['quantity_available'])) {
            $data['quantity_available'] = $data['quantity_total'];
        }

        $event->ticketTypes()->create($data);

        return redirect()
            ->route('events.show', $event)
            ->with('success', 'Ticket type created successfully!');
    }

    public function edit(Event $event, TicketType $ticketType)
    {
        $supabase = app(SupabaseService::class);
        $accessToken = session('supabase_access_token');
        $user = $supabase->getUser($accessToken);
        
        // Check if user is the organizer
        if ($event->organizer_id !== $user['id']) {
            abort(403, 'Unauthorized');
        }

        return view('ticket-types.edit', compact('event', 'ticketType'));
    }

    public function update(TicketTypeRequest $request, Event $event, TicketType $ticketType)
    {
        $supabase = app(SupabaseService::class);
        $accessToken = session('supabase_access_token');
        $user = $supabase->getUser($accessToken);
        
        // Check if user is the organizer
        if ($event->organizer_id !== $user['id']) {
            abort(403, 'Unauthorized');
        }

        $ticketType->update($request->validated());

        return redirect()
            ->route('events.show', $event)
            ->with('success', 'Ticket type updated successfully!');
    }

    public function destroy(Event $event, TicketType $ticketType)
    {
        $supabase = app(SupabaseService::class);
        $accessToken = session('supabase_access_token');
        $user = $supabase->getUser($accessToken);
        
        // Check if user is the organizer
        if ($event->organizer_id !== $user['id']) {
            abort(403, 'Unauthorized');
        }

        $ticketType->delete();

        return redirect()
            ->route('events.show', $event)
            ->with('success', 'Ticket type deleted successfully!');
    }
}
