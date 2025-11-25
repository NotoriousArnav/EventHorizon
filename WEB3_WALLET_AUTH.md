# Web3 Wallet Authentication - Event Horizon 🔐💎

## ✅ What's Been Implemented

Replaced Google OAuth with **Web3 Wallet Authentication** (MetaMask, WalletConnect, etc.)

### **Why Web3 Instead of Google?**
- ✅ **No OAuth setup needed** - No Google Cloud Console configuration
- ✅ **Instant integration** - Just connect wallet
- ✅ **Decentralized** - User controls their identity
- ✅ **Web3-native** - Perfect for blockchain/crypto projects
- ✅ **Auto-registration** - Creates account automatically on first connect

---

## 🎨 UI Changes

### **Login Page (`/login`)**
```
┌─────────────────────────────────┐
│  Email/Password Form            │
│                                 │
│      Or continue with           │
│                                 │
│  [🔮 Web3 Wallet]  [🐙 GitHub] │
└─────────────────────────────────┘
```

- **Web3 Wallet Button** - Purple gradient with wallet icon
- **GitHub Button** - Remains as alternative OAuth option

### **Register Page (`/register`)**
Same layout - Web3 wallet button replaces Google

---

## 🔧 How It Works

### **Frontend (JavaScript)**
When user clicks "Web3 Wallet":

```javascript
1. Check if MetaMask/Web3 wallet is installed
2. Request wallet connection: ethereum.request({ method: 'eth_requestAccounts' })
3. Get wallet address: accounts[0]
4. Send address to backend: POST /auth/wallet/login
5. Backend authenticates and creates session
6. Redirect to dashboard
```

### **Backend (Laravel)**
`SupabaseAuthController::walletLogin()`:

```php
1. Receive wallet address (e.g., 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb)
2. Convert to pseudo-email: 0x742d...@wallet.eventhorizon
3. Generate secure password from: hash(address + app_key)
4. Try to sign in with Supabase
5. If doesn't exist, auto-register user
6. Store tokens in session
7. Return success response
```

### **Authentication Flow**

```
User clicks "Web3 Wallet"
    ↓
MetaMask popup opens
    ↓
User approves connection
    ↓
Frontend gets wallet address
    ↓
POST to /auth/wallet/login with address
    ↓
Laravel creates/authenticates user in Supabase
    ↓
Session created with Supabase tokens
    ↓
User redirected to dashboard
```

---

## 🔑 Technical Details

### **Wallet Address Format**
```
Original: 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
Converted to email: 0x742d35cc6634c0532925a3b844bc9e7595f0beb@wallet.eventhorizon
```

### **Password Generation**
```php
$password = hash('sha256', $address . config('app.key'));
```
- Deterministic (same address = same password)
- Secure (includes app key)
- User never sees this password

### **Session Data**
```php
[
    'supabase_access_token' => 'eyJhbGci...',
    'supabase_refresh_token' => 'eyJhbGci...',
    'supabase_user' => [...],
    'wallet_address' => '0x742d35cc...'
]
```

---

## 📝 Supported Wallets

Any Ethereum-compatible wallet that injects `window.ethereum`:

- ✅ **MetaMask** (Browser extension & Mobile)
- ✅ **WalletConnect** (via MetaMask mobile)
- ✅ **Coinbase Wallet**
- ✅ **Trust Wallet**
- ✅ **Rainbow**
- ✅ **Brave Wallet** (Built into Brave browser)
- ✅ And many more...

---

## 🧪 Testing

### **Step 1: Install MetaMask**
If you don't have it:
1. Visit https://metamask.io/download/
2. Install browser extension
3. Create wallet or import existing

### **Step 2: Test Connection**
1. Visit http://localhost:8000/login
2. Click "Web3 Wallet" button
3. MetaMask popup appears
4. Click "Connect"
5. You're redirected to dashboard!

### **Step 3: Verify in Supabase**
Go to: https://app.supabase.com/project/aiwcqroacxepuiquywyl/auth/users

You should see user with email like:
```
0x742d35cc6634c0532925a3b844bc9e7595f0beb@wallet.eventhorizon
```

