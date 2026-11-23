# FME-Quiz – Schritt-für-Schritt-Anleitung

Quiz-Plattform für **Fundamentals of Machine Elements** mit Speed- und Learn-Modus, Top-5-Bestenliste, Deutsch/Englisch und einem Admin-Bereich.
Der Betrieb ist **kostenlos**: Die Datenbank läuft im Free-Tarif von **Supabase**, die Webseite auf **GitHub Pages**.

Zeitbedarf für die Einrichtung: etwa 30 Minuten.

---

## Inhalt des Ordners

| Datei / Ordner | Zweck |
|---|---|
| `index.html`, `app.js`, `style.css` | Die Webseite (läuft komplett im Browser, auch auf dem Handy) |
| `config.js` | **Hier tragt ihr eure Supabase-Zugangsdaten ein** (Schritt 3) |
| `img/` | Abbildungen für die Bildfragen (eigene Schemazeichnungen `.svg` und Abbildungen aus dem Skript `.jpg`) |
| `supabase/01_schema.sql` | Legt die Datenbank an: Tabellen, Login, Punktezählung, Admin-Funktionen |
| `supabase/02_fragen_lager_getriebe.sql` | Die ersten Fragen (Wälzlager + Getriebe), mit eigenen Schemazeichnungen |
| `supabase/03_fragen_skript_abbildungen.sql` | Bildfragen mit Abbildungen aus dem Skript, jeweils mit Quellenangabe |
| `.github/workflows/keepalive.yml` | Hält das kostenlose Supabase-Projekt wach (Schritt 6) |
| `tools/` | Hilfsskripte (Bilder und Fragen-SQL erzeugen) – für den Betrieb nicht nötig |

---

## Schritt 1 – Supabase-Projekt anlegen

1. Auf **https://supabase.com** gehen → **Start your project** → registrieren (z. B. mit dem GitHub-Konto aus Schritt 4 oder per E-Mail).
2. **New project** anklicken und ausfüllen:
   - **Name:** `fme-quiz`
   - **Database Password:** ein sicheres Passwort erzeugen und gut aufbewahren (wird im Alltag nicht gebraucht).
   - **Region:** **Central EU (Frankfurt)**. Dann liegen die Daten in der EU.
   - **Plan:** Free.
   - Falls angezeigt: **Data API** eingeschaltet lassen.
3. **Create new project** klicken und 1–2 Minuten warten, bis das Projekt bereit ist.

## Schritt 2 – Datenbank einrichten

1. Links im Menü **SQL Editor** öffnen → **New query**.
2. Den kompletten Inhalt von `supabase/01_schema.sql` einfügen → **Run**.
   Am Ende sollte *Success. No rows returned* stehen.
3. Wieder **New query** → Inhalt von `supabase/02_fragen_lager_getriebe.sql` einfügen → **Run**.
4. Ebenso mit `supabase/03_fragen_skript_abbildungen.sql`.
5. Kontrolle (optional): **Table Editor** → Tabelle `questions` sollte 92 Fragen enthalten.

> Alle Skripte kann man gefahrlos erneut ausführen. Die Fragen werden nur eingefügt, wenn das Thema noch leer ist, sodass Änderungen aus dem Admin-Bereich nicht überschrieben werden.

## Schritt 3 – Zugangsdaten in `config.js` eintragen

1. In Supabase oben auf **Connect** klicken (oder **Project Settings → API Keys**).
2. Kopieren:
   - die **Project URL** (`https://xxxxxxxx.supabase.co`)
   - den **Publishable key** (`sb_publishable_…`). Alternativ geht auch der ältere **anon public** Key unter *Legacy API Keys*.
3. `config.js` mit einem Texteditor öffnen und beide Werte eintragen:

```js
window.QUIZ_CONFIG = {
  supabaseUrl: "https://xxxxxxxx.supabase.co",
  supabaseKey: "sb_publishable_xxxxxxxxxxxxxxxx"
};
```

