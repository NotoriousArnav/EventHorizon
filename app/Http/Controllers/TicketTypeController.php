<?php

namespace App\Http\Controllers;

use App\Http\Requests\TicketTypeRequest;
use App\Models\Event;
use App\Models\TicketType;
use Illuminate\Http\Request;

class TicketTypeController extends Controller
{
    public function create(Event $event)
    {
        $this->authorize('update', $event);

        return view('ticket-types.create', compact('event'));
    }

    public function store(TicketTypeRequest $request, Event $event)
    {
        $this->authorize('update', $event);

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
        $this->authorize('update', $ticketType);

        return view('ticket-types.edit', compact('event', 'ticketType'));
    }

    public function update(TicketTypeRequest $request, Event $event, TicketType $ticketType)
    {
        $this->authorize('update', $ticketType);

        $ticketType->update($request->validated());

        return redirect()
            ->route('events.show', $event)
            ->with('success', 'Ticket type updated successfully!');
    }

    public function destroy(Event $event, TicketType $ticketType)
    {
        $this->authorize('delete', $ticketType);

        $ticketType->delete();

        return redirect()
            ->route('events.show', $event)
            ->with('success', 'Ticket type deleted successfully!');
    }
}
