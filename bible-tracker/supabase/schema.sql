-- Bible Tracker — Supabase sync schema (project: yzvgkyljkcksbjufneuh).
-- Idempotent: safe to re-run in the SQL editor. If you already applied the
-- Pulse schema to this project, this only widens the domain check + RLS.
--
-- Apply: paste this whole file into Supabase Dashboard → SQL Editor → Run.
-- Then whitelist the app URLs under Authentication → URL Configuration:
--   Site URL: https://changelinglabs.com/bible-tracker/
--   Redirect URLs: https://changelinglabs.com/bible-tracker/, http://localhost:8901/

create extension if not exists pgcrypto;

create table if not exists public.sync_rows (
  user_id      uuid        not null default auth.uid() references auth.users (id) on delete cascade,
  domain       text        not null,
  external_id  text        not null,
  payload      jsonb       not null,
  updated_at   timestamptz not null,
  deleted_at   timestamptz,
  primary key (user_id, domain, external_id)
);

-- Widen the domain check so 'state' (Bible Tracker's single document) is allowed.
alter table public.sync_rows drop constraint if exists sync_rows_domain_check;
alter table public.sync_rows
  add constraint sync_rows_domain_check
  check (domain in ('exercises', 'sets', 'fuel_logs', 'water_logs', 'equipment', 'state'));

create index if not exists sync_rows_user_updated on public.sync_rows (user_id, updated_at desc);

alter table public.sync_rows enable row level security;

drop policy if exists sync_rows_select on public.sync_rows;
create policy sync_rows_select on public.sync_rows
  for select using (auth.uid() = user_id);

drop policy if exists sync_rows_insert on public.sync_rows;
create policy sync_rows_insert on public.sync_rows
  for insert with check (auth.uid() = user_id);

drop policy if exists sync_rows_update on public.sync_rows;
create policy sync_rows_update on public.sync_rows
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists sync_rows_delete on public.sync_rows;
create policy sync_rows_delete on public.sync_rows
  for delete using (auth.uid() = user_id);

grant select, insert, update, delete on public.sync_rows to authenticated;