<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Support\Str;

class Registration extends Model
{
    protected $fillable = [
        'event_id',
        'user_id',
        'ticket_type_id',
        'attendee_name',
        'attendee_email',
        'status',
        'payment_status',
        'checked_in_at',
        'qr_code',
        'registration_data',
    ];

    protected $casts = [
        'checked_in_at' => 'datetime',
        'registration_data' => 'array',
    ];

    protected static function boot()
    {
        parent::boot();

        static::creating(function ($registration) {
            if (!$registration->qr_code) {
                $registration->qr_code = Str::uuid()->toString();
            }
        });
    }

    public function event(): BelongsTo
    {
        return $this->belongsTo(Event::class);
    }

    public function ticketType(): BelongsTo
    {
        return $this->belongsTo(TicketType::class);
    }

    public function isCheckedIn(): bool
    {
        return $this->checked_in_at !== null;
    }

    public function checkIn(): void
    {
        $this->update(['checked_in_at' => now()]);
    }

    public function scopeConfirmed($query)
    {
        return $query->where('status', 'confirmed');
    }

    public function scopeWaitlist($query)
    {
        return $query->where('status', 'waitlist');
    }
}