> Dieser Key darf öffentlich sein. Die Datenbank ist so eingerichtet, dass man damit nur die Quiz-Funktionen aufrufen kann, nicht direkt Tabellen lesen oder ändern.
> **Niemals** den *secret* bzw. *service_role* Key eintragen!

## Schritt 4 – Webseite auf GitHub Pages veröffentlichen

1. Auf **https://github.com** ein kostenloses Konto anlegen (z. B. ein Lehrstuhl-Konto).
2. Oben rechts **+ → New repository**:
   - **Repository name:** `fme-quiz`
   - **Public** auswählen (für kostenloses GitHub Pages nötig. Es liegen keine Geheimnisse im Code.)
   - **Create repository**
3. Auf der neuen Seite **uploading an existing file** anklicken.
   Den **gesamten Inhalt** des Ordners `fme-quiz` (alle Dateien und Unterordner, nicht den Ordner selbst) ins Browserfenster ziehen → **Commit changes**.
4. Prüfen, ob der Ordner `.github` mit hochgeladen wurde (Dateiliste im Repository). Falls nicht (versteckte Ordner werden manchmal übersprungen):
   **Add file → Create new file**, als Namen `.github/workflows/keepalive.yml` eintippen, den Inhalt der Datei hineinkopieren → **Commit changes**.
5. **Settings → Pages**:
   - **Source:** *Deploy from a branch*
   - **Branch:** `main`, Ordner `/ (root)` → **Save**
6. Nach 1–2 Minuten erscheint oben die Adresse, z. B.
   **`https://<github-name>.github.io/fme-quiz/`**. Das ist der Link für die Studierenden.

> Tipp: Aus dem Link einen QR-Code für die Vorlesungsfolie machen.

## Schritt 5 – Admin-Zugang einrichten

1. Die Quiz-Seite öffnen → **Registrieren** → einen Nickname wählen, z. B. `FMT_Admin`.
2. In Supabase **SQL Editor → New query**:

```sql
update public.players set is_admin = true where lower(nickname) = lower('FMT_Admin');
```

3. In der Quiz-Seite ab- und wieder anmelden. Oben erscheint jetzt der Button **Admin**.

## Schritt 6 – Automatisches Wachhalten prüfen

Kostenlose Supabase-Projekte pausieren nach **7 Tagen ohne Nutzung** (z. B. in den Semesterferien). Der mitgelieferte GitHub-Ablauf pingt die Datenbank deshalb alle 3 Tage an.

1. Im GitHub-Repository den Reiter **Actions** öffnen. Falls gefragt: *I understand my workflows, go ahead and enable them*.
2. Links **Supabase keep-alive** wählen → **Run workflow** → **Run workflow**.
3. Nach ca. 30 Sekunden sollte ein grüner Haken erscheinen. Fertig.

> Der Ablauf liest URL und Key direkt aus `config.js`. Außerdem checkt er höchstens alle 30 Tage einen Zeitstempel ein, weil GitHub geplante Abläufe sonst nach 60 Tagen ohne Aktivität abschaltet.

Falls das Projekt trotzdem einmal pausiert: Supabase-Dashboard öffnen → **Restore project**. Die Daten bleiben erhalten.

---

## Bedienung

### Für Studierende
- **Registrieren** nur mit Nickname und Passwort, ohne E-Mail. Bitte keinen Klarnamen verwenden.
- **Speed:** 60 Sekunden. Jede richtige Antwort bringt 10 Punkte. Ab 3 richtigen Antworten in Folge zählen die Punkte ×2, ab 5 in Folge ×3. Eine falsche Antwort setzt die Serie zurück. Zeit und Punkte werden auf dem Server gezählt, man kann sie also nicht im Browser manipulieren.
- **Learn:** ohne Zeitlimit, mit Erklärung nach jeder Frage. Das Karteikasten-Prinzip sorgt dafür, dass falsch beantwortete Fragen bald und häufig wiederkommen und sichere Fragen immer seltener.
- **Sprache:** Deutsch oder English. Im Learn-Modus gibt es zusätzlich *Deutsch + EN* bzw. *English + DE* mit Fachbegriffen der anderen Sprache in Klammern.
- **⚑ Melden:** An jeder Frage kann man melden, wenn Frage oder Lösung falsch erscheint. Im Speed-Modus geht das auch nach der Runde in der Fragenübersicht.