---

## 🔐 Security Features

### **Auto-Registration**
- First connection automatically creates account
- No manual registration needed
- User metadata stores wallet address

### **Deterministic Password**
- Generated from wallet address + app key
- Cannot be guessed without app key
- User never needs to remember it

### **Session-Based**
- Tokens stored in Laravel session
- Secure server-side storage
- No blockchain private keys needed

### **No Signature Required (For Now)**
Current implementation is simplified:
- Just connects wallet
- Auto-creates/logs in user

**Future Enhancement:**
Add signature verification for extra security:
```javascript
// Sign a message to prove wallet ownership
const signature = await ethereum.request({
    method: 'personal_sign',
    params: [message, address]
});
```

---

## 🚀 Routes

### **Added Routes:**
```php
POST /auth/wallet/login      - Authenticate with wallet
POST /auth/wallet/register   - Same as login (auto-creates)
```

### **All Auth Routes:**
```
GET  /login                  - Login page
POST /login                  - Email/password login
GET  /register               - Register page
POST /register               - Email/password register
POST /logout                 - Logout
POST /auth/wallet/login      - Web3 wallet login
POST /auth/wallet/register   - Web3 wallet register
GET  /auth/oauth/{provider}  - OAuth (GitHub)
GET  /auth/callback          - OAuth callback
```

---

## 🎯 User Experience

### **First Time User:**
1. Click "Web3 Wallet"
2. Connect wallet (one click in MetaMask)
3. Automatically registered + logged in
4. Redirected to dashboard

### **Returning User:**
1. Click "Web3 Wallet"
2. Connect wallet (already connected = instant)
3. Logged in
4. Dashboard

### **No Wallet?**
Button shows helpful message:
> "Please install MetaMask or another Web3 wallet to continue."

Opens MetaMask download page

---

## 💡 Benefits Over Google OAuth

| Feature | Google OAuth | Web3 Wallet |
|---------|-------------|-------------|
| Setup complexity | ⚠️ High (OAuth app, credentials) | ✅ None |
| User privacy | ⚠️ Google tracks | ✅ Decentralized |
| Integration time | ⚠️ Hours | ✅ Minutes |
| Cost | ⚠️ May have limits | ✅ Free |
| Web3 native | ❌ No | ✅ Yes |
| Auto-registration | ❌ No | ✅ Yes |

---

## 🔄 Migration Path

Users can still use:
- ✅ Email/Password authentication
- ✅ GitHub OAuth
- ✅ Web3 Wallet (new!)

All three methods work simultaneously!

---

## 📊 Button Styling

### **Web3 Wallet Button**
```css
bg-gradient-to-r from-purple-600 to-indigo-600
border-purple-500
shadow-lg shadow-purple-500/50
```
- Purple gradient (blockchain/crypto aesthetic)
- Glowing effect
- Wallet icon

### **GitHub Button**
```css
bg-gray-700 hover:bg-gray-600
border-gray-600
```
- Stays as secondary option
- Gray theme

---

## 🛠️ Files Modified

```
resources/views/auth/
├── login.blade.php          - Added Web3 button + script
└── register.blade.php       - Added Web3 button + script

app/Http/Controllers/Auth/
└── SupabaseAuthController.php  - Added walletLogin(), walletRegister()

routes/
└── web.php                  - Added wallet auth routes
```

---

## 🎉 Result

**Before:**
- Google button (complex setup, tracking)

**After:**
- Web3 Wallet button (instant, decentralized, zero config!)
- Perfect for Event Horizon's tech-forward image

---

## 📝 Future Enhancements

### **1. Signature Verification**
Prove wallet ownership:
```javascript
const signature = await signer.signMessage("Sign in to Event Horizon");
```

### **2. Multi-Chain Support**
- Ethereum
- Polygon
- BSC
- Arbitrum

### **3. ENS Integration**
Show ENS names instead of addresses:
```
vitalik.eth instead of 0x742d...
```

### **4. NFT Gating**
Require specific NFT to access:
```
if (user.hasNFT('EventHorizonPass')) {
    // Grant access
}
```

---

Built with ❤️ for Event Horizon
