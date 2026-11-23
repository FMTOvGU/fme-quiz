/* FME-Quiz – Frontend (ohne externe Bibliotheken)
 * Kommuniziert ausschließlich über Supabase-RPC-Funktionen (siehe supabase/01_schema.sql).
 */
(() => {
"use strict";

// ------------------------------------------------------------------ Texte
const T = {
  de: {
    subtitle: "Fundamentals of Machine Elements · FMB · OVGU",
    footer: "Lehrstuhl für Förder- und Materialflusstechnik · Otto-von-Guericke-Universität Magdeburg",
    top5: "Top 5 · Speed-Modus", noScores: "Noch keine Punkte – sei die/der Erste!",
    login: "Anmelden", register: "Registrieren", nickname: "Nickname", password: "Passwort",
    password2: "Passwort wiederholen",
    nickHint: "3–20 Zeichen: Buchstaben, Zahlen, _ . -  · Bitte keinen echten Namen.",
    pwHint: "Mind. 6 Zeichen. Gut merken – es gibt keine E-Mail-Wiederherstellung.",
    pwMismatch: "Die Passwörter stimmen nicht überein.",
    welcome: "Hallo", logout: "Abmelden", admin: "Admin",
    best: "Bestwert", rank: "Platz", none: "–",
    modeSpeed: "Speed", modeSpeedTxt: "{s} Sekunden, so viele Fragen wie möglich. Serien geben Booster!",
    modeLearn: "Learn", modeLearnTxt: "Ohne Zeitlimit, mit Erklärungen. Falsche Fragen kommen öfter wieder.",
    quizLang: "Sprache der Fragen", langDe: "Deutsch", langEn: "English",
    langDeEn: "Deutsch + EN", langDeEnTxt: "Fachbegriffe auf Englisch in Klammern",
    langEnDe: "English + DE", langEnDeTxt: "Technical terms in German in brackets",
    topics: "Themen", all: "Alle", start: "Los geht's",
    learnProgress: "Dein Lernstand", mastered: "sicher", seen: "gesehen", weak: "zuletzt falsch",
    resetLearn: "Lernstand zurücksetzen", resetLearnQ: "Wirklich den gesamten Lernstand löschen?",
    score: "Punkte", streak: "Serie", sec: "s",
    correct: "Richtig!", wrong: "Leider falsch.", solutionIs: "Richtig wäre:",
    next: "Weiter", check: "Prüfen", choose: "– bitte wählen –",
    true: "Wahr", false: "Falsch",
    report: "Melden", reportTitle: "Fehler in der Frage melden",
    reportReason: "Was stimmt nicht?",
    rAnswer: "Die als richtig gewertete Antwort ist falsch", rQuestion: "Die Frage ist falsch oder unklar",
    rTranslation: "Übersetzung / Fachbegriff stimmt nicht", rImage: "Abbildung ist falsch oder unklar", rOther: "Sonstiges",
    reportComment: "Kommentar (optional, z. B. was richtig wäre)", send: "Absenden", cancel: "Abbrechen",
    reportThanks: "Danke! Die Meldung ist beim Lehrstuhl eingegangen.",
    speedNote: "Hinweis: Die Zeit läuft weiter.", source: "Quelle",
    timeUp: "Zeit abgelaufen!", yourScore: "Dein Ergebnis", newBest: "Neuer Bestwert!",
    answered: "beantwortet", correctN: "richtig", bestStreak: "längste Serie",
    again: "Nochmal", menu: "Menü", review: "Fragen dieser Runde", yourAnswer: "Deine Antwort",
    box: "Karteifach", newQ: "Neue Frage",
    learnEnd: "Beenden", noQuestions: "Für diese Auswahl gibt es noch keine Fragen.",
    matchHint: "Wähle zu jedem Begriff links die passende Beschreibung.",
    typeImg: "Bild", typeMc: "Auswahl", typeTf: "Wahr/Falsch", typeMatch: "Zuordnen",
    errors: {
      bad_nickname: "Nickname: 3–20 Zeichen (Buchstaben, Zahlen, _ . -).",
      bad_password: "Passwort: mindestens 6 Zeichen.",
      nickname_taken: "Dieser Nickname ist schon vergeben.",
      login_failed: "Nickname oder Passwort falsch.",
      locked: "Zu viele Fehlversuche – bitte 5 Minuten warten.",
      not_logged_in: "Bitte erneut anmelden.",
      no_questions: "Für diese Auswahl gibt es noch keine Fragen.",
      too_many_reports: "Zu viele Meldungen – bitte später erneut versuchen.",
      not_admin: "Keine Admin-Rechte.",
      network: "Keine Verbindung zum Server. Bitte später erneut versuchen.",
      config: "Die Plattform ist noch nicht eingerichtet (config.js).",
      generic: "Es ist ein Fehler aufgetreten."
    }
  },
  en: {
    subtitle: "Fundamentals of Machine Elements · FMB · OVGU",
    footer: "Chair of Material Handling · Otto von Guericke University Magdeburg",
    top5: "Top 5 · Speed mode", noScores: "No scores yet – be the first!",
    login: "Log in", register: "Sign up", nickname: "Nickname", password: "Password",
    password2: "Repeat password",
    nickHint: "3–20 characters: letters, digits, _ . -  · Please don't use your real name.",
    pwHint: "At least 6 characters. Remember it – there is no e-mail recovery.",
    pwMismatch: "The passwords do not match.",
    welcome: "Hi", logout: "Log out", admin: "Admin",
    best: "Best score", rank: "Rank", none: "–",
    modeSpeed: "Speed", modeSpeedTxt: "{s} seconds, answer as many as you can. Streaks give boosters!",
    modeLearn: "Learn", modeLearnTxt: "No time limit, with explanations. Wrong answers come back more often.",
    quizLang: "Question language", langDe: "Deutsch", langEn: "English",
    langDeEn: "Deutsch + EN", langDeEnTxt: "Fachbegriffe auf Englisch in Klammern",
    langEnDe: "English + DE", langEnDeTxt: "Technical terms in German in brackets",
    topics: "Topics", all: "All", start: "Let's go",
    learnProgress: "Your progress", mastered: "mastered", seen: "seen", weak: "recently wrong",
    resetLearn: "Reset progress", resetLearnQ: "Really delete all your learning progress?",
    score: "Points", streak: "Streak", sec: "s",
    correct: "Correct!", wrong: "Not quite.", solutionIs: "Correct answer:",
    next: "Next", check: "Check", choose: "– please choose –",
    true: "True", false: "False",
    report: "Report", reportTitle: "Report a problem with this question",
    reportReason: "What is wrong?",
    rAnswer: "The answer marked as correct is wrong", rQuestion: "The question is wrong or unclear",
    rTranslation: "Translation / technical term is wrong", rImage: "Figure is wrong or unclear", rOther: "Other",
    reportComment: "Comment (optional, e.g. what would be correct)", send: "Send", cancel: "Cancel",
    reportThanks: "Thanks! Your report has been sent to the chair.",
    speedNote: "Note: the timer keeps running.", source: "Source",
    timeUp: "Time's up!", yourScore: "Your result", newBest: "New personal best!",
    answered: "answered", correctN: "correct", bestStreak: "best streak",
    again: "Play again", menu: "Menu", review: "Questions of this round", yourAnswer: "Your answer",
    box: "Box", newQ: "New question",
    learnEnd: "Finish", noQuestions: "There are no questions for this selection yet.",
    matchHint: "Pick the matching description for each term on the left.",
    typeImg: "Image", typeMc: "Choice", typeTf: "True/False", typeMatch: "Matching",
    errors: {
      bad_nickname: "Nickname: 3–20 characters (letters, digits, _ . -).",
      bad_password: "Password: at least 6 characters.",
      nickname_taken: "This nickname is already taken.",
      login_failed: "Wrong nickname or password.",
      locked: "Too many failed attempts – please wait 5 minutes.",
      not_logged_in: "Please log in again.",
      no_questions: "There are no questions for this selection yet.",
      too_many_reports: "Too many reports – please try again later.",
      not_admin: "No admin rights.",
      network: "Cannot reach the server. Please try again later.",
      config: "The platform is not configured yet (config.js).",
      generic: "Something went wrong."
    }
  }
};

// ------------------------------------------------------------------ Zustand
const store = {
  get(k, d) { try { const v = localStorage.getItem("fmeq_" + k); return v === null ? d : JSON.parse(v); } catch { return d; } },
  set(k, v) { try { localStorage.setItem("fmeq_" + k, JSON.stringify(v)); } catch { /* egal */ } },
  del(k) { try { localStorage.removeItem("fmeq_" + k); } catch { /* egal */ } }
};
const S = {
  ui: store.get("ui", (navigator.language || "de").startsWith("de") ? "de" : "en"),
  session: store.get("session", null),         // {token, nickname, is_admin}
  mode: store.get("mode", "speed"),
  lang: store.get("lang", "de"),               // de | en | de+en | en+de
  topics: store.get("topics", []),             // [] = alle
  topicList: [],
  speedSeconds: 60,
};
const t = (k) => (T[S.quiz || S.ui][k] ?? T.de[k] ?? k);
const app = document.getElementById("app");
const CFG = window.QUIZ_CONFIG || {};

// ------------------------------------------------------------------ Server
class ApiError extends Error { constructor(code) { super(code); this.code = code; } }
async function rpc(fn, args = {}) {
  if (!CFG.supabaseUrl || CFG.supabaseUrl.includes("DEIN-PROJEKT")) throw new ApiError("config");
  const headers = { "apikey": CFG.supabaseKey, "Content-Type": "application/json" };
  if ((CFG.supabaseKey || "").startsWith("eyJ")) headers.Authorization = "Bearer " + CFG.supabaseKey;
  let res;
  try {
    res = await fetch(CFG.supabaseUrl.replace(/\/$/, "") + "/rest/v1/rpc/" + fn, {
      method: "POST", headers, body: JSON.stringify(args)
    });
  } catch { throw new ApiError("network"); }
  const txt = await res.text();
  let data = null; try { data = txt ? JSON.parse(txt) : null; } catch { data = txt; }
  if (!res.ok) {
    const code = (data && data.message) || "generic";
    if (code === "not_logged_in") { logoutLocal(); }
    throw new ApiError(code);
  }
  return data;
}
const errText = (e) => (T[S.quiz || S.ui].errors[e && e.code] || T[S.ui].errors.generic);
const tok = () => S.session && S.session.token;

// ------------------------------------------------------------------ Hilfen
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const MARK = /\{\{([^|}]+)\|([^}]+)\}\}([A-Za-zÄÖÜäöüß]*)/g;
/** Fachbegriff-Markierung {{a|b}} je nach Sprachmodus darstellen */
function fmt(text, mode) {
  const combined = mode === "de+en" || mode === "en+de";
  return esc(text).replace(MARK, (_, a, b, suf) =>
    combined ? `<b>${a}${suf}</b> <span class="muted">(${b})</span>` : `${a}${suf}`);
}
const baseLang = (mode) => (mode.startsWith("en") ? "en" : "de");
const qText = (q, field, mode) => fmt(q[field + "_" + baseLang(mode)] ?? q[field + "_de"], mode);
const optText = (o, mode) => fmt(o[baseLang(mode)] ?? o.de, mode);
function shuffle(a) { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
function toast(msg, ms = 2600) {
  const el = document.createElement("div"); el.className = "toast"; el.textContent = msg;
  document.body.appendChild(el); setTimeout(() => el.remove(), ms);
}
const topicName = (id) => { const x = S.topicList.find((z) => z.id === id); return x ? x["name_" + (S.quiz || S.ui)] : id; };
const typeName = (ty) => t({ img: "typeImg", mc: "typeMc", tf: "typeTf", match: "typeMatch" }[ty]);
const $ = (sel, root = app) => root.querySelector(sel);
const $$ = (sel, root = app) => Array.from(root.querySelectorAll(sel));

function setUiLang(l) {
  S.ui = l; store.set("ui", l);
  document.documentElement.lang = l;
  document.querySelectorAll("[data-ui]").forEach((b) => b.classList.toggle("on", b.dataset.ui === l));
  document.querySelectorAll("[data-t]").forEach((el) => { el.textContent = t(el.dataset.t); });
  if (current.rerender) current.rerender();
}
document.querySelectorAll("[data-ui]").forEach((b) => b.addEventListener("click", () => setUiLang(b.dataset.ui)));

// einfache Navigation (Zurück-Taste des Handys führt ins Menü)
const current = { name: "", rerender: null, cleanup: null };
function show(name, render) {
  app.className = name;
  if (!["speed", "learn", "result"].includes(name)) S.quiz = null;
  if (current.cleanup) { try { current.cleanup(); } catch { /* egal */ } }
  current.name = name; current.cleanup = null; current.rerender = null;
  render();
  window.scrollTo(0, 0);
  if (name !== "login" && name !== "home" && history.state?.screen !== name) history.pushState({ screen: name }, "");
}
window.addEventListener("popstate", () => { if (current.name !== "home" && current.name !== "login") start(); });

// ------------------------------------------------------------------ Top 5
async function loadTop() {
  try { return await rpc("quiz_top", { p_limit: 5 }); } catch { return null; }
}
function top5Html(list) {
  if (!list) return `<p class="muted">${esc(t("errors").network || "")}</p>`;
  if (!list.length) return `<p class="muted">${t("noScores")}</p>`;
  const me = S.session && S.session.nickname.toLowerCase();
  return `<ol class="top5">${list.map((r, i) => `
    <li class="${r.nickname.toLowerCase() === me ? "me" : ""}"><span class="pos">${i + 1}</span>
      <span class="nick">${esc(r.nickname)}</span><span class="pts">${r.score}</span></li>`).join("")}</ol>`;
}

// ------------------------------------------------------------------ Login
function logoutLocal() { S.session = null; store.del("session"); }
function viewLogin(tab = "login") {
  show("login", () => {
    const render = (topList) => {
      app.innerHTML = `
        <section class="card"><h2>🏆 ${t("top5")}</h2><div id="top">${topList === undefined ? '<p class="muted">…</p>' : top5Html(topList)}</div></section>
        <section class="card">
          <div class="tabs"><button data-tab="login" class="${tab === "login" ? "on" : ""}">${t("login")}</button>
            <button data-tab="register" class="${tab === "register" ? "on" : ""}">${t("register")}</button></div>
          <form id="f" autocomplete="on">
            <label class="field"><span>${t("nickname")}</span>
              <input type="text" name="nick" autocomplete="username" autocapitalize="off" autocorrect="off" spellcheck="false" maxlength="20" required></label>
            <label class="field"><span>${t("password")}</span>
              <input type="password" name="pw" autocomplete="${tab === "login" ? "current-password" : "new-password"}" required></label>
            ${tab === "register" ? `<label class="field"><span>${t("password2")}</span>
              <input type="password" name="pw2" autocomplete="new-password" required></label>
              <p class="muted small">${t("nickHint")}<br>${t("pwHint")}</p>` : ""}
            <div class="err" id="err"></div>
            <button class="btn block" type="submit">${tab === "login" ? t("login") : t("register")}</button>
          </form>
        </section>`;
      $$("[data-tab]").forEach((b) => b.addEventListener("click", () => { tab = b.dataset.tab; render(topList); }));
      $("#f").addEventListener("submit", async (ev) => {
        ev.preventDefault();
        const f = ev.target, err = $("#err"), btn = f.querySelector("button[type=submit]");
        err.textContent = "";
        if (tab === "register" && f.pw.value !== f.pw2.value) { err.textContent = t("pwMismatch"); return; }
        btn.disabled = true;
        try {
          const r = await rpc(tab === "login" ? "quiz_login" : "quiz_register", { p_nickname: f.nick.value.trim(), p_password: f.pw.value });
          S.session = r; store.set("session", r);
          viewHome();
        } catch (e) { err.textContent = errText(e); btn.disabled = false; }
      });
    };
    current.rerender = () => render(lastTop);
    let lastTop;
    render(undefined);
    loadTop().then((l) => { lastTop = l; if (current.name === "login") { const el = $("#top"); if (el) el.innerHTML = top5Html(l); } });
  });
}

// ------------------------------------------------------------------ Startseite
async function viewHome() {
  show("home", () => { app.innerHTML = `<p class="muted center">…</p>`; });
  let me, top, stats;
  try {
    [me, top, S.topicList, stats] = await Promise.all([
      rpc("quiz_me", { p_token: tok() }), loadTop(), rpc("quiz_topics"), rpc("quiz_learn_stats", { p_token: tok() })
    ]);
  } catch (e) {
    if (!S.session) return viewLogin();
    app.innerHTML = `<div class="card"><p class="err">${errText(e)}</p><button class="btn" id="retry">↻</button></div>`;
    $("#retry").onclick = viewHome; return;
  }
  S.session.is_admin = me.is_admin; store.set("session", S.session);
  if (me.speed_seconds) S.speedSeconds = me.speed_seconds;
  // nicht mehr vorhandene Themen aus Auswahl entfernen
  S.topics = S.topics.filter((id) => S.topicList.some((x) => x.id === id && x.count > 0));

  const render = () => {
    if (S.mode === "speed" && S.lang.includes("+")) S.lang = baseLang(S.lang);
    const countKey = S.mode === "speed" ? "speed_count" : "count";
    const langs = [["de", t("langDe")], ["en", t("langEn")]];
    if (S.mode === "learn") langs.push(["de+en", t("langDeEn"), t("langDeEnTxt")], ["en+de", t("langEnDe"), t("langEnDeTxt")]);
    const statRows = (stats || []).filter((s) => s.total > 0);
    app.innerHTML = `
      <section class="card">
        <div class="row"><h2 style="margin:0">${t("welcome")}, ${esc(S.session.nickname)} 👋</h2><span class="spacer"></span>
          ${me.is_admin ? `<button class="ghost" id="adm">${t("admin")}</button>` : ""}
          <button class="ghost" id="out">${t("logout")}</button></div>
        <div class="stats" style="margin-top:12px">
          <div class="stat"><b>${me.best ?? t("none")}</b><span>${t("best")}</span></div>
          <div class="stat"><b>${me.rank ? "#" + me.rank : t("none")}</b><span>${t("rank")}</span></div>
        </div>
      </section>

      <div class="modes">
        <button class="mode ${S.mode === "speed" ? "on" : ""}" data-mode="speed"><span class="ic">⚡</span><b>${t("modeSpeed")}</b>
          <span>${t("modeSpeedTxt").replace("{s}", S.speedSeconds)}</span></button>
        <button class="mode ${S.mode === "learn" ? "on" : ""}" data-mode="learn"><span class="ic">📘</span><b>${t("modeLearn")}</b>
          <span>${t("modeLearnTxt")}</span></button>
      </div>

      <section class="card">
        <h3>${t("quizLang")}</h3>
        <div class="seg">${langs.map(([k, l, s]) => `<button data-lang="${k}" class="${S.lang === k ? "on" : ""}">${l}${s ? `<small>${s}</small>` : ""}</button>`).join("")}</div>
        <h3 style="margin-top:16px">${t("topics")}</h3>
        <div class="chips">
          <button class="chip ${S.topics.length === 0 ? "on" : ""}" data-topic="">${t("all")}</button>
          ${S.topicList.filter((x) => x[countKey] > 0).map((x) => `<button class="chip ${S.topics.includes(x.id) ? "on" : ""}" data-topic="${x.id}">
             ${esc(x["name_" + S.ui])}<span class="n">(${x[countKey]})</span></button>`).join("")}
        </div>
        <div class="err" id="err"></div>
        <button class="btn block" id="go" style="margin-top:6px">${S.mode === "speed" ? "⚡" : "📘"} ${t("start")}</button>
      </section>

      ${S.mode === "learn" && statRows.length ? `<section class="card progress-list"><h3>${t("learnProgress")}</h3>
        ${statRows.map((s) => `<div class="pl"><div class="row small"><span>${esc(topicName(s.topic))}</span><span class="spacer"></span>
          <span class="muted">${s.mastered}/${s.total} ${t("mastered")}</span></div>
          <div class="bar"><i class="m" style="width:${100 * s.mastered / s.total}%"></i><i class="s" style="width:${100 * (s.seen - s.mastered - s.weak) / s.total}%"></i><i class="w" style="width:${100 * s.weak / s.total}%"></i></div></div>`).join("")}
        <p class="muted small" style="margin:8px 0 0">■ <span style="color:var(--fmb)">${t("mastered")}</span> · ■ <span style="color:var(--fmb-2)">${t("seen")}</span> · ■ <span style="color:#e57f87">${t("weak")}</span></p>
        <button class="linkbtn small" id="resetLearn">${t("resetLearn")}</button></section>` : ""}

      <section class="card"><h2>🏆 ${t("top5")}</h2>${top5Html(top)}</section>`;

    $$("[data-mode]").forEach((b) => b.onclick = () => { S.mode = b.dataset.mode; store.set("mode", S.mode); render(); });
    $$("[data-lang]").forEach((b) => b.onclick = () => { S.lang = b.dataset.lang; store.set("lang", S.lang); render(); });
    $$("[data-topic]").forEach((b) => b.onclick = () => {
      const id = b.dataset.topic;
      if (!id) S.topics = [];
      else S.topics = S.topics.includes(id) ? S.topics.filter((x) => x !== id) : [...S.topics, id];
      store.set("topics", S.topics); render();
    });
    $("#out").onclick = async () => { try { await rpc("quiz_logout", { p_token: tok() }); } catch { /* egal */ } logoutLocal(); viewLogin(); };
    if ($("#adm")) $("#adm").onclick = () => viewAdmin();
    if ($("#resetLearn")) $("#resetLearn").onclick = async () => {
      if (!confirm(t("resetLearnQ"))) return;
      await rpc("quiz_learn_reset", { p_token: tok() }); stats = await rpc("quiz_learn_stats", { p_token: tok() }); render();
    };
    $("#go").onclick = () => (S.mode === "speed" ? playSpeed() : playLearn());
  };
  current.rerender = render;
  render();
}

// ------------------------------------------------------------------ Fragen darstellen
/** Baut die Fragekarte. onAnswer(answer) wird mit der Antwort (Originalindex/Bool/Array) aufgerufen. */
function questionHtml(q, mode, extraTop = "") {
  const img = q.image ? `<figure class="qimg"><img src="${esc(q.image)}" alt="">${q.image_source ? `<figcaption>${t("source")}: ${esc(q.image_source)}</figcaption>` : ""}</figure>` : "";
  let body = "";
  if (q.type === "mc" || q.type === "img") {
    q._order = shuffle(q.options.map((_, i) => i));
    body = `<div class="opts">${q._order.map((oi, k) => `<button class="opt" data-a="${oi}"><span class="k">${"ABCDEFGH"[k]}</span><span>${optText(q.options[oi], mode)}</span></button>`).join("")}</div>`;
  } else if (q.type === "tf") {
    body = `<div class="opts tf"><button class="opt" data-a="true">✓ ${t("true")}</button><button class="opt" data-a="false">✗ ${t("false")}</button></div>`;
  } else if (q.type === "match") {
    const right = q.options.right.map((o, i) => ({ o, i }));
    q._rorder = shuffle(right.map((x) => x.i));
    body = `<p class="muted small">${t("matchHint")}</p>
      ${q.options.left.map((l, li) => `<div class="match-row"><div class="l">${optText(l, mode)}</div>
        <select data-li="${li}"><option value="">${t("choose")}</option>
          ${q._rorder.map((ri) => `<option value="${ri}">${optText(q.options.right[ri], mode).replace(/<[^>]+>/g, "")}</option>`).join("")}
        </select><div class="sol hidden"></div></div>`).join("")}
      <button class="btn block" id="checkMatch" style="margin-top:12px">${t("check")}</button>`;
  }
  return `<article class="card qcard">
    <div class="qmeta"><span class="tag topic">${esc(topicName(q.topic))}</span><span class="tag">${typeName(q.type)}</span>${extraTop}
      <button class="flag" id="flag" title="${t("report")}">⚑ ${t("report")}</button></div>
    ${img}<p class="prompt">${qText(q, "prompt", mode)}</p>${body}<div id="fb"></div></article>`;
}
function bindAnswer(q, onAnswer) {
  $$(".opt[data-a]").forEach((b) => b.onclick = () => {
    $$(".opt[data-a]").forEach((x) => (x.disabled = true));
    const v = b.dataset.a; b.dataset.picked = "1";
    onAnswer(v === "true" ? true : v === "false" ? false : Number(v));
  });
  const cm = $("#checkMatch");
  if (cm) cm.onclick = () => {
    const sels = $$("select[data-li]");
    if (sels.some((s) => s.value === "")) { sels.filter((s) => !s.value)[0].focus(); return; }
    cm.disabled = true; sels.forEach((s) => (s.disabled = true));
    onAnswer(sels.map((s) => Number(s.value)));
  };
}
/** Lösung farbig markieren */
function showSolution(q, answer, solution, mode) {
  if (q.type === "mc" || q.type === "img" || q.type === "tf") {
    $$(".opt[data-a]").forEach((b) => {
      const v = b.dataset.a === "true" ? true : b.dataset.a === "false" ? false : Number(b.dataset.a);
      if (v === solution) b.classList.add("ok");
      else if (v === answer) b.classList.add("bad");
    });
  } else if (q.type === "match") {
    $$("select[data-li]").forEach((s) => {
      const li = Number(s.dataset.li), ok = Number(s.value) === li;
      s.classList.add(ok ? "ok" : "bad");
      if (!ok) { const d = s.parentElement.querySelector(".sol"); d.classList.remove("hidden"); d.innerHTML = "✓ " + optText(q.options.right[li], mode); }
    });
  }
}
function solutionText(q, solution, mode) {
  if (q.type === "tf") return solution ? t("true") : t("false");
  if (q.type === "match") return q.options.left.map((l, i) => optText(l, mode) + " → " + optText(q.options.right[i], mode)).join("<br>");
  return optText(q.options[solution], mode);
}
function answerText(q, a, mode) {
  if (a === undefined || a === null) return "–";
  if (q.type === "tf") return a ? t("true") : t("false");
  if (q.type === "match") return "…";
  return optText(q.options[a], mode);
}

// ------------------------------------------------------------------ Melden
function openReport(q, mode, note = "") {
  const m = document.createElement("div");
  m.className = "modal";
  const reasons = [["answer", "rAnswer"], ["question", "rQuestion"], ["translation", "rTranslation"], ["image", "rImage"], ["other", "rOther"]]
    .filter(([k]) => k !== "image" || q.image);
  m.innerHTML = `<div class="sheet" role="dialog" aria-modal="true">
    <h2 style="margin-top:0">⚑ ${t("reportTitle")}</h2>
    ${note ? `<p class="muted small">${note}</p>` : ""}
    <p class="small" style="background:var(--fmb-3);padding:8px 10px;border-radius:8px">${qText(q, "prompt", mode)}</p>
    <h3>${t("reportReason")}</h3>
    <div class="radio-list">${reasons.map(([k, l], i) => `<label><input type="radio" name="r" value="${k}" ${i === 0 ? "checked" : ""}> ${t(l)}</label>`).join("")}</div>
    <label class="field" style="margin-top:12px"><span>${t("reportComment")}</span><textarea id="rc" maxlength="1000"></textarea></label>
    <div class="err" id="rerr"></div>
    <div class="row"><button class="btn secondary" id="rcancel" style="flex:1">${t("cancel")}</button>
      <button class="btn" id="rsend" style="flex:1">${t("send")}</button></div></div>`;
  document.body.appendChild(m);
  const close = () => m.remove();
  m.addEventListener("click", (e) => { if (e.target === m) close(); });
  m.querySelector("#rcancel").onclick = close;
  m.querySelector("#rsend").onclick = async (e) => {
    e.target.disabled = true;
    try {
      await rpc("quiz_report", { p_token: tok(), p_question_id: q.id, p_reason: m.querySelector("input[name=r]:checked").value,
        p_comment: m.querySelector("#rc").value, p_lang: mode });
      close(); toast(t("reportThanks"));
    } catch (err) { m.querySelector("#rerr").textContent = errText(err); e.target.disabled = false; }
  };
}

// ------------------------------------------------------------------ Speed-Modus
async function playSpeed() {
  const mode = baseLang(S.lang);
  let run, q, endAt, timer, busy = false, done = false;
  const st = { score: 0, streak: 0, review: [] };
  try {
    const r = await rpc("quiz_speed_start", { p_token: tok(), p_topics: S.topics });
    run = r.run; q = r.question; endAt = performance.now() + r.time_left_ms; S.speedSeconds = r.seconds;
  } catch (e) { const el = $("#err"); if (el) el.textContent = errText(e); else toast(errText(e)); return; }
  S.quiz = mode;

  show("speed", () => {
    app.innerHTML = `<div class="hud"><div class="row">
        <div><div class="muted small">${t("score")}</div><div class="score" id="sc">0</div></div>
        <span id="boost" class="boost">🔥 ×1</span>
        <div class="secs" id="secs">${S.speedSeconds}</div></div>
        <div class="timer" id="tbar"><i></i></div></div><div id="qwrap"></div>`;
  });
  const total = S.speedSeconds * 1000;
  const tick = () => {
    const left = Math.max(0, endAt - performance.now());
    const bar = $("#tbar"); if (!bar) return;
    bar.firstElementChild.style.width = (100 * left / total) + "%";
    bar.classList.toggle("low", left < 10000);
    $("#secs").textContent = Math.ceil(left / 1000);
    if (left <= 0 && !busy) finish();
  };
  timer = setInterval(tick, 100);
  current.cleanup = () => { clearInterval(timer); if (!done) rpc("quiz_speed_finish", { p_token: tok(), p_run: run }).catch(() => {}); };

  const boostEl = () => $("#boost");
  const updHud = (mult) => {
    $("#sc").textContent = st.score;
    const b = boostEl(); b.className = "boost" + (mult >= 3 ? " x3" : mult >= 2 ? " x2" : "");
    b.textContent = `🔥 ${st.streak} · ×${mult}`;
  };
  const pop = (txt) => { const p = document.createElement("div"); p.className = "pop"; p.textContent = txt; document.body.appendChild(p); setTimeout(() => p.remove(), 850); };
  const flash = (ok) => { const f = document.createElement("div"); f.className = "flash"; document.body.appendChild(f);
    requestAnimationFrame(() => f.classList.add(ok ? "ok" : "bad")); setTimeout(() => f.remove(), 350); };

  const renderQ = () => {
    $("#qwrap").innerHTML = questionHtml(q, mode);
    const thisQ = q;
    $("#flag").onclick = () => openReport(thisQ, mode, t("speedNote"));
    bindAnswer(q, async (answer) => {
      busy = true;
      let r;
      try { r = await rpc("quiz_speed_answer", { p_token: tok(), p_run: run, p_question_id: q.id, p_answer: answer }); }
      catch (e) { busy = false; toast(errText(e)); return finish(); }
      st.review.push({ q: thisQ, answer, correct: r.correct, solution: r.solution });
      if (r.finished && r.correct === undefined) { busy = false; return finish(); }
      showSolution(thisQ, answer, r.solution, mode);
      flash(r.correct);
      const prevMult = st.streak >= 5 ? 3 : st.streak >= 3 ? 2 : 1;
      st.score = r.score; st.streak = r.streak;
      updHud(r.multiplier || 1);
      if (r.correct) pop(`+${r.points}`);
      if (r.correct && r.multiplier > prevMult) setTimeout(() => pop(`BOOST ×${r.multiplier}!`), 300);
      endAt = performance.now() + r.time_left_ms;
      setTimeout(() => {
        busy = false;
        if (r.finished || !r.question) return finish();
        q = r.question; renderQ();
        if (endAt - performance.now() <= 0) finish();
      }, r.correct ? 450 : 1100);
    });
  };
  renderQ(); updHud(1);

  async function finish() {
    if (done) return; done = true; clearInterval(timer);
    let res;
    try { res = await rpc("quiz_speed_finish", { p_token: tok(), p_run: run }); } catch { res = { score: st.score }; }
    const top = await loadTop();
    show("result", () => {
      const render = () => {
        app.innerHTML = `
          <section class="card center"><h2>⏱ ${t("timeUp")}</h2>
            <div class="muted">${t("yourScore")}</div><div class="big-score">${res.score}</div>
            ${res.new_best ? `<span class="badge-new">🏅 ${t("newBest")}</span>` : ""}
            <div class="stats" style="margin-top:14px">
              <div class="stat"><b>${res.n_correct ?? "–"}/${res.answered ?? "–"}</b><span>${t("correctN")}</span></div>
              <div class="stat"><b>${res.best_streak ?? "–"}</b><span>${t("bestStreak")}</span></div>
              <div class="stat"><b>${res.rank ? "#" + res.rank : "–"}</b><span>${t("rank")}</span></div></div>
            <div class="row" style="margin-top:14px"><button class="btn secondary" id="menu" style="flex:1">${t("menu")}</button>
              <button class="btn" id="again" style="flex:1">⚡ ${t("again")}</button></div></section>
          <section class="card"><h2>🏆 ${t("top5")}</h2>${top5Html(top)}</section>
          ${st.review.length ? `<section class="card"><h3>${t("review")}</h3><ul class="review">${st.review.map((x, i) => `
            <li><div class="row"><span class="${x.correct ? "r-ok" : "r-bad"}">${x.correct ? "✓" : "✗"}</span>
              <span class="small" style="flex:1">${qText(x.q, "prompt", mode)}</span>
              <button class="flag" data-rep="${i}">⚑</button></div>
              ${x.correct ? "" : `<div class="small muted">${t("yourAnswer")}: ${answerText(x.q, x.answer, mode)}</div>`}
              <div class="small"><b>${t("solutionIs")}</b> ${solutionText(x.q, x.solution, mode)}</div></li>`).join("")}</ul></section>` : ""}`;
        $("#menu").onclick = () => viewHome();
        $("#again").onclick = () => playSpeed();
        $$("[data-rep]").forEach((b) => b.onclick = () => openReport(st.review[Number(b.dataset.rep)].q, mode));
      };
      current.rerender = render; render();
    });
  }
}

// ------------------------------------------------------------------ Learn-Modus
async function playLearn() {
  const mode = S.lang;
  S.quiz = baseLang(mode);
  let count = 0;
  const next = async () => {
    let r;
    try { r = await rpc("quiz_learn_next", { p_token: tok(), p_topics: S.topics }); }
    catch (e) { toast(errText(e)); return viewHome(); }
    if (!r.question) { toast(t("noQuestions")); return viewHome(); }
    const q = r.question; count++;
    show("learn", () => {
      const boxHtml = (b) => `<span class="box-ind" title="${t("box")}">${[1, 2, 3, 4, 5].map((i) => `<i class="${b !== null && b !== undefined && b >= i ? "on" : ""}"></i>`).join("")}</span>`;
      app.innerHTML = `<div class="row" style="margin-bottom:10px"><button class="ghost" id="end">← ${t("learnEnd")}</button><span class="spacer"></span>
        <span class="muted small">#${count} · ${r.box === null || r.box === undefined ? t("newQ") : t("box") + " " + r.box + "/5"}</span></div>
        ${questionHtml(q, mode)}
        <div class="sticky-actions hidden" id="nextWrap"><button class="btn block" id="next">${t("next")} →</button></div>`;
      $("#end").onclick = () => viewHome();
      $("#flag").onclick = () => openReport(q, mode);
      bindAnswer(q, async (answer) => {
        let a;
        try { a = await rpc("quiz_learn_answer", { p_token: tok(), p_question_id: q.id, p_answer: answer }); }
        catch (e) { toast(errText(e)); return; }
        showSolution(q, answer, a.solution, mode);
        const ex = a["explanation_" + baseLang(mode)] || a.explanation_de;
        $("#fb").innerHTML = `<div class="feedback ${a.correct ? "ok" : "bad"}">
          <b>${a.correct ? "✓ " + t("correct") : "✗ " + t("wrong")}</b>
          ${!a.correct && q.type !== "match" ? `<div class="small"><b>${t("solutionIs")}</b> ${solutionText(q, a.solution, mode)}</div>` : ""}
          ${ex ? `<div style="margin-top:6px">${fmt(ex, mode)}</div>` : ""}
          <div class="box-ind small muted">${t("box")} ${a.box}/5 ${boxHtml(a.box)}</div></div>`;
        $("#nextWrap").classList.remove("hidden");
        $("#next").onclick = next;
        $("#next").focus({ preventScroll: true });
        $("#fb").scrollIntoView({ behavior: "smooth", block: "nearest" });
      });
    });
  };
  next();
}

// ------------------------------------------------------------------ Admin
async function viewAdmin(tab = "reports") {
  let data;
  show("admin", () => { app.innerHTML = `<p class="muted center">…</p>`; });
  try {
    if (tab === "reports") data = await rpc("admin_reports", { p_token: tok() });
    if (tab === "questions") data = await rpc("admin_questions", { p_token: tok() });
    if (tab === "players") data = await rpc("admin_players", { p_token: tok() });
  } catch (e) { app.innerHTML = `<div class="card err">${errText(e)}</div>`; return; }
  const head = `<div class="row" style="margin-bottom:10px"><button class="ghost" id="back">← ${t("menu")}</button><b style="margin-left:6px">Admin</b></div>
    <div class="tabs">${[["reports", "Meldungen"], ["questions", "Fragen"], ["players", "Spieler"], ["settings", "Einstellungen"]]
      .map(([k, l]) => `<button data-at="${k}" class="${tab === k ? "on" : ""}">${l}</button>`).join("")}</div>`;
  const bindHead = () => { $("#back").onclick = () => viewHome(); $$("[data-at]").forEach((b) => b.onclick = () => viewAdmin(b.dataset.at)); };

  if (tab === "reports") {
    const open = data.filter((r) => r.status === "open").length;
    const reasonDe = { answer: "Antwort falsch", question: "Frage falsch/unklar", translation: "Übersetzung", image: "Abbildung", other: "Sonstiges" };
    app.innerHTML = head + `<section class="card admin-list"><h3>${open} offene Meldung(en)</h3>
      ${data.length ? data.map((r) => `<div class="item">
        <div class="row wrap"><span class="pill ${r.status === "open" ? "open" : "off"}">${r.status === "open" ? "offen" : "erledigt"}</span>
          <span class="pill">${esc(topicName(r.topic_id))} · #${r.question_id}</span><span class="pill">${reasonDe[r.reason] || r.reason}</span>
          <span class="muted small">${new Date(r.created_at).toLocaleString("de-DE")} · ${esc(r.nickname || "?")} · ${esc(r.lang || "")}</span></div>
        <div class="small" style="margin:6px 0">${fmt(r.prompt_de, "de")}</div>
        ${r.comment ? `<div class="small" style="background:#fff8e6;padding:6px 8px;border-radius:8px">💬 ${esc(r.comment)}</div>` : ""}
        <div class="row" style="margin-top:6px"><button class="ghost" data-edit="${r.question_id}">Frage bearbeiten</button>
          <button class="ghost" data-st="${r.id}" data-to="${r.status === "open" ? "done" : "open"}">${r.status === "open" ? "✓ erledigt" : "wieder öffnen"}</button></div></div>`).join("")
        : `<p class="muted">Keine Meldungen.</p>`}</section>`;
    bindHead();
    $$("[data-st]").forEach((b) => b.onclick = async () => { await rpc("admin_set_report_status", { p_token: tok(), p_id: Number(b.dataset.st), p_status: b.dataset.to }); viewAdmin("reports"); });
    $$("[data-edit]").forEach((b) => b.onclick = async () => {
      const qs = await rpc("admin_questions", { p_token: tok() });
      const q = qs.find((x) => x.id === Number(b.dataset.edit)); if (q) editQuestion(q, "reports");
    });
  }

  if (tab === "questions") {
    let filter = store.get("admTopic", ""), search = "";
    const render = () => {
      const list = data.filter((q) => (!filter || q.topic_id === filter) &&
        (!search || (q.prompt_de + " " + q.prompt_en).toLowerCase().includes(search.toLowerCase())));
      app.innerHTML = head + `<section class="card">
        <div class="row wrap"><select id="ft" style="flex:1;min-width:160px"><option value="">Alle Themen (${data.length})</option>
          ${S.topicList.map((x) => `<option value="${x.id}" ${filter === x.id ? "selected" : ""}>${esc(x.name_de)} (${data.filter((q) => q.topic_id === x.id).length})</option>`).join("")}</select>
          <button class="btn" id="new">+ Neue Frage</button></div>
        <input type="text" id="fs" placeholder="Suchen …" value="${esc(search)}" style="margin-top:10px">
        <div class="admin-list" style="margin-top:8px">${list.map((q) => `<div class="item row" data-q="${q.id}" style="cursor:pointer">
          <span class="pill ${q.active ? "" : "off"}">#${q.id} ${typeName(q.qtype)}</span>
          <span class="small" style="flex:1">${fmt(q.prompt_de, "de")}</span><span>›</span></div>`).join("")}</div></section>`;
      bindHead();
      $("#ft").onchange = (e) => { filter = e.target.value; store.set("admTopic", filter); render(); };
      $("#fs").oninput = (e) => { search = e.target.value; const pos = e.target.selectionStart; render(); const f = $("#fs"); f.focus(); f.setSelectionRange(pos, pos); };
      $("#new").onclick = () => editQuestion({ topic_id: filter || S.topicList[0].id, qtype: "mc", prompt_de: "", prompt_en: "", image: "",
        options: [{ de: "", en: "" }, { de: "", en: "" }, { de: "", en: "" }, { de: "", en: "" }], correct: 0, explanation_de: "", explanation_en: "", active: true }, "questions");
      $$("[data-q]").forEach((el) => el.onclick = () => editQuestion(data.find((q) => q.id === Number(el.dataset.q)), "questions"));
    };
    render();
  }

  if (tab === "players") {
    app.innerHTML = head + `<section class="card admin-list"><h3>${data.length} Spieler</h3>
      ${data.map((p) => `<div class="item"><div class="row wrap"><b>${esc(p.nickname)}</b>${p.is_admin ? '<span class="pill">Admin</span>' : ""}
        <span class="spacer"></span><span class="muted small">Best: ${p.best ?? "–"} · Läufe: ${p.runs} · Learn: ${p.learned}</span></div>
        <div class="row" style="margin-top:6px"><button class="ghost" data-pw="${p.id}">Passwort setzen</button>
        ${p.is_admin ? "" : `<button class="ghost" data-del="${p.id}" data-n="${esc(p.nickname)}">Löschen</button>`}</div></div>`).join("")}</section>`;
    bindHead();
    $$("[data-pw]").forEach((b) => b.onclick = async () => {
      const pw = prompt("Neues Passwort (mind. 6 Zeichen):"); if (!pw) return;
      try { await rpc("admin_set_password", { p_token: tok(), p_player_id: Number(b.dataset.pw), p_new: pw }); toast("Passwort geändert."); } catch (e) { toast(errText(e)); }
    });
    $$("[data-del]").forEach((b) => b.onclick = async () => {
      if (!confirm(`Spieler „${b.dataset.n}“ mit allen Ergebnissen löschen?`)) return;
      await rpc("admin_delete_player", { p_token: tok(), p_player_id: Number(b.dataset.del) }); viewAdmin("players");
    });
  }

  if (tab === "settings") {
    app.innerHTML = head + `<section class="card"><h3>Speed-Modus</h3>
        <label class="field"><span>Dauer in Sekunden (15–600)</span><input type="number" id="secs" min="15" max="600" value="${S.speedSeconds}"></label>
        <button class="btn" id="saveSecs">Speichern</button></section>
      <section class="card"><h3>Bestenliste</h3><p class="muted small">Setzt die Top-5 zurück, z. B. zum Semesterstart. Die einzelnen Läufe bleiben für Statistiken erhalten.</p>
        <button class="btn danger" id="resetRank">Bestenliste zurücksetzen</button></section>`;
    bindHead();
    $("#saveSecs").onclick = async () => {
      try { await rpc("admin_set_speed_seconds", { p_token: tok(), p_seconds: Number($("#secs").value) }); S.speedSeconds = Number($("#secs").value); toast("Gespeichert."); } catch (e) { toast(errText(e)); }
    };
    $("#resetRank").onclick = async () => {
      if (!confirm("Bestenliste wirklich zurücksetzen?")) return;
      await rpc("admin_reset_ranking", { p_token: tok() }); toast("Bestenliste zurückgesetzt.");
    };
  }
}

function editQuestion(q0, backTab) {
  const q = JSON.parse(JSON.stringify(q0));
  const ensureShape = () => {
    if (q.qtype === "mc" || q.qtype === "img") {
      if (!Array.isArray(q.options)) q.options = [{ de: "", en: "" }, { de: "", en: "" }, { de: "", en: "" }, { de: "", en: "" }];
      if (typeof q.correct !== "number") q.correct = 0;
    } else if (q.qtype === "tf") { q.options = null; if (typeof q.correct !== "boolean") q.correct = true; }
    else if (q.qtype === "match") {
      if (!q.options || !q.options.left) q.options = { left: [{ de: "", en: "" }, { de: "", en: "" }, { de: "", en: "" }], right: [{ de: "", en: "" }, { de: "", en: "" }, { de: "", en: "" }] };
      q.correct = null;
    }
  };
  ensureShape();
  const collect = () => {
    q.topic_id = $("#e_topic").value; // Typ erst nach dem Einsammeln wechseln (Formular zeigt noch den alten)
    q.prompt_de = $("#e_pde").value; q.prompt_en = $("#e_pen").value; q.image = $("#e_img").value.trim();
    q.image_source = $("#e_src").value.trim();
    q.explanation_de = $("#e_xde").value; q.explanation_en = $("#e_xen").value; q.active = $("#e_act").checked;
    if (q.qtype === "mc" || q.qtype === "img") {
      q.options = $$(".oe").map((r) => ({ de: r.querySelector(".ode").value, en: r.querySelector(".oen").value }));
      const c = $("input[name=corr]:checked"); q.correct = c ? Number(c.value) : 0;
    } else if (q.qtype === "tf") { q.correct = $("input[name=tfc]:checked").value === "true"; }
    else if (q.qtype === "match") {
      q.options = { left: $$(".me").map((r) => ({ de: r.querySelector(".lde").value, en: r.querySelector(".len").value })),
        right: $$(".me").map((r) => ({ de: r.querySelector(".rde").value, en: r.querySelector(".ren").value })) };
    }
  };
  const render = () => {
    let opts = "";
    if (q.qtype === "mc" || q.qtype === "img") {
      opts = `<h3>Antworten <span class="muted small">(Kreis = richtige Antwort)</span></h3>${q.options.map((o, i) => `
        <div class="opt-edit oe"><input type="radio" name="corr" value="${i}" ${q.correct === i ? "checked" : ""}>
          <div><input type="text" class="ode" placeholder="Deutsch" value="${esc(o.de)}"><input type="text" class="oen" placeholder="English" value="${esc(o.en)}" style="margin-top:4px">
          <button class="linkbtn small" data-rm="${i}">entfernen</button></div></div>`).join("")}
        <button class="ghost" id="addOpt" style="margin-top:8px">+ Antwort</button>`;
    } else if (q.qtype === "tf") {
      opts = `<h3>Richtige Antwort</h3><div class="radio-list"><label><input type="radio" name="tfc" value="true" ${q.correct ? "checked" : ""}> Wahr</label>
        <label><input type="radio" name="tfc" value="false" ${!q.correct ? "checked" : ""}> Falsch</label></div>`;
    } else if (q.qtype === "match") {
      opts = `<h3>Paare <span class="muted small">(links gehört zu rechts in derselben Zeile)</span></h3>${q.options.left.map((l, i) => `
        <div class="opt-edit me" style="grid-template-columns:1fr 1fr"><div><input type="text" class="lde" placeholder="Links DE" value="${esc(l.de)}"><input type="text" class="len" placeholder="Links EN" value="${esc(l.en)}" style="margin-top:4px"></div>
          <div><input type="text" class="rde" placeholder="Rechts DE" value="${esc(q.options.right[i].de)}"><input type="text" class="ren" placeholder="Rechts EN" value="${esc(q.options.right[i].en)}" style="margin-top:4px"></div>
          <button class="linkbtn small" data-rmp="${i}">Paar entfernen</button></div>`).join("")}
        <button class="ghost" id="addPair" style="margin-top:8px">+ Paar</button>`;
    }
    app.innerHTML = `<div class="row" style="margin-bottom:10px"><button class="ghost" id="back">← Zurück</button>
      <b style="margin-left:6px">${q.id ? "Frage #" + q.id : "Neue Frage"}</b></div>
      <section class="card">
        <p class="muted small">Fachbegriffe für die kombinierte Sprachversion markieren:<br>
          DE-Text: <code>{{Rillenkugellager|deep groove ball bearing}}</code> · EN-Text: <code>{{deep groove ball bearing|Rillenkugellager}}</code></p>
        <div class="row wrap"><label class="field" style="flex:1;min-width:150px"><span>Thema</span><select id="e_topic">
          ${S.topicList.map((x) => `<option value="${x.id}" ${q.topic_id === x.id ? "selected" : ""}>${esc(x.name_de)}</option>`).join("")}</select></label>
          <label class="field" style="flex:1;min-width:150px"><span>Fragetyp</span><select id="e_type">
          ${[["mc", "Multiple Choice"], ["img", "Bild erkennen"], ["tf", "Wahr/Falsch"], ["match", "Zuordnen (nur Learn)"]].map(([k, l]) => `<option value="${k}" ${q.qtype === k ? "selected" : ""}>${l}</option>`).join("")}</select></label></div>
        <label class="field"><span>Frage (Deutsch)</span><textarea id="e_pde">${esc(q.prompt_de)}</textarea></label>
        <label class="field"><span>Frage (English)</span><textarea id="e_pen">${esc(q.prompt_en)}</textarea></label>
        <label class="field"><span>Bild (optional): Pfad wie <code>img/datei.svg</code> oder vollständige URL</span><input type="text" id="e_img" value="${esc(q.image || "")}"></label>
        <label class="field"><span>Quellenangabe zur Abbildung (z. B. <code>SKF (www.skf.com) · Skript FME, Folie 17</code>)</span><input type="text" id="e_src" value="${esc(q.image_source || "")}"></label>
        ${q.image ? `<div class="qimg"><img src="${esc(q.image)}" alt="" style="max-height:160px"></div>` : ""}
        ${opts}
        <label class="field" style="margin-top:14px"><span>Erklärung (Deutsch)</span><textarea id="e_xde">${esc(q.explanation_de)}</textarea></label>
        <label class="field"><span>Erklärung (English)</span><textarea id="e_xen">${esc(q.explanation_en)}</textarea></label>
        <label class="row" style="margin:8px 0"><input type="checkbox" id="e_act" ${q.active !== false ? "checked" : ""} style="width:20px;height:20px"> Aktiv (wird im Quiz verwendet)</label>
        <div class="err" id="eerr"></div>
        <div class="row wrap"><button class="btn" id="save" style="flex:1">Speichern</button><button class="btn secondary" id="prev" style="flex:1">Vorschau</button>
          ${q.id ? `<button class="btn danger" id="del">Löschen</button>` : ""}</div>
        <div id="pv"></div></section>`;
    $("#back").onclick = () => viewAdmin(backTab);
    $("#e_type").onchange = () => { collect(); q.qtype = $("#e_type").value; ensureShape(); render(); };
    $("#e_img").onchange = () => { collect(); render(); };
    if ($("#addOpt")) $("#addOpt").onclick = () => { collect(); q.options.push({ de: "", en: "" }); render(); };
    $$("[data-rm]").forEach((b) => b.onclick = () => { collect(); q.options.splice(Number(b.dataset.rm), 1); if (q.correct >= q.options.length) q.correct = 0; render(); });
    if ($("#addPair")) $("#addPair").onclick = () => { collect(); q.options.left.push({ de: "", en: "" }); q.options.right.push({ de: "", en: "" }); render(); };
    $$("[data-rmp]").forEach((b) => b.onclick = () => { collect(); const i = Number(b.dataset.rmp); q.options.left.splice(i, 1); q.options.right.splice(i, 1); render(); });
    $("#prev").onclick = () => {
      collect();
      const pq = { id: q.id || 0, topic: q.topic_id, type: q.qtype, prompt_de: q.prompt_de, prompt_en: q.prompt_en, image: q.image, options: q.options };
      $("#pv").innerHTML = ["de", "en", "de+en", "en+de"].map((m) => `<div class="preview"><div class="pill">${m}</div><p class="prompt">${qText(pq, "prompt", m)}</p>
        ${q.qtype === "mc" || q.qtype === "img" ? q.options.map((o, i) => `<div class="small">${i === q.correct ? "✓" : "·"} ${optText(o, m)}</div>`).join("") : ""}
        ${q.qtype === "match" ? q.options.left.map((l, i) => `<div class="small">${optText(l, m)} → ${optText(q.options.right[i], m)}</div>`).join("") : ""}
        <div class="small muted" style="margin-top:6px">${fmt(m.startsWith("en") ? q.explanation_en : q.explanation_de, m)}</div></div>`).join("");
    };
    $("#save").onclick = async () => {
      collect();
      const err = $("#eerr"); err.textContent = "";
      if (!q.prompt_de.trim() || !q.prompt_en.trim()) { err.textContent = "Bitte die Frage auf Deutsch und Englisch eingeben."; return; }
      if ((q.qtype === "mc" || q.qtype === "img") && (q.options.length < 2 || q.options.some((o) => !o.de.trim() || !o.en.trim()))) { err.textContent = "Mind. 2 Antworten, jeweils DE und EN."; return; }
      if (q.qtype === "img" && !q.image) { err.textContent = "Für „Bild erkennen“ bitte ein Bild angeben."; return; }
      if (q.image && !q.image_source && !confirm("Keine Quellenangabe zur Abbildung eingetragen. Trotzdem speichern?")) return;
      if (q.qtype === "match" && (q.options.left.length < 2 || [...q.options.left, ...q.options.right].some((o) => !o.de.trim() || !o.en.trim()))) { err.textContent = "Mind. 2 vollständige Paare (DE und EN)."; return; }
      try {
        const r = await rpc("admin_save_question", { p_token: tok(), p_q: q }); q.id = r.id;
        toast("Gespeichert (#" + r.id + ")."); viewAdmin(backTab === "reports" ? "reports" : "questions");
      } catch (e) { err.textContent = errText(e) + " (" + e.code + ")"; }
    };
    if ($("#del")) $("#del").onclick = async () => {
      if (!confirm("Frage endgültig löschen? (Alternativ: „Aktiv“ abwählen)")) return;
      await rpc("admin_delete_question", { p_token: tok(), p_id: q.id }); viewAdmin("questions");
    };
  };
  show("edit", render);
}

// ------------------------------------------------------------------ Start
function start() { setUiLang(S.ui); if (S.session && S.session.token) viewHome(); else viewLogin(); }
start();
})();
