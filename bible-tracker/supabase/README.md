# Bible Tracker sync — backend setup (Supabase)

Reuses the shared `sync_rows` table (same project as Pulse is fine).

## One-time setup

1. Apply `schema.sql` in the SQL Editor (idempotent; widens the domain check).
2. Authentication → URL Configuration:
   - Site URL: `https://changelinglabs.com/bible-tracker/`
   - Redirect URLs: `https://changelinglabs.com/bible-tracker/` and `http://localhost:8901/`
3. Email provider stays on (default). Free tier is enough.

Publishable key ships in `app.js` (see `SYNC_CONFIG`). No secrets committed.