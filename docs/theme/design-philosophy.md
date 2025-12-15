# Design Philosophy

Event Horizon adopts a **Sci-Fi / Command Terminal** aesthetic.

## Color Palette

- **Background:** `slate-900` (#0f172a) - Deep Space
- **Surface:** `slate-800` (#1e293b) - Ship Panels
- **Primary:** `sky-500` (#0ea5e9) - Holographic Interface
- **Accent:** `cyan-400` (#22d3ee) - Data Streams
- **Danger:** `red-500` (#ef4444) - Critical Alerts

## Typography

- **Font Family:** `Courier New`, `Monospace`
- **Style:** All headers are uppercase with a ">" prefix (e.g., `> MISSION LOG`).
- **Feel:** Retro-futuristic, functional, brutalist.

## UI Components

### Glassmorphism
Elements use subtle semi-transparent backgrounds with borders to mimic glass displays on a spaceship dashboard.

### Status Indicators
- **Green:** Active / Operational
- **Yellow:** Waitlisted / Standby
- **Red:** Cancelled / Critical Failure

## Customizing the Theme

The theme is built using **Tailwind CSS**. You can customize the look by editing `templates/base.html` or configuring `tailwind.config.js` (if building assets).