### Admin-Bereich
- **Meldungen:** alle gemeldeten Fragen mit Kommentar. Von dort direkt **Frage bearbeiten** und danach **✓ erledigt**.
- **Fragen:** nach Thema filtern, suchen, bearbeiten, neu anlegen, deaktivieren oder löschen. Mit **Vorschau** sieht man die Frage in allen vier Sprachvarianten.
- **Spieler:** Übersicht; **Passwort setzen**, falls jemand sein Passwort vergessen hat; Spieler löschen.
- **Einstellungen:** Dauer des Speed-Modus ändern; **Bestenliste zurücksetzen**, z. B. zum Semesterstart.

### Fachbegriffe für die kombinierte Sprachversion markieren
Damit ein Begriff im Modus *Deutsch + EN* in Klammern übersetzt wird, schreibt man ihn so:

- im deutschen Text: `{{Rillenkugellager|deep groove ball bearing}}`
- im englischen Text: `{{deep groove ball bearing|Rillenkugellager}}`

In den reinen Sprachversionen erscheint nur der erste Begriff. Angehängte Buchstaben wie bei `{{Dichtung|seal}}en` werden mitgenommen.

### Bilder ergänzen und Quellen angeben
1. Bild (PNG, JPG oder SVG) im GitHub-Repository in den Ordner `img/` hochladen (**Add file → Upload files**).
2. In der Frage im Admin-Bereich als Bild `img/dateiname.jpg` eintragen.
3. Im Feld **Quellenangabe zur Abbildung** die Herkunft eintragen, z. B. `SKF (www.skf.com) · Skript FME, Folie 17`.
   Die Quelle erscheint im Quiz klein unter dem Bild („Quelle: …“). Fehlt sie, fragt der Admin-Bereich beim Speichern nach.

Bei den mitgelieferten Fragen sind die Quellen aus den Folien übernommen (Schaeffler, SKF, reiff-tp, Schlecht – Maschinenelemente 2, TU München FZG). Die eigenen Zeichnungen sind als „Eigene Darstellung, Lehrstuhl FMT“ gekennzeichnet.

---

## Kosten und Grenzen (Free-Tarif, Stand Nov. 2026)
- Supabase Free: 500 MB Datenbank und 50.000 aktive Nutzer pro Monat. Für das Quiz reicht das bei Weitem. Es sind max. 2 aktive Free-Projekte pro Konto möglich.
- GitHub Pages: kostenlos für öffentliche Repositories.

## Datenschutz (Kurzfassung)
Gespeichert werden nur Nickname, Passwort-Hash (bcrypt), Spielstände, Lernstand und Meldungen. Es gibt keine E-Mail-Adressen, keine Klarnamen und keine Tracking-Cookies. Im Browser wird lediglich das Login-Token im lokalen Speicher abgelegt. Die Datenbank liegt in Frankfurt.
Es empfiehlt sich, kurz mit der/dem Datenschutzbeauftragten der OVGU abzustimmen, ob ein Hinweistext auf der Seite gewünscht ist.

## Häufige Probleme

| Problem | Lösung |
|---|---|
| „Die Plattform ist noch nicht eingerichtet (config.js)“ | Schritt 3: URL und Key in `config.js` eintragen und neu hochladen |
| „Keine Verbindung zum Server“ | Supabase-Projekt pausiert → im Dashboard **Restore project**. Sonst URL/Key prüfen. |
| Fehler *permission denied* oder *function … does not exist* | `01_schema.sql` erneut im SQL Editor ausführen |
| Änderungen an der Seite erscheinen nicht | GitHub Pages braucht 1–2 Minuten; im Browser neu laden |
| Passwort vergessen | Admin → Spieler → **Passwort setzen** |
| Kein Admin-Button | Schritt 5 ausführen, danach ab- und wieder anmelden |
