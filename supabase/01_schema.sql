-- =====================================================================
--  FME-Quiz  ·  Datenbank-Schema für Supabase (PostgreSQL)
--  Lehrstuhl für Förder- und Materialflusstechnik (FMT), OVGU Magdeburg
--
--  Ausführen: Supabase → SQL Editor → Inhalt einfügen → "Run".
--  Das Skript kann gefahrlos mehrfach ausgeführt werden.
--
--  Sicherheitskonzept:
--   * Alle Tabellen sind für den Browser gesperrt (RLS ohne Policies).
--   * Der Browser ruft ausschließlich die unten definierten Funktionen
--     (RPC) auf. Diese prüfen Login, Zeit und Antworten serverseitig.
--   * Passwörter werden mit bcrypt gehasht (pgcrypto).
-- =====================================================================

create extension if not exists pgcrypto with schema extensions;

-- ---------------------------------------------------------------------
--  Tabellen
-- ---------------------------------------------------------------------
create table if not exists public.players (
  id            bigserial primary key,
  nickname      text not null,
  pw_hash       text not null,
  is_admin      boolean not null default false,
  failed_logins int not null default 0,
  locked_until  timestamptz,
  created_at    timestamptz not null default now()
);
create unique index if not exists players_nick_uq on public.players (lower(nickname));

create table if not exists public.sessions (
  token      uuid primary key default gen_random_uuid(),
  player_id  bigint not null references public.players(id) on delete cascade,
  created_at timestamptz not null default now(),
  expires_at timestamptz not null default now() + interval '30 days'
);

create table if not exists public.topics (
  id      text primary key,
  sort    int  not null default 0,
  name_de text not null,
  name_en text not null
);

-- qtype:  mc    = Multiple Choice (Text)
--         img   = Bild erkennen (Multiple Choice mit Abbildung)
--         tf    = Wahr / Falsch
--         match = Zuordnen (nur Learn-Modus)
--
-- options:  mc/img : [{"de":"…","en":"…"}, …]          correct: Index (Zahl)
--           tf     : null                                 correct: true/false
--           match  : {"left":[{de,en}…],"right":[{de,en}…]}  correct: null
--                    (left[i] gehört zu right[i])
--
-- Fachbegriffe werden im Text markiert:
--   prompt_de: "Ein {{Rillenkugellager|deep groove ball bearing}} …"
--   prompt_en: "A {{deep groove ball bearing|Rillenkugellager}} …"
create table if not exists public.questions (
  id             serial primary key,
  topic_id       text not null references public.topics(id),
  qtype          text not null check (qtype in ('mc','img','tf','match')),
  prompt_de      text not null,
  prompt_en      text not null,
  image          text,
  options        jsonb,
  correct        jsonb,
  explanation_de text not null default '',
  explanation_en text not null default '',
  active         boolean not null default true,
  created_at     timestamptz not null default now(),
  updated_at     timestamptz not null default now()
);
alter table public.questions add column if not exists image_source text;  -- Quellenangabe zur Abbildung
create index if not exists questions_topic_idx on public.questions (topic_id) where active;

-- Learn-Modus: Karteikasten (Leitner) je Spieler und Frage
create table if not exists public.progress (
  player_id  bigint not null references public.players(id) on delete cascade,
  question_id int   not null references public.questions(id) on delete cascade,
  box        int    not null default 0,      -- 0 = zuletzt falsch … 5 = sicher
  n_right    int    not null default 0,
  n_wrong    int    not null default 0,
  last_seen  timestamptz not null default now(),
  primary key (player_id, question_id)
);

-- Speed-Modus: jeder Lauf wird serverseitig geführt
create table if not exists public.speed_runs (
  id          uuid primary key default gen_random_uuid(),
  player_id   bigint not null references public.players(id) on delete cascade,
  topics      text[],
  started_at  timestamptz not null default now(),
  ends_at     timestamptz not null,
  score       int not null default 0,
  streak      int not null default 0,
  best_streak int not null default 0,
  answered    int not null default 0,
  n_correct   int not null default 0,
  current_qid int,
  served      int[] not null default '{}',
  in_ranking  boolean not null default true
);
create index if not exists speed_runs_score_idx on public.speed_runs (score desc) where in_ranking;

-- Meldungen: Spieler halten Frage oder Lösung für falsch
create table if not exists public.reports (
  id          bigserial primary key,
  question_id int not null references public.questions(id) on delete cascade,
  player_id   bigint references public.players(id) on delete set null,
  reason      text not null,          -- 'answer' | 'question' | 'translation' | 'image' | 'other'
  comment     text not null default '',
  lang        text,
  status      text not null default 'open' check (status in ('open','done')),
  created_at  timestamptz not null default now()
);

-- Einstellungen (z. B. Dauer des Speed-Modus)
create table if not exists public.settings (
  key   text primary key,
  value jsonb not null
);
insert into public.settings (key, value) values
  ('speed_seconds', '60'),
  ('speed_base_points', '10')
on conflict (key) do nothing;

-- Browser darf keine Tabelle direkt lesen/schreiben
alter table public.players    enable row level security;
alter table public.sessions   enable row level security;
alter table public.topics     enable row level security;
alter table public.questions  enable row level security;
alter table public.progress   enable row level security;
alter table public.speed_runs enable row level security;
alter table public.settings   enable row level security;
alter table public.reports    enable row level security;
revoke all on all tables    in schema public from anon, authenticated;
revoke all on all sequences in schema public from anon, authenticated;

-- ---------------------------------------------------------------------
--  Hilfsfunktionen (intern)
-- ---------------------------------------------------------------------
create or replace function public._player_from_token(p_token uuid)
returns public.players
language plpgsql security definer set search_path = public, extensions as $$
declare r public.players;
begin
  select p.* into r
    from public.sessions s join public.players p on p.id = s.player_id
   where s.token = p_token and s.expires_at > now();
  if r.id is null then
    raise exception 'not_logged_in' using errcode = 'P0001';
  end if;
  return r;
end $$;

create or replace function public._require_admin(p_token uuid)
returns public.players
language plpgsql security definer set search_path = public, extensions as $$
declare r public.players;
begin
  r := public._player_from_token(p_token);
  if not r.is_admin then
    raise exception 'not_admin' using errcode = 'P0001';
  end if;
  return r;
end $$;

-- Frage ohne Lösung für den Browser
create or replace function public._public_question(q public.questions)
returns jsonb
language sql immutable as $$
  select jsonb_build_object(
    'id', q.id, 'topic', q.topic_id, 'type', q.qtype,
    'prompt_de', q.prompt_de, 'prompt_en', q.prompt_en,
    'image', q.image, 'image_source', q.image_source, 'options', q.options)
$$;

-- Antwort prüfen
create or replace function public._is_correct(q public.questions, p_answer jsonb)
returns boolean
language plpgsql immutable as $$
declare n int; i int;
begin
  if p_answer is null or p_answer = 'null'::jsonb then
    return false;
  end if;
  if q.qtype in ('mc','img') then
    return jsonb_typeof(p_answer) = 'number' and p_answer = q.correct;
  elsif q.qtype = 'tf' then
    return jsonb_typeof(p_answer) = 'boolean' and p_answer = q.correct;
  elsif q.qtype = 'match' then
    -- Antwort: Array; Element i = Index des rechten Eintrags, der zu left[i] gewählt wurde
    n := jsonb_array_length(q.options->'left');
    if jsonb_typeof(p_answer) <> 'array' or jsonb_array_length(p_answer) <> n then
      return false;
    end if;
    for i in 0 .. n-1 loop
      if (p_answer->>i) is distinct from i::text then
        return false;
      end if;
    end loop;
    return true;
  end if;
  return false;
end $$;

create or replace function public._clean_nick(p_nick text)
returns text language sql immutable as $$
  select btrim(coalesce(p_nick,''))
$$;

