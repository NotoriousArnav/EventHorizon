<?php

namespace App\Http\Controllers;

use App\Http\Requests\EventRequest;
use App\Models\Event;
use App\Models\Community;
use App\Services\SupabaseService;
use Illuminate\Http\Request;
use Illuminate\Support\Str;
use Illuminate\Foundation\Auth\Access\AuthorizesRequests;

class EventController extends Controller
{
    use AuthorizesRequests;

    public function index()
    {
        $events = Event::published()
            ->where('visibility', 'public')
            ->upcoming()
            ->with(['community', 'ticketTypes'])
            ->orderBy('start_datetime')
            ->paginate(12);

        return view('events.index', compact('events'));
    }

    public function create()
    {

        $supabase = app(SupabaseService::class);
        $accessToken = session('supabase_access_token');
        $user = $supabase->getUser($accessToken);
        
        $communities = Community::where('user_id', $user['id'])->get();

        return view('events.create', compact('communities'));
    }

    public function store(EventRequest $request)
    {

        $supabase = app(SupabaseService::class);
        $accessToken = session('supabase_access_token');
        $user = $supabase->getUser($accessToken);

        $data = $request->validated();
        $data['organizer_id'] = $user['id'];

        if (empty($data['slug'])) {
            $data['slug'] = Str::slug($data['title']);
        }

        $event = Event::create($data);

        return redirect()
            ->route('events.show', $event)
            ->with('success', 'Event created successfully!');
    }

    public function show(Event $event)
    {

        $event->load(['community', 'ticketTypes', 'registrations']);

        $supabase = app(SupabaseService::class);
        $accessToken = session('supabase_access_token');
        $user = $supabase->getUser($accessToken);

        if ($user) {
            $event->views()->create([
                'user_id' => $user['id'],
                'viewed_at' => now(),
                'ip_address' => request()->ip(),
                'user_agent' => request()->userAgent(),
            ]);
        }

        return view('events.show', compact('event'));
    }

    public function edit(Event $event)
    {
        $supabase = app(SupabaseService::class);
        $accessToken = session('supabase_access_token');
        $user = $supabase->getUser($accessToken);
        
        // Check if user is the organizer
        if ($event->organizer_id !== $user['id']) {
            abort(403, 'Unauthorized');
        }
        
        $communities = Community::where('user_id', $user['id'])->get();

        return view('events.edit', compact('event', 'communities'));
    }

    public function update(EventRequest $request, Event $event)
    {
        $supabase = app(SupabaseService::class);
        $accessToken = session('supabase_access_token');
        $user = $supabase->getUser($accessToken);
        
        // Check if user is the organizer
        if ($event->organizer_id !== $user['id']) {
            abort(403, 'Unauthorized');
        }

        $event->update($request->validated());

        return redirect()
            ->route('events.show', $event)
            ->with('success', 'Event updated successfully!');
    }

    public function destroy(Event $event)
    {
        $supabase = app(SupabaseService::class);
        $accessToken = session('supabase_access_token');
        $user = $supabase->getUser($accessToken);
        
        // Check if user is the organizer
        if ($event->organizer_id !== $user['id']) {
            abort(403, 'Unauthorized');
        }

        $event->delete();

        return redirect()
            ->route('events.index')
            ->with('success', 'Event deleted successfully!');
    }
}
