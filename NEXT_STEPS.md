# Event Horizon - Next Steps 🚀

**Last Updated:** November 25, 2024  
**Project Status:** Authentication & Base Setup Complete ✅  
**Goal:** Build a lu.ma-like event management platform

---

## 🎯 Project Vision

Building **Event Horizon** - a modern event management platform inspired by lu.ma with:
- Beautiful event landing pages
- Smooth registration/RSVP flows
- Free & paid ticketing
- Waitlists & capacity management
- Email notifications (confirmations, reminders)
- Check-in system (QR codes)
- Organizer profiles & communities
- Event analytics
- Multi-admin collaboration

---

## ✅ What's Already Done

### **Infrastructure**
- ✅ Laravel 12 + PHP 8.4 setup
- ✅ Supabase PostgreSQL database connected
- ✅ Supabase authentication integrated
- ✅ Dark theme UI (Tailwind CSS 4)
- ✅ Alpine.js for interactivity
- ✅ Vite build system
- ✅ Git repository initialized

### **Authentication (3 Methods)**
- ✅ Email/Password signup & login
- ✅ GitHub OAuth (hash-based token handling)
- ✅ Web3 Wallet (MetaMask integration)

### **Frontend**
- ✅ Black hole animated landing page
- ✅ Login/Register pages
- ✅ Basic dashboard layout
- ✅ Navigation with user session

---

## 📋 Phase 1: Core Event System (NEXT)

### **1.1 Database Schema Design**
Design and implement lu.ma-style data model:

**Tables to create:**
```
✓ users (already exists via Supabase)

□ events
  - id, organizer_id, title, slug, description
  - cover_image_url, location, location_type (online/physical)
  - start_datetime, end_datetime, timezone
  - capacity, status (draft/published/ended)
  - visibility (public/unlisted/private)
  - timestamps

□ ticket_types
  - id, event_id, name, description
  - price, currency, quantity_total, quantity_available
  - sales_start, sales_end
  - is_free, requires_approval
  - timestamps

□ registrations
  - id, event_id, user_id, ticket_type_id
  - status (pending/confirmed/cancelled/waitlist)
  - payment_status (null/pending/paid/refunded)
  - checked_in_at
  - registration_data (jsonb for custom questions)
  - timestamps

□ communities (organizer profiles)
  - id, user_id, name, slug, bio
  - avatar_url, website
  - timestamps

□ event_views (analytics)
  - id, event_id, user_id (nullable)
  - viewed_at, ip_address, user_agent
  - timestamps
```

**Relationships:**
- User → Events (organizer)
- Event → Ticket Types (has many)
- Event → Registrations (has many)
- User → Registrations (attendee)
- User → Community (has one)
- Community → Events (has many)

### **1.2 Eloquent Models**
Create models with relationships:
```
□ app/Models/Event.php
□ app/Models/TicketType.php
□ app/Models/Registration.php
□ app/Models/Community.php
□ app/Models/EventView.php
```

### **1.3 Event CRUD**
Implement event management:
```
□ EventController (create, store, edit, update, destroy)
□ routes/web.php (event routes)
□ Form validation (EventRequest)
□ Event policies (authorization)
```

### **1.4 Event Landing Pages**
Beautiful lu.ma-style event pages:
```
□ resources/views/events/show.blade.php
□ Cover image display
□ Event details (date, time, location)
□ Ticket selection UI
□ Register/RSVP button
□ Share buttons
```

---

## �� Phase 2: Registration & Ticketing

### **2.1 Registration Flow**
```
□ Registration form with ticket selection
□ Guest info collection (name, email, custom questions)
□ Capacity checking
□ Waitlist when full
□ Confirmation page
```

### **2.2 Email Notifications**
```
□ Laravel notifications setup
□ Confirmation email (on registration)
□ Reminder email (24h before event)
□ Follow-up email (after event)
□ Cancellation email
□ Waitlist notification (when spot opens)
```

### **2.3 Attendee Management**
```
□ Organizer dashboard: view registrations
□ Attendee list export (CSV)
□ Search/filter attendees
□ Cancel/refund registrations
□ Send messages to attendees
```

---

## 📋 Phase 3: Organizer Features

### **3.1 Community/Profile Pages**
```
□ Organizer profile creation
□ Custom slug (e.g., lu.ma/@yourname)
□ List all events by organizer
□ Follow/subscribe to organizers
□ Bio, avatar, social links
```

### **3.2 Event Analytics**
```
□ Page views tracking
□ Registration conversion rate
□ Ticket sales by type
□ Revenue tracking (paid events)
□ Attendee demographics
□ Check-in rate
```