-- ---------------------------------------------------------------------
--  Öffentliche Funktionen: Anmeldung
-- ---------------------------------------------------------------------
create or replace function public.quiz_register(p_nickname text, p_password text)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
declare v_nick text := public._clean_nick(p_nickname); v_id bigint; v_token uuid;
begin
  if v_nick !~ '^[A-Za-z0-9ÄÖÜäöüß_.\-]{3,20}$' then
    raise exception 'bad_nickname' using errcode = 'P0001';
  end if;
  if length(coalesce(p_password,'')) < 6 or length(p_password) > 72 then
    raise exception 'bad_password' using errcode = 'P0001';
  end if;
  if exists (select 1 from public.players where lower(nickname) = lower(v_nick)) then
    raise exception 'nickname_taken' using errcode = 'P0001';
  end if;
  insert into public.players (nickname, pw_hash)
       values (v_nick, crypt(p_password, gen_salt('bf', 8)))
    returning id into v_id;
  insert into public.sessions (player_id) values (v_id) returning token into v_token;
  return jsonb_build_object('token', v_token, 'nickname', v_nick, 'is_admin', false);
end $$;

create or replace function public.quiz_login(p_nickname text, p_password text)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
declare r public.players; v_token uuid;
begin
  select * into r from public.players where lower(nickname) = lower(public._clean_nick(p_nickname));
  if r.id is null then
    raise exception 'login_failed' using errcode = 'P0001';
  end if;
  if r.locked_until is not null and r.locked_until > now() then
    raise exception 'locked' using errcode = 'P0001';
  end if;
  if r.pw_hash <> crypt(coalesce(p_password,''), r.pw_hash) then
    update public.players
       set failed_logins = failed_logins + 1,
           locked_until  = case when failed_logins + 1 >= 8 then now() + interval '5 minutes' end
     where id = r.id;
    raise exception 'login_failed' using errcode = 'P0001';
  end if;
  update public.players set failed_logins = 0, locked_until = null where id = r.id;
  delete from public.sessions where expires_at < now();
  insert into public.sessions (player_id) values (r.id) returning token into v_token;
  return jsonb_build_object('token', v_token, 'nickname', r.nickname, 'is_admin', r.is_admin);
end $$;

create or replace function public.quiz_logout(p_token uuid)
returns jsonb
language sql security definer set search_path = public, extensions as $$
  delete from public.sessions where token = p_token;
  select '{"ok":true}'::jsonb;
$$;

create or replace function public.quiz_me(p_token uuid)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
declare r public.players; v_best int; v_rank int;
begin
  r := public._player_from_token(p_token);
  select max(score) into v_best from public.speed_runs where player_id = r.id and in_ranking and score > 0;
  if v_best is not null then
    select 1 + count(*) into v_rank from (
      select player_id, max(score) s from public.speed_runs where in_ranking group by player_id
    ) t where t.s > v_best;
  end if;
  return jsonb_build_object('nickname', r.nickname, 'is_admin', r.is_admin,
                            'best', v_best, 'rank', v_rank,
                            'speed_seconds', (select (value)::int from public.settings where key = 'speed_seconds'));
end $$;

create or replace function public.quiz_change_password(p_token uuid, p_old text, p_new text)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
declare r public.players;
begin
  r := public._player_from_token(p_token);
  if r.pw_hash <> crypt(coalesce(p_old,''), r.pw_hash) then
    raise exception 'login_failed' using errcode = 'P0001';
  end if;
  if length(coalesce(p_new,'')) < 6 or length(p_new) > 72 then
    raise exception 'bad_password' using errcode = 'P0001';
  end if;
  update public.players set pw_hash = crypt(p_new, gen_salt('bf', 8)) where id = r.id;
  return '{"ok":true}'::jsonb;
end $$;

