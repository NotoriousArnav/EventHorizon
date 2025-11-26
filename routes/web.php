<?php

use App\Http\Controllers\ProfileController;
use App\Http\Controllers\Auth\SupabaseAuthController;
use App\Http\Controllers\EventController;
use App\Http\Controllers\TicketTypeController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('landing');
});

// Supabase Authentication Routes
Route::get('/login', [SupabaseAuthController::class, 'showLogin'])->name('login');
Route::post('/login', [SupabaseAuthController::class, 'login'])->name('supabase.login');
Route::get('/register', [SupabaseAuthController::class, 'showRegister'])->name('register');
Route::post('/register', [SupabaseAuthController::class, 'register'])->name('supabase.register');
Route::post('/logout', [SupabaseAuthController::class, 'logout'])->name('logout');
Route::get('/auth/oauth/{provider}', [SupabaseAuthController::class, 'oauthRedirect'])->name('supabase.oauth');
Route::get('/auth/callback', [SupabaseAuthController::class, 'oauthCallback'])->name('supabase.callback');
Route::post('/auth/oauth/process', [SupabaseAuthController::class, 'processOAuthTokens'])->name('oauth.process');

// Password reset routes (still needed for fallback)
Route::get('/forgot-password', function () {
    return view('auth.forgot-password');
})->name('password.request');

// Web3 Wallet Authentication Routes
Route::post('/auth/wallet/login', [SupabaseAuthController::class, 'walletLogin'])->name('wallet.login');
Route::post('/auth/wallet/register', [SupabaseAuthController::class, 'walletRegister'])->name('wallet.register');

// Debug callback route
Route::get('/auth/callback/debug', function() {
    return view('auth.callback-debug');
})->name('callback.debug');

Route::get('/dashboard', function () {
    // Check if user is authenticated via Supabase
    if (!session()->has('supabase_access_token')) {
        return redirect()->route('login');
    }
    return view('dashboard');
})->name('dashboard');

// Event Management Routes
Route::resource('events', EventController::class);

// Ticket Type Management Routes (nested under events)
Route::prefix('events/{event}/tickets')->name('events.tickets.')->group(function () {
    Route::get('/create', [TicketTypeController::class, 'create'])->name('create');
    Route::post('/', [TicketTypeController::class, 'store'])->name('store');
    Route::get('/{ticketType}/edit', [TicketTypeController::class, 'edit'])->name('edit');
    Route::put('/{ticketType}', [TicketTypeController::class, 'update'])->name('update');
    Route::delete('/{ticketType}', [TicketTypeController::class, 'destroy'])->name('destroy');
});

Route::middleware('auth')->group(function () {
    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');
});