### **3.3 Check-in System**
```
□ Generate QR codes for attendees
□ Scan QR codes (mobile-friendly)
□ Manual check-in (search by name/email)
□ Check-in status in attendee list
□ Real-time check-in count
```

### **3.4 Multi-Admin Collaboration**
```
□ Event team members table
□ Invite co-organizers
□ Role-based permissions (admin/editor/viewer)
□ Activity log
```

---

## 📋 Phase 4: Advanced Features

### **4.1 Paid Ticketing**
```
□ Stripe integration
□ Payment processing
□ Refund handling
□ Discount codes
□ Early bird pricing
```

### **4.2 Recurring Events**
```
□ Event series model
□ Recurring schedule (weekly, monthly)
□ Bulk registration for series
□ Series management UI
```

### **4.3 Custom Questions**
```
□ Form builder for registration
□ Custom field types (text, select, checkbox)
□ Conditional questions
□ Store responses in jsonb
```

### **4.4 Integrations & API**
```
□ RESTful API for events
□ Webhooks (registration, check-in)
□ Calendar sync (Google Calendar, iCal)
□ Zapier integration
```

---

## 🗂️ Project Structure (Proposed)

```
app/
├── Models/
│   ├── Event.php
│   ├── TicketType.php
│   ├── Registration.php
│   ├── Community.php
│   └── EventView.php
├── Http/Controllers/
│   ├── EventController.php
│   ├── RegistrationController.php
│   ├── CommunityController.php
│   └── CheckInController.php
├── Services/
│   ├── SupabaseService.php (exists)
│   ├── EventService.php
│   ├── TicketService.php
│   └── NotificationService.php
├── Notifications/
│   ├── EventConfirmation.php
│   ├── EventReminder.php
│   └── WaitlistNotification.php
└── Policies/
    ├── EventPolicy.php
    └── RegistrationPolicy.php

database/migrations/
├── 2024_11_26_create_events_table.php
├── 2024_11_26_create_ticket_types_table.php
├── 2024_11_26_create_registrations_table.php
├── 2024_11_26_create_communities_table.php
└── 2024_11_26_create_event_views_table.php

resources/views/
├── events/
│   ├── index.blade.php (browse/discover)
│   ├── show.blade.php (event landing page)
│   ├── create.blade.php
│   └── edit.blade.php
├── registrations/
│   ├── create.blade.php (registration form)
│   └── confirmation.blade.php
└── communities/
    └── show.blade.php (organizer profile)
```

---

## �� Technical Decisions to Make

### **Storage**
- [ ] Use Supabase Storage or AWS S3 for event images?
- [ ] Image optimization strategy?

### **Queue/Jobs**
- [ ] Email delivery (queue vs sync)?
- [ ] Background job for analytics?
- [ ] Which queue driver (database, Redis, Supabase)?

### **Search**
- [ ] Event search/filtering strategy?
- [ ] Full-text search in PostgreSQL?
- [ ] External search service (Algolia, Meilisearch)?

### **Real-time**
- [ ] Use Supabase Realtime for live updates?
- [ ] WebSockets for check-in counter?

### **API**
- [ ] API versioning strategy?
- [ ] Laravel Sanctum for API tokens?
- [ ] GraphQL or REST?

---

## 📚 Resources & References

### **lu.ma Inspiration**
- Event page design: Clean, minimal, mobile-first
- Registration flow: 2-3 steps max
- Ticketing: Clear pricing, quantity selector
- Email style: Simple, branded, actionable

### **Laravel Resources**
- Events/Listeners for decoupled logic
- Queue jobs for async tasks
- Policies for authorization
- Form Requests for validation

### **Supabase Resources**
- Row Level Security (RLS) for access control
- Storage for images/files
- Realtime subscriptions (optional)
- PostgREST for direct DB access

---

## 🎯 Immediate Next Session Tasks

**When you're ready, we'll start with:**

1. **Database schema design** - Create migrations for core tables
2. **Event model** - Build the main Event entity with relationships
3. **Event creation** - Let organizers create their first event
4. **Event landing page** - Beautiful lu.ma-style event view

**Questions to answer:**
- What event details do we want to collect initially?
- Should we start with free events only, or include paid from the start?
- Do you want waitlist functionality in MVP?
- Which email service for notifications (Laravel Mail, Supabase, external)?

---

## 📝 Notes

- Authentication is solid (3 methods working)
- Database is Supabase PostgreSQL (already connected)
- Frontend is Alpine.js + Tailwind (dark theme)
- Git repo initialized (commit: 461814d)
- All sensitive data (.env) is gitignored ✅

---

**Ready to build when you are!** 🚀

Built with ❤️ for Event Horizon
