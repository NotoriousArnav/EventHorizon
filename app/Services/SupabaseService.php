<?php

namespace App\Services;

use GuzzleHttp\Client;
use Illuminate\Support\Facades\Log;

class SupabaseService
{
    protected $client;
    protected $url;
    protected $key;
    protected $jwtSecret;

    public function __construct()
    {
        $this->url = config('services.supabase.url');
        $this->key = config('services.supabase.key');
        $this->jwtSecret = config('services.supabase.jwt_secret');

        $this->client = new Client([
            'base_uri' => $this->url,
            'headers' => [
                'apikey' => $this->key,
                'Content-Type' => 'application/json',
            ],
        ]);
    }

    public function signUp($email, $password, $metadata = [])
    {
        try {
            $response = $this->client->post('/auth/v1/signup', [
                'json' => [
                    'email' => $email,
                    'password' => $password,
                    'data' => $metadata,
                ],
            ]);

            return json_decode($response->getBody()->getContents(), true);
        } catch (\Exception $e) {
            Log::error('Supabase SignUp Error: ' . $e->getMessage());
            throw $e;
        }
    }

    public function signIn($email, $password)
    {
        try {
            $response = $this->client->post('/auth/v1/token?grant_type=password', [
                'json' => [
                    'email' => $email,
                    'password' => $password,
                ],
            ]);

            return json_decode($response->getBody()->getContents(), true);
        } catch (\Exception $e) {
            Log::error('Supabase SignIn Error: ' . $e->getMessage());
            throw $e;
        }
    }

    public function signOut($accessToken)
    {
        try {
            $response = $this->client->post('/auth/v1/logout', [
                'headers' => [
                    'Authorization' => 'Bearer ' . $accessToken,
                ],
            ]);

            return true;
        } catch (\Exception $e) {
            Log::error('Supabase SignOut Error: ' . $e->getMessage());
            return false;
        }
    }

    public function getUser($accessToken)
    {
        try {
            $response = $this->client->get('/auth/v1/user', [
                'headers' => [
                    'Authorization' => 'Bearer ' . $accessToken,
                ],
            ]);

            return json_decode($response->getBody()->getContents(), true);
        } catch (\GuzzleHttp\Exception\ClientException $e) {
            // Token expired or invalid - clear session
            if ($e->getResponse()->getStatusCode() === 403) {
                session()->forget(['supabase_access_token', 'supabase_refresh_token', 'supabase_user']);
                Log::warning('Supabase token expired, session cleared');
            }
            throw $e;
        } catch (\Exception $e) {
            Log::error('Supabase GetUser Error: ' . $e->getMessage());
            throw $e;
        }
    }

    public function refreshToken($refreshToken)
    {
        try {
            $response = $this->client->post('/auth/v1/token?grant_type=refresh_token', [
                'json' => [
                    'refresh_token' => $refreshToken,
                ],
            ]);

            return json_decode($response->getBody()->getContents(), true);
        } catch (\Exception $e) {
            Log::error('Supabase RefreshToken Error: ' . $e->getMessage());
            throw $e;
        }
    }

    public function resetPasswordForEmail($email)
    {
        try {
            $response = $this->client->post('/auth/v1/recover', [
                'json' => [
                    'email' => $email,
                ],
            ]);

            return json_decode($response->getBody()->getContents(), true);
        } catch (\Exception $e) {
            Log::error('Supabase ResetPassword Error: ' . $e->getMessage());
            throw $e;
        }
    }

    public function getOAuthUrl($provider, $redirectTo = null)
    {
        $params = [
            'provider' => $provider,
        ];

        if ($redirectTo) {
            $params['redirect_to'] = $redirectTo;
        }

        return $this->url . '/auth/v1/authorize?' . http_build_query($params);
    }
}
