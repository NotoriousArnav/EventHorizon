<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use App\Services\SupabaseService;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Session;

class SupabaseAuthController extends Controller
{
    protected $supabase;

    public function __construct(SupabaseService $supabase)
    {
        $this->supabase = $supabase;
    }

    public function showLogin()
    {
        return view('auth.login');
    }

    public function showRegister()
    {
        return view('auth.register');
    }

    public function register(Request $request)
    {
        $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|email',
            'password' => 'required|min:6|confirmed',
        ]);

        try {
            $result = $this->supabase->signUp(
                $request->email,
                $request->password,
                ['name' => $request->name]
            );

            if (isset($result['access_token'])) {
                Session::put('supabase_access_token', $result['access_token']);
                Session::put('supabase_refresh_token', $result['refresh_token']);
                Session::put('supabase_user', $result['user']);

                return redirect()->route('dashboard')->with('success', 'Registration successful!');
            }

            return back()->withErrors(['email' => 'Registration failed. Please try again.']);
        } catch (\Exception $e) {
            return back()->withErrors(['email' => 'An error occurred: ' . $e->getMessage()]);
        }
    }

    public function login(Request $request)
    {
        $request->validate([
            'email' => 'required|email',
            'password' => 'required',
        ]);

        try {
            $result = $this->supabase->signIn(
                $request->email,
                $request->password
            );

            if (isset($result['access_token'])) {
                Session::put('supabase_access_token', $result['access_token']);
                Session::put('supabase_refresh_token', $result['refresh_token']);
                Session::put('supabase_user', $result['user']);

                return redirect()->intended('dashboard')->with('success', 'Login successful!');
            }

            return back()->withErrors(['email' => 'Invalid credentials.']);
        } catch (\Exception $e) {
            return back()->withErrors(['email' => 'An error occurred: ' . $e->getMessage()]);
        }
    }

    public function logout(Request $request)
    {
        $accessToken = Session::get('supabase_access_token');

        if ($accessToken) {
            try {
                $this->supabase->signOut($accessToken);
            } catch (\Exception $e) {
                // Log but don't fail logout
            }
        }

        Session::forget('supabase_access_token');
        Session::forget('supabase_refresh_token');
        Session::forget('supabase_user');

        return redirect('/')->with('success', 'Logged out successfully!');
    }

    public function oauthRedirect($provider)
    {
        $redirectTo = url('/auth/callback');
        $url = $this->supabase->getOAuthUrl($provider, $redirectTo);

        return redirect($url);
    }

    public function oauthCallback(Request $request)
    {
        // Since Supabase uses hash-based tokens (#access_token), 
        // we need JavaScript to extract them
        // This route just shows the handler page
        return view('auth.oauth-handler');
    }

    public function processOAuthTokens(Request $request)
    {
        $request->validate([
            'access_token' => 'required|string',
            'refresh_token' => 'required|string',
        ]);

        try {
            $accessToken = $request->input('access_token');
            $refreshToken = $request->input('refresh_token');

            // Fetch user info from Supabase
            $user = $this->supabase->getUser($accessToken);

            // Store in session
            Session::put('supabase_access_token', $accessToken);
            Session::put('supabase_refresh_token', $refreshToken);
            Session::put('supabase_user', $user);

            \Log::info('OAuth tokens processed successfully', [
                'user_email' => $user['email'] ?? 'unknown'
            ]);

            return response()->json([
                'success' => true,
                'redirect' => route('dashboard')
            ]);
        } catch (\Exception $e) {
            \Log::error('OAuth token processing failed', [
                'error' => $e->getMessage()
            ]);

            return response()->json([
                'success' => false,
                'message' => $e->getMessage()
            ], 500);
        }
    }

    public function walletLogin(Request $request)
    {
        $request->validate([
            'address' => 'required|string',
        ]);

        $address = strtolower($request->address);

        try {
            // Try to authenticate with wallet address using Supabase
            // For now, we'll create a session directly with the wallet address
            // In production, you'd verify wallet ownership via signature
            
            $email = $address . '@wallet.eventhorizon';
            $password = hash('sha256', $address . config('app.key'));

            try {
                // Try to sign in first
                $result = $this->supabase->signIn($email, $password);
            } catch (\Exception $e) {
                // If user doesn't exist, create account
                $result = $this->supabase->signUp(
                    $email,
                    $password,
                    ['wallet_address' => $address]
                );
            }

            if (isset($result['access_token'])) {
                Session::put('supabase_access_token', $result['access_token']);
                Session::put('supabase_refresh_token', $result['refresh_token']);
                Session::put('supabase_user', $result['user']);
                Session::put('wallet_address', $address);

                return response()->json(['success' => true, 'redirect' => '/dashboard']);
            }

            return response()->json(['success' => false, 'message' => 'Authentication failed']);
        } catch (\Exception $e) {
            return response()->json(['success' => false, 'message' => $e->getMessage()], 500);
        }
    }

    public function walletRegister(Request $request)
    {
        // Same as wallet login since we auto-create accounts
        return $this->walletLogin($request);
    }
}

