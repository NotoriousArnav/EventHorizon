<?php

namespace App\Policies;

use App\Models\Event;
use App\Models\User;
use Illuminate\Auth\Access\Response;

class EventPolicy
{
    public function viewAny(?User $user): bool
    {
        return true;
    }

    public function view(?User $user, Event $event): bool
    {
        if ($event->visibility === 'public' || $event->visibility === 'unlisted') {
            return true;
        }

        if (!$user) {
            return false;
        }

        return $event->organizer_id === $user->id;
    }

    public function create(User $user): bool
    {
        return true;
    }

    public function update(User $user, Event $event): bool
    {
        return $event->organizer_id === $user->id;
    }

    public function delete(User $user, Event $event): bool
    {
        return $event->organizer_id === $user->id;
    }

    public function restore(User $user, Event $event): bool
    {
        return $event->organizer_id === $user->id;
    }

    public function forceDelete(User $user, Event $event): bool
    {
        return $event->organizer_id === $user->id;
    }
}