-- ---------------------------------------------------------------------
--  Öffentlich: Bestenliste + Themen
-- ---------------------------------------------------------------------
create or replace function public.quiz_top(p_limit int default 5)
returns jsonb
language sql stable security definer set search_path = public, extensions as $$
  select coalesce(jsonb_agg(t order by t.score desc, t.at asc), '[]'::jsonb)
  from (
    select * from (
      select distinct on (r.player_id)
             p.nickname, r.score, r.best_streak, r.started_at as at
        from public.speed_runs r join public.players p on p.id = r.player_id
       where r.in_ranking and r.score > 0
       order by r.player_id, r.score desc, r.started_at asc
    ) b
    order by b.score desc, b.at asc
    limit least(greatest(coalesce(p_limit,5),1),50)
  ) t
$$;

create or replace function public.quiz_topics()
returns jsonb
language sql stable security definer set search_path = public, extensions as $$
  select coalesce(jsonb_agg(jsonb_build_object(
           'id', t.id, 'name_de', t.name_de, 'name_en', t.name_en,
           'count', (select count(*) from public.questions q where q.topic_id = t.id and q.active),
           'speed_count', (select count(*) from public.questions q where q.topic_id = t.id and q.active and q.qtype <> 'match'))
         order by t.sort), '[]'::jsonb)
  from public.topics t
$$;

-- ---------------------------------------------------------------------
--  Learn-Modus (Karteikasten / Leitner)
--    Fach 0 = zuletzt falsch  → kommt sehr oft
--    neu                      → oft
--    Fach 1 … 5               → immer seltener
-- ---------------------------------------------------------------------
create or replace function public.quiz_learn_next(p_token uuid, p_topics text[] default null)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
declare r public.players; q public.questions; v_box int; v_qid int;
begin
  r := public._player_from_token(p_token);
  with cand as (
    select qq.*, pr.box, pr.last_seen,
           case when pr.box is null then 6.0
                else (array[12.0, 5.0, 2.5, 1.2, 0.6, 0.3])[pr.box + 1] end as w
      from public.questions qq
      left join public.progress pr on pr.question_id = qq.id and pr.player_id = r.id
     where qq.active
       and (p_topics is null or cardinality(p_topics) = 0 or qq.topic_id = any(p_topics))
  ), recent as (
    -- die 3 zuletzt gesehenen Fragen nicht direkt wiederholen (wenn genug Auswahl)
    select question_id from public.progress
     where player_id = r.id order by last_seen desc limit 3
  ), pool as (
    select * from cand
     where (select count(*) from cand) <= 4
        or id not in (select question_id from recent)
  )
  -- gewichtete Zufallsauswahl (Efraimidis-Spirakis)
  select p.id into v_qid
    from pool p
   order by -ln(1.0 - random()) / p.w
   limit 1;

  select * into q from public.questions where id = v_qid;
  if q.id is null then
    return jsonb_build_object('question', null);
  end if;
  select box into v_box from public.progress where player_id = r.id and question_id = q.id;
  return jsonb_build_object('question', public._public_question(q), 'box', v_box);
end $$;

create or replace function public.quiz_learn_answer(p_token uuid, p_question_id int, p_answer jsonb)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
declare r public.players; q public.questions; ok boolean; v_box int;
begin
  r := public._player_from_token(p_token);
  select * into q from public.questions where id = p_question_id;
  if q.id is null then raise exception 'unknown_question' using errcode = 'P0001'; end if;
  ok := public._is_correct(q, p_answer);

  insert into public.progress as pr (player_id, question_id, box, n_right, n_wrong, last_seen)
  values (r.id, q.id, case when ok then 1 else 0 end,
          case when ok then 1 else 0 end, case when ok then 0 else 1 end, now())
  on conflict (player_id, question_id) do update
     set box       = case when ok then least(pr.box + 1, 5) else 0 end,
         n_right   = pr.n_right + case when ok then 1 else 0 end,
         n_wrong   = pr.n_wrong + case when ok then 0 else 1 end,
         last_seen = now()
  returning box into v_box;

  return jsonb_build_object('correct', ok, 'solution', q.correct, 'box', v_box,
                            'explanation_de', q.explanation_de, 'explanation_en', q.explanation_en);
