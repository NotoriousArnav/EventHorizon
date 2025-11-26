<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class RegistrationRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'ticket_type_id' => ['required', 'exists:ticket_types,id'],
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'email', 'max:255'],
            'custom_answers' => ['nullable', 'array'],
        ];
    }

    public function messages(): array
    {
        return [
            'ticket_type_id.required' => 'Please select a ticket type.',
            'ticket_type_id.exists' => 'Invalid ticket type selected.',
        ];
    }
}
