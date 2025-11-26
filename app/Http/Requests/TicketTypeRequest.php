<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class TicketTypeRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'description' => ['nullable', 'string'],
            'price' => ['required', 'numeric', 'min:0'],
            'currency' => ['required', 'string', 'size:3'],
            'quantity_total' => ['nullable', 'integer', 'min:1'],
            'quantity_available' => ['nullable', 'integer', 'min:0'],
            'sales_start' => ['nullable', 'date'],
            'sales_end' => ['nullable', 'date', 'after:sales_start'],
            'is_free' => ['required', 'boolean'],
            'requires_approval' => ['required', 'boolean'],
            'sort_order' => ['nullable', 'integer', 'min:0'],
        ];
    }

    public function messages(): array
    {
        return [
            'sales_end.after' => 'Sales end date must be after sales start date.',
            'currency.size' => 'Currency must be a 3-letter code (e.g., USD, EUR).',
        ];
    }
}