end $$;

create or replace function public.quiz_learn_stats(p_token uuid)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
declare r public.players; res jsonb;
begin
  r := public._player_from_token(p_token);
  select coalesce(jsonb_agg(x order by x.sort), '[]'::jsonb) into res from (
    select t.id as topic, t.sort,
           count(q.id)                                         as total,
           count(pr.question_id)                               as seen,
           count(*) filter (where pr.box >= 3)                 as mastered,
           count(*) filter (where pr.box = 0)                  as weak
      from public.topics t
      join public.questions q on q.topic_id = t.id and q.active
      left join public.progress pr on pr.question_id = q.id and pr.player_id = r.id
     group by t.id, t.sort
  ) x;
  return res;
end $$;

create or replace function public.quiz_learn_reset(p_token uuid)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
declare r public.players;
begin
  r := public._player_from_token(p_token);
  delete from public.progress where player_id = r.id;
  return '{"ok":true}'::jsonb;
end $$;

-- ---------------------------------------------------------------------
--  Speed-Modus (Zeit und Punkte werden nur auf dem Server gezählt)
--    10 Punkte je richtige Antwort
--    ab 3 richtigen in Folge ×2, ab 5 in Folge ×3
--    falsche Antwort → Serie zurück auf 0
-- ---------------------------------------------------------------------
create or replace function public._speed_pick(p_run public.speed_runs)
returns public.questions
language plpgsql security definer set search_path = public, extensions as $$
declare q public.questions;
begin
  select * into q from public.questions
   where active and qtype <> 'match'
     and (p_run.topics is null or cardinality(p_run.topics) = 0 or topic_id = any(p_run.topics))
     and not (id = any(p_run.served))
   order by random() limit 1;
  if q.id is null then
    -- alle Fragen gesehen → wieder von vorn (außer der letzten)
    select * into q from public.questions
     where active and qtype <> 'match'
       and (p_run.topics is null or cardinality(p_run.topics) = 0 or topic_id = any(p_run.topics))
       and id is distinct from p_run.current_qid
     order by random() limit 1;
  end if;
  return q;
end $$;

create or replace function public.quiz_speed_start(p_token uuid, p_topics text[] default null)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
declare r public.players; run public.speed_runs; q public.questions; v_secs int;
begin
  r := public._player_from_token(p_token);
  select (value)::int into v_secs from public.settings where key = 'speed_seconds';
  v_secs := coalesce(v_secs, 60);
  -- vorherige offene Läufe dieses Spielers beenden
  update public.speed_runs set ends_at = least(ends_at, now()) where player_id = r.id and ends_at > now();

  insert into public.speed_runs (player_id, topics, ends_at)
       values (r.id, p_topics, now() + make_interval(secs => v_secs))
    returning * into run;
  q := public._speed_pick(run);
  if q.id is null then raise exception 'no_questions' using errcode = 'P0001'; end if;
  update public.speed_runs set current_qid = q.id, served = served || q.id where id = run.id;
  return jsonb_build_object('run', run.id, 'seconds', v_secs,
                            'time_left_ms', v_secs * 1000,
                            'question', public._public_question(q));
end $$;

create or replace function public.quiz_speed_answer(p_token uuid, p_run uuid, p_question_id int, p_answer jsonb)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
declare r public.players; run public.speed_runs; q public.questions; nq public.questions;
        ok boolean; v_mult int := 1; v_pts int := 0; v_base int; v_left numeric;
