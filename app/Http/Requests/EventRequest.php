<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class EventRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        $eventId = $this->route('event')?->id;

        $uniqueRule = $eventId 
            ? 'unique:events,slug,' . $eventId
            : 'unique:events,slug';

        return [
            'title' => ['required', 'string', 'max:255'],
            'slug' => ['required', 'string', 'max:255', 'alpha_dash', $uniqueRule],
            'description' => ['nullable', 'string'],
            'cover_image_url' => ['nullable', 'url'],
            'location' => ['nullable', 'string', 'max:255'],
            'location_type' => ['required', 'in:online,physical,hybrid'],
            'start_datetime' => ['required', 'date', 'after:now'],
            'end_datetime' => ['required', 'date', 'after:start_datetime'],
            'timezone' => ['required', 'string', 'timezone'],
            'capacity' => ['nullable', 'integer', 'min:1'],
            'status' => ['required', 'in:draft,published,cancelled,ended'],
            'visibility' => ['required', 'in:public,unlisted,private'],
            'community_id' => ['nullable', 'exists:communities,id'],
        ];
    }

    public function messages(): array
    {
        return [
            'start_datetime.after' => 'Event must start in the future.',
            'end_datetime.after' => 'Event must end after it starts.',
            'slug.alpha_dash' => 'Slug can only contain letters, numbers, dashes and underscores.',
        ];
    }
}
