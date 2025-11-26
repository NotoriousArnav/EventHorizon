<?php

namespace App\Http\Controllers;

use App\Http\Requests\ProfileUpdateRequest;
use App\Services\SupabaseService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redirect;
use Illuminate\View\View;

class ProfileController extends Controller
{
    public function edit(Request $request): View
    {
        try {
            $supabase = app(SupabaseService::class);
            $accessToken = session('supabase_access_token');
            $supabaseUser = $supabase->getUser($accessToken);
            
            // Create a user object from Supabase data
            $user = (object) [
                'name' => $supabaseUser['user_metadata']['name'] ?? $supabaseUser['email'] ?? '',
                'email' => $supabaseUser['email'] ?? '',
            ];
        } catch (\Exception $e) {
            return redirect()->route('login')->with('error', 'Your session has expired. Please login again.');
        }

        return view('profile.edit', [
            'user' => $user,
        ]);
    }

    public function update(ProfileUpdateRequest $request): RedirectResponse
    {
        // For now, just return success - Supabase profile updates would need to be implemented
        return Redirect::route('profile.edit')->with('status', 'profile-updated');
    }

    public function destroy(Request $request): RedirectResponse
    {
        // Clear Supabase session
        session()->forget(['supabase_access_token', 'supabase_refresh_token', 'supabase_user']);
        session()->invalidate();
        session()->regenerateToken();

        return Redirect::to('/')->with('status', 'Account logged out.');
    }
}