begin
  r := public._player_from_token(p_token);
  select * into run from public.speed_runs where id = p_run and player_id = r.id for update;
  if run.id is null then raise exception 'unknown_run' using errcode = 'P0001'; end if;
  v_left := extract(epoch from (run.ends_at - now())) * 1000;

  -- 1,5 s Kulanz für die Netzwerklaufzeit der letzten Antwort
  if v_left < -1500 or run.current_qid is null then
    update public.speed_runs set current_qid = null where id = run.id;
    return jsonb_build_object('finished', true, 'score', run.score, 'best_streak', run.best_streak,
                              'answered', run.answered, 'n_correct', run.n_correct);
  end if;
  if p_question_id is distinct from run.current_qid then
    raise exception 'wrong_question' using errcode = 'P0001';
  end if;

  select * into q from public.questions where id = run.current_qid;
  ok := public._is_correct(q, p_answer);
  select (value)::int into v_base from public.settings where key = 'speed_base_points';
  v_base := coalesce(v_base, 10);

  if ok then
    run.streak := run.streak + 1;
    v_mult := case when run.streak >= 5 then 3 when run.streak >= 3 then 2 else 1 end;
    v_pts  := v_base * v_mult;
    run.score := run.score + v_pts;
    run.n_correct := run.n_correct + 1;
    run.best_streak := greatest(run.best_streak, run.streak);
  else
    run.streak := 0;
  end if;
  run.answered := run.answered + 1;

  if v_left > 0 then
    nq := public._speed_pick(run);
  end if;

  update public.speed_runs
     set score = run.score, streak = run.streak, best_streak = run.best_streak,
         answered = run.answered, n_correct = run.n_correct,
         current_qid = nq.id,
         served = case when nq.id is null then served else served || nq.id end
   where id = run.id;

  return jsonb_build_object(
    'correct', ok, 'solution', q.correct, 'points', v_pts, 'multiplier', v_mult,
    'score', run.score, 'streak', run.streak, 'best_streak', run.best_streak,
    'answered', run.answered, 'n_correct', run.n_correct,
    'time_left_ms', greatest(v_left, 0)::int,
    'finished', nq.id is null,
    'question', case when nq.id is null then null else public._public_question(nq) end);
end $$;

create or replace function public.quiz_speed_finish(p_token uuid, p_run uuid)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
declare r public.players; run public.speed_runs; v_rank int; v_best int;
begin
  r := public._player_from_token(p_token);
  update public.speed_runs set current_qid = null, ends_at = least(ends_at, now())
   where id = p_run and player_id = r.id
   returning * into run;
  if run.id is null then raise exception 'unknown_run' using errcode = 'P0001'; end if;
  select max(score) into v_best from public.speed_runs where player_id = r.id and in_ranking;
  select 1 + count(*) into v_rank from (
    select player_id, max(score) s from public.speed_runs where in_ranking group by player_id
  ) t where t.s > coalesce(v_best,0);
  return jsonb_build_object('score', run.score, 'best_streak', run.best_streak,
                            'answered', run.answered, 'n_correct', run.n_correct,
                            'personal_best', v_best, 'rank', v_rank,
                            'new_best', run.score >= coalesce(v_best,0) and run.score > 0);
end $$;

-- ---------------------------------------------------------------------
--  Admin-Funktionen (nur für Spieler mit is_admin = true)
-- ---------------------------------------------------------------------
create or replace function public.admin_questions(p_token uuid)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
begin
  perform public._require_admin(p_token);
  return (select coalesce(jsonb_agg(to_jsonb(q) order by q.topic_id, q.id), '[]'::jsonb)
            from public.questions q);
end $$;

create or replace function public.admin_save_question(p_token uuid, p_q jsonb)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
declare v_id int;
begin
  perform public._require_admin(p_token);
  if (p_q->>'qtype') not in ('mc','img','tf','match') then
    raise exception 'bad_type' using errcode = 'P0001';
  end if;
  if nullif(p_q->>'id','') is null then
    insert into public.questions (topic_id, qtype, prompt_de, prompt_en, image, image_source, options, correct,
                                  explanation_de, explanation_en, active)
    values (p_q->>'topic_id', p_q->>'qtype', p_q->>'prompt_de', p_q->>'prompt_en',
            nullif(p_q->>'image',''), nullif(p_q->>'image_source',''), p_q->'options', p_q->'correct',
            coalesce(p_q->>'explanation_de',''), coalesce(p_q->>'explanation_en',''),
            coalesce((p_q->>'active')::boolean, true))
    returning id into v_id;
  else
    update public.questions set
      topic_id = p_q->>'topic_id', qtype = p_q->>'qtype',
      prompt_de = p_q->>'prompt_de', prompt_en = p_q->>'prompt_en',
      image = nullif(p_q->>'image',''), image_source = nullif(p_q->>'image_source',''), options = p_q->'options', correct = p_q->'correct',
      explanation_de = coalesce(p_q->>'explanation_de',''),
      explanation_en = coalesce(p_q->>'explanation_en',''),
      active = coalesce((p_q->>'active')::boolean, true),
      updated_at = now()
    where id = (p_q->>'id')::int
    returning id into v_id;
  end if;
  return jsonb_build_object('id', v_id);
