<?php

namespace App\Http\Controllers;

use App\Models\Event;
use App\Models\Registration;
use App\Services\SupabaseService;
use Illuminate\Http\Request;

class DashboardController extends Controller
{
    public function index()
    {
        $supabase = app(SupabaseService::class);
        $user = $supabase->getUser();

        // Get organizer's events
        $events = Event::where('organizer_id', $user['id'])
            ->with(['ticketTypes', 'registrations'])
            ->orderBy('start_datetime', 'desc')
            ->get();

        // Calculate stats
        $totalEvents = $events->count();
        $upcomingEvents = $events->filter(fn($e) => $e->start_datetime->isFuture())->count();
        $totalRegistrations = $events->sum(fn($e) => $e->registrations()->where('status', 'confirmed')->count());
        
        // Recent events (last 5)
        $recentEvents = $events->take(5);

        return view('dashboard', compact('events', 'totalEvents', 'upcomingEvents', 'totalRegistrations', 'recentEvents'));
    }
}
