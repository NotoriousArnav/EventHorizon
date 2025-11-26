<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class EventView extends Model
{
    protected $fillable = [
        'event_id',
        'user_id',
        'viewed_at',
        'ip_address',
        'user_agent',
    ];

    protected $casts = [
        'viewed_at' => 'datetime',
    ];

    public $timestamps = true;

    public function event(): BelongsTo
    {
        return $this->belongsTo(Event::class);
    }
}
