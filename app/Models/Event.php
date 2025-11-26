<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Event extends Model
{
    protected $fillable = [
        'organizer_id',
        'community_id',
        'title',
        'slug',
        'description',
        'cover_image_url',
        'location',
        'location_type',
        'start_datetime',
        'end_datetime',
        'timezone',
        'capacity',
        'status',
        'visibility',
    ];

    protected $casts = [
        'start_datetime' => 'datetime',
        'end_datetime' => 'datetime',
    ];

    public function community(): BelongsTo
    {
        return $this->belongsTo(Community::class);
    }

    public function ticketTypes(): HasMany
    {
        return $this->hasMany(TicketType::class);
    }

    public function registrations(): HasMany
    {
        return $this->hasMany(Registration::class);
    }

    public function views(): HasMany
    {
        return $this->hasMany(EventView::class);
    }

    public function getRouteKeyName(): string
    {
        return 'slug';
    }

    public function scopePublished($query)
    {
        return $query->where('status', 'published');
    }

    public function scopeUpcoming($query)
    {
        return $query->where('start_datetime', '>', now());
    }

    public function isAtCapacity(): bool
    {
        if (!$this->capacity) {
            return false;
        }

        return $this->registrations()->where('status', 'confirmed')->count() >= $this->capacity;
    }

    public function availableSpots(): ?int
    {
        if (!$this->capacity) {
            return null;
        }

        $confirmed = $this->registrations()->where('status', 'confirmed')->count();
        return max(0, $this->capacity - $confirmed);
    }
}
