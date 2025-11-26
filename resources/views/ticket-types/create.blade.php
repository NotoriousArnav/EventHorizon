<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-200 leading-tight">
            Add Ticket Type to "{{ $event->title }}"
        </h2>
    </x-slot>

    <div class="py-12">
        <div class="max-w-3xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-gray-800 overflow-hidden shadow-sm sm:rounded-lg border border-gray-700">
                <form action="{{ route('events.tickets.store', $event) }}" method="POST" class="p-6 space-y-6">
                    @csrf

                    <!-- Ticket Name -->
                    <div>
                        <label for="name" class="block text-sm font-medium text-gray-200 mb-2">Ticket Name *</label>
                        <input type="text" name="name" id="name" value="{{ old('name') }}" required
                            class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
                            placeholder="General Admission, VIP, Early Bird, etc.">
                        @error('name')
                        <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                        @enderror
                    </div>

                    <!-- Description -->
                    <div>
                        <label for="description" class="block text-sm font-medium text-gray-200 mb-2">Description</label>
                        <textarea name="description" id="description" rows="3"
                            class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
                            placeholder="What's included with this ticket?">{{ old('description') }}</textarea>
                        @error('description')
                        <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                        @enderror
                    </div>

                    <!-- Free Ticket Toggle -->
                    <div>
                        <label class="flex items-center space-x-3 cursor-pointer">
                            <input type="checkbox" name="is_free" id="is_free" value="1" 
                                {{ old('is_free', true) ? 'checked' : '' }}
                                class="w-5 h-5 bg-gray-900 border-gray-700 rounded text-purple-600 focus:ring-2 focus:ring-purple-600"
                                onchange="document.getElementById('price-fields').classList.toggle('hidden')">
                            <span class="text-gray-200 font-medium">This is a free ticket</span>
                        </label>
                    </div>

                    <!-- Price Fields -->
                    <div id="price-fields" class="{{ old('is_free', true) ? 'hidden' : '' }} space-y-4">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label for="price" class="block text-sm font-medium text-gray-200 mb-2">Price *</label>
                                <input type="number" name="price" id="price" value="{{ old('price', 0) }}" min="0" step="0.01" required
                                    class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent">
                                @error('price')
                                <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                                @enderror
                            </div>

                            <div>
                                <label for="currency" class="block text-sm font-medium text-gray-200 mb-2">Currency *</label>
                                <input type="text" name="currency" id="currency" value="{{ old('currency', 'USD') }}" maxlength="3" required
                                    class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
                                    placeholder="USD">
                                @error('currency')
                                <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                                @enderror
                            </div>
                        </div>
                    </div>

                    <!-- Quantity -->
                    <div>
                        <label for="quantity_total" class="block text-sm font-medium text-gray-200 mb-2">Quantity Available</label>
                        <input type="number" name="quantity_total" id="quantity_total" value="{{ old('quantity_total') }}" min="1"
                            class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
                            placeholder="Leave empty for unlimited">
                        <p class="mt-1 text-xs text-gray-400">Total number of tickets available (optional)</p>
                        @error('quantity_total')
                        <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                        @enderror
                    </div>

                    <!-- Sales Period -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label for="sales_start" class="block text-sm font-medium text-gray-200 mb-2">Sales Start</label>
                            <input type="datetime-local" name="sales_start" id="sales_start" value="{{ old('sales_start') }}"
                                class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent">
                            @error('sales_start')
                            <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                            @enderror
                        </div>

                        <div>
                            <label for="sales_end" class="block text-sm font-medium text-gray-200 mb-2">Sales End</label>
                            <input type="datetime-local" name="sales_end" id="sales_end" value="{{ old('sales_end') }}"
                                class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent">
                            @error('sales_end')
                            <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                            @enderror
                        </div>
                    </div>

                    <!-- Requires Approval -->
                    <div>
                        <label class="flex items-center space-x-3 cursor-pointer">
                            <input type="checkbox" name="requires_approval" id="requires_approval" value="1" 
                                {{ old('requires_approval') ? 'checked' : '' }}
                                class="w-5 h-5 bg-gray-900 border-gray-700 rounded text-purple-600 focus:ring-2 focus:ring-purple-600">
                            <span class="text-gray-200">Require manual approval for registrations</span>
                        </label>
                        <p class="mt-1 text-xs text-gray-400 ml-8">Registrations will be pending until you approve them</p>
                    </div>

                    <!-- Sort Order -->
                    <div>
                        <label for="sort_order" class="block text-sm font-medium text-gray-200 mb-2">Display Order</label>
                        <input type="number" name="sort_order" id="sort_order" value="{{ old('sort_order', 0) }}" min="0"
                            class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent">
                        <p class="mt-1 text-xs text-gray-400">Lower numbers appear first</p>
                        @error('sort_order')
                        <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                        @enderror
                    </div>

                    <!-- Submit -->
                    <div class="flex justify-end space-x-3 pt-4">
                        <a href="{{ route('events.show', $event) }}" class="px-6 py-2 bg-gray-700 hover:bg-gray-600 text-gray-200 rounded-lg transition">
                            Cancel
                        </a>
                        <button type="submit" class="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition">
                            Add Ticket Type
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</x-app-layout>
