-- minimal tables for MVP
create table profiles (
  id uuid primary key references auth.users on delete cascade,
  display_name text,
  avatar_ref text,
  daily_xp_goal int default 100,
  timezone text,
  demo_flag boolean default false,
  created_at timestamptz default now()
);

create table tasks (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references profiles(id) on delete cascade,
  title text not null,
  category text,
  xp_value int default 10,
  recurrence_rule text,
  due_time time,
  notes text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table task_completions (
  id uuid primary key default gen_random_uuid(),
  task_id uuid references tasks(id) on delete cascade,
  user_id uuid references profiles(id) on delete cascade,
  completed_at timestamptz default now(),
  xp_awarded int
);

create table streaks (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references profiles(id) on delete cascade,
  current_streak int default 0,
  longest_streak int default 0,
  last_completion_date date
);

create table ai_sessions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references profiles(id),
  session_type text,
  language_from text,
  language_to text,
  prompt_hash text,
  response_summary text,
  created_at timestamptz default now()
);

create table events (
  id bigserial primary key,
  event_name text,
  user_id uuid,
  properties jsonb,
  created_at timestamptz default now()
);
