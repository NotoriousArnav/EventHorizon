<?php

namespace App\Policies;

use App\Models\TicketType;
use App\Models\Event;
use App\Models\User;
use App\Services\SupabaseService;

class TicketTypePolicy
{
    public function viewAny(?User $user): bool
    {
        return true;
    }

    public function view(?User $user, TicketType $ticketType): bool
    {
        return true;
    }

    public function create(User $user): bool
    {
        return true;
    }

    public function update(User $user, TicketType $ticketType): bool
    {
        $supabase = app(SupabaseService::class);
        $currentUser = $supabase->getUser();
        
        return $ticketType->event->organizer_id === $currentUser['id'];
    }

    public function delete(User $user, TicketType $ticketType): bool
    {
        $supabase = app(SupabaseService::class);
        $currentUser = $supabase->getUser();
        
        return $ticketType->event->organizer_id === $currentUser['id'];
    }

    public function restore(User $user, TicketType $ticketType): bool
    {
        $supabase = app(SupabaseService::class);
        $currentUser = $supabase->getUser();
        
        return $ticketType->event->organizer_id === $currentUser['id'];
    }

    public function forceDelete(User $user, TicketType $ticketType): bool
    {
        $supabase = app(SupabaseService::class);
        $currentUser = $supabase->getUser();
        
        return $ticketType->event->organizer_id === $currentUser['id'];
    }
}