end $$;

create or replace function public.admin_delete_question(p_token uuid, p_id int)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
begin
  perform public._require_admin(p_token);
  delete from public.questions where id = p_id;
  return '{"ok":true}'::jsonb;
end $$;

create or replace function public.admin_players(p_token uuid)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
begin
  perform public._require_admin(p_token);
  return (select coalesce(jsonb_agg(x order by x.created_at desc), '[]'::jsonb) from (
    select p.id, p.nickname, p.is_admin, p.created_at,
           (select max(score) from public.speed_runs r where r.player_id = p.id and r.in_ranking) as best,
           (select count(*) from public.speed_runs r where r.player_id = p.id) as runs,
           (select count(*) from public.progress g where g.player_id = p.id) as learned
      from public.players p) x);
end $$;

create or replace function public.admin_set_password(p_token uuid, p_player_id bigint, p_new text)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
begin
  perform public._require_admin(p_token);
  if length(coalesce(p_new,'')) < 6 then raise exception 'bad_password' using errcode = 'P0001'; end if;
  update public.players set pw_hash = crypt(p_new, gen_salt('bf', 8)), failed_logins = 0, locked_until = null
   where id = p_player_id;
  delete from public.sessions where player_id = p_player_id;
  return '{"ok":true}'::jsonb;
end $$;

create or replace function public.admin_delete_player(p_token uuid, p_player_id bigint)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
declare me public.players;
begin
  me := public._require_admin(p_token);
  if me.id = p_player_id then raise exception 'cannot_delete_self' using errcode = 'P0001'; end if;
  delete from public.players where id = p_player_id;
  return '{"ok":true}'::jsonb;
end $$;

-- Bestenliste zurücksetzen (z. B. zum Semesterstart). Läufe bleiben für Statistik erhalten.
create or replace function public.admin_reset_ranking(p_token uuid)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
begin
  perform public._require_admin(p_token);
  update public.speed_runs set in_ranking = false where in_ranking;
  return '{"ok":true}'::jsonb;
end $$;

create or replace function public.admin_set_speed_seconds(p_token uuid, p_seconds int)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
begin
  perform public._require_admin(p_token);
  if p_seconds < 15 or p_seconds > 600 then raise exception 'bad_value' using errcode = 'P0001'; end if;
  insert into public.settings (key, value) values ('speed_seconds', to_jsonb(p_seconds))
  on conflict (key) do update set value = excluded.value;
  return '{"ok":true}'::jsonb;
end $$;

-- ---------------------------------------------------------------------
--  Meldungen ("Frage/Antwort falsch?")
-- ---------------------------------------------------------------------
create or replace function public.quiz_report(p_token uuid, p_question_id int, p_reason text, p_comment text, p_lang text)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
declare r public.players;
begin
  r := public._player_from_token(p_token);
  if not exists (select 1 from public.questions where id = p_question_id) then
    raise exception 'unknown_question' using errcode = 'P0001';
  end if;
  -- Spam-Schutz: max. 20 Meldungen pro Spieler und Stunde
  if (select count(*) from public.reports where player_id = r.id and created_at > now() - interval '1 hour') >= 20 then
    raise exception 'too_many_reports' using errcode = 'P0001';
  end if;
  insert into public.reports (question_id, player_id, reason, comment, lang)
  values (p_question_id, r.id,
          case when p_reason in ('answer','question','translation','image','other') then p_reason else 'other' end,
          left(coalesce(p_comment,''), 1000), left(p_lang, 10));
  return '{"ok":true}'::jsonb;
