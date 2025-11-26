<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-200 leading-tight">
            Create New Event
        </h2>
    </x-slot>

    <div class="py-12">
        <div class="max-w-3xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-gray-800 overflow-hidden shadow-sm sm:rounded-lg border border-gray-700">
                <form action="{{ route('events.store') }}" method="POST" class="p-6 space-y-6">
                    @csrf

                    <!-- Title -->
                    <div>
                        <label for="title" class="block text-sm font-medium text-gray-200 mb-2">Event Title *</label>
                        <input type="text" name="title" id="title" value="{{ old('title') }}" required
                            class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
                            placeholder="Amazing Tech Conference 2024">
                        @error('title')
                        <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                        @enderror
                    </div>

                    <!-- Slug -->
                    <div>
                        <label for="slug" class="block text-sm font-medium text-gray-200 mb-2">Event Slug *</label>
                        <input type="text" name="slug" id="slug" value="{{ old('slug') }}" required
                            class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
                            placeholder="amazing-tech-conference-2024">
                        <p class="mt-1 text-xs text-gray-400">URL-friendly version of the title</p>
                        @error('slug')
                        <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                        @enderror
                    </div>

                    <!-- Description -->
                    <div>
                        <label for="description" class="block text-sm font-medium text-gray-200 mb-2">Description</label>
                        <textarea name="description" id="description" rows="6"
                            class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
                            placeholder="Tell attendees what your event is about...">{{ old('description') }}</textarea>
                        @error('description')
                        <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                        @enderror
                    </div>

                    <!-- Cover Image URL -->
                    <div>
                        <label for="cover_image_url" class="block text-sm font-medium text-gray-200 mb-2">Cover Image URL</label>
                        <input type="url" name="cover_image_url" id="cover_image_url" value="{{ old('cover_image_url') }}"
                            class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
                            placeholder="https://example.com/image.jpg">
                        @error('cover_image_url')
                        <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                        @enderror
                    </div>

                    <!-- Location Type -->
                    <div>
                        <label for="location_type" class="block text-sm font-medium text-gray-200 mb-2">Location Type *</label>
                        <select name="location_type" id="location_type" required
                            class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent">
                            <option value="physical" {{ old('location_type') == 'physical' ? 'selected' : '' }}>Physical Location</option>
                            <option value="online" {{ old('location_type') == 'online' ? 'selected' : '' }}>Online Event</option>
                            <option value="hybrid" {{ old('location_type') == 'hybrid' ? 'selected' : '' }}>Hybrid</option>
                        </select>
                        @error('location_type')
                        <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                        @enderror
                    </div>

                    <!-- Location -->
                    <div>
                        <label for="location" class="block text-sm font-medium text-gray-200 mb-2">Location/Venue</label>
                        <input type="text" name="location" id="location" value="{{ old('location') }}"
                            class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
                            placeholder="123 Main St, San Francisco, CA or Zoom link">
                        @error('location')
                        <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                        @enderror
                    </div>

                    <!-- Date & Time -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label for="start_datetime" class="block text-sm font-medium text-gray-200 mb-2">Start Date & Time *</label>
                            <input type="datetime-local" name="start_datetime" id="start_datetime" value="{{ old('start_datetime') }}" required
                                class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent">
                            @error('start_datetime')
                            <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                            @enderror
                        </div>

                        <div>
                            <label for="end_datetime" class="block text-sm font-medium text-gray-200 mb-2">End Date & Time *</label>
                            <input type="datetime-local" name="end_datetime" id="end_datetime" value="{{ old('end_datetime') }}" required
                                class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent">
                            @error('end_datetime')
                            <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                            @enderror
                        </div>
                    </div>

                    <!-- Timezone -->
                    <div>
                        <label for="timezone" class="block text-sm font-medium text-gray-200 mb-2">Timezone *</label>
                        <input type="text" name="timezone" id="timezone" value="{{ old('timezone', 'UTC') }}" required
                            class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
                            placeholder="UTC, America/New_York, etc.">
                        @error('timezone')
                        <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                        @enderror
                    </div>

                    <!-- Capacity -->
                    <div>
                        <label for="capacity" class="block text-sm font-medium text-gray-200 mb-2">Capacity</label>
                        <input type="number" name="capacity" id="capacity" value="{{ old('capacity') }}" min="1"
                            class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
                            placeholder="Leave empty for unlimited">
                        <p class="mt-1 text-xs text-gray-400">Maximum number of attendees (optional)</p>
                        @error('capacity')
                        <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                        @enderror
                    </div>

                    <!-- Status & Visibility -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label for="status" class="block text-sm font-medium text-gray-200 mb-2">Status *</label>
                            <select name="status" id="status" required
                                class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent">
                                <option value="draft" {{ old('status') == 'draft' ? 'selected' : '' }}>Draft</option>
                                <option value="published" {{ old('status') == 'published' ? 'selected' : '' }}>Published</option>
                            </select>
                            @error('status')
                            <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                            @enderror
                        </div>

                        <div>
                            <label for="visibility" class="block text-sm font-medium text-gray-200 mb-2">Visibility *</label>
                            <select name="visibility" id="visibility" required
                                class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent">
                                <option value="public" {{ old('visibility') == 'public' ? 'selected' : '' }}>Public</option>
                                <option value="unlisted" {{ old('visibility') == 'unlisted' ? 'selected' : '' }}>Unlisted</option>
                                <option value="private" {{ old('visibility') == 'private' ? 'selected' : '' }}>Private</option>
                            </select>
                            @error('visibility')
                            <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                            @enderror
                        </div>
                    </div>

                    <!-- Community -->
                    @if($communities->isNotEmpty())
                    <div>
                        <label for="community_id" class="block text-sm font-medium text-gray-200 mb-2">Community (Optional)</label>
                        <select name="community_id" id="community_id"
                            class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-200 focus:ring-2 focus:ring-purple-600 focus:border-transparent">
                            <option value="">No Community</option>
                            @foreach($communities as $community)
                            <option value="{{ $community->id }}" {{ old('community_id') == $community->id ? 'selected' : '' }}>
                                {{ $community->name }}
                            </option>
                            @endforeach
                        </select>
                        @error('community_id')
                        <p class="mt-1 text-sm text-red-400">{{ $message }}</p>
                        @enderror
                    </div>
                    @endif

                    <!-- Submit -->
                    <div class="flex justify-end space-x-3 pt-4">
                        <a href="{{ route('events.index') }}" class="px-6 py-2 bg-gray-700 hover:bg-gray-600 text-gray-200 rounded-lg transition">
                            Cancel
                        </a>
                        <button type="submit" class="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition">
                            Create Event
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</x-app-layout>
