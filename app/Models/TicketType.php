<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class TicketType extends Model
{
    protected $fillable = [
        'event_id',
        'name',
        'description',
        'price',
        'currency',
        'quantity_total',
        'quantity_available',
        'sales_start',
        'sales_end',
        'is_free',
        'requires_approval',
        'sort_order',
    ];

    protected $casts = [
        'price' => 'decimal:2',
        'is_free' => 'boolean',
        'requires_approval' => 'boolean',
        'sales_start' => 'datetime',
        'sales_end' => 'datetime',
    ];

    public function event(): BelongsTo
    {
        return $this->belongsTo(Event::class);
    }

    public function registrations(): HasMany
    {
        return $this->hasMany(Registration::class);
    }

    public function isAvailable(): bool
    {
        if ($this->sales_start && now()->lt($this->sales_start)) {
            return false;
        }

        if ($this->sales_end && now()->gt($this->sales_end)) {
            return false;
        }

        if ($this->quantity_available !== null && $this->quantity_available <= 0) {
            return false;
        }

        return true;
    }

    public function isSoldOut(): bool
    {
        return $this->quantity_available !== null && $this->quantity_available <= 0;
    }
}