end $$;

create or replace function public.admin_reports(p_token uuid)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
begin
  perform public._require_admin(p_token);
  return (select coalesce(jsonb_agg(x order by x.status, x.created_at desc), '[]'::jsonb) from (
    select rp.id, rp.question_id, rp.reason, rp.comment, rp.lang, rp.status, rp.created_at,
           p.nickname, q.prompt_de, q.topic_id
      from public.reports rp
      left join public.players p on p.id = rp.player_id
      join public.questions q on q.id = rp.question_id) x);
end $$;

create or replace function public.admin_set_report_status(p_token uuid, p_id bigint, p_status text)
returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
begin
  perform public._require_admin(p_token);
  update public.reports set status = p_status where id = p_id;
  return '{"ok":true}'::jsonb;
end $$;

-- Nur für den Keep-alive-Job (hält das kostenlose Projekt aktiv)
create or replace function public.quiz_ping()
returns jsonb
language sql stable security definer set search_path = public, extensions as $$
  select jsonb_build_object('ok', true, 'questions', (select count(*) from public.questions))
$$;

-- ---------------------------------------------------------------------
--  Rechte: Browser (anon) darf nur die öffentlichen Funktionen aufrufen
-- ---------------------------------------------------------------------
revoke execute on all functions in schema public from public, anon, authenticated;

grant execute on function
  public.quiz_register(text,text), public.quiz_login(text,text), public.quiz_logout(uuid),
  public.quiz_me(uuid), public.quiz_change_password(uuid,text,text),
  public.quiz_top(int), public.quiz_topics(),
  public.quiz_learn_next(uuid,text[]), public.quiz_learn_answer(uuid,int,jsonb),
  public.quiz_learn_stats(uuid), public.quiz_learn_reset(uuid),
  public.quiz_speed_start(uuid,text[]), public.quiz_speed_answer(uuid,uuid,int,jsonb),
  public.quiz_speed_finish(uuid,uuid),
  public.admin_questions(uuid), public.admin_save_question(uuid,jsonb),
  public.admin_delete_question(uuid,int), public.admin_players(uuid),
  public.admin_set_password(uuid,bigint,text), public.admin_delete_player(uuid,bigint),
  public.admin_reset_ranking(uuid), public.admin_set_speed_seconds(uuid,int),
  public.quiz_report(uuid,int,text,text,text),
  public.admin_reports(uuid), public.admin_set_report_status(uuid,bigint,text),
  public.quiz_ping()
to anon, authenticated;

-- Themen (Kapitel 02–11 des Skripts)
insert into public.topics (id, sort, name_de, name_en) values
  ('bonded',     2, 'Stoffschlüssige Verbindungen',  'Material-bonded joints'),
  ('formfit',    3, 'Formschlüssige Verbindungen',   'Form-fit joints'),
  ('screws',     4, 'Schraubenverbindungen',         'Screw connections'),
  ('springs',    5, 'Federn',                        'Springs'),
  ('shafts',     6, 'Achsen und Wellen',             'Axles and shafts'),
  ('shafthub',   7, 'Welle-Nabe-Verbindungen',       'Shaft-hub connections'),
  ('bearings',   8, 'Wälzlager',                     'Rolling bearings'),
  ('lubrication',9, 'Schmierung und Dichtungen',     'Lubrication and seals'),
  ('gears',     10, 'Getriebe und Zahnräder',        'Drivetrains and gears'),
  ('couplings', 11, 'Kupplungen und Bremsen',        'Couplings and brakes')
on conflict (id) do update set sort = excluded.sort, name_de = excluded.name_de, name_en = excluded.name_en;
