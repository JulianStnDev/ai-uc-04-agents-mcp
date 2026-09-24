# Entscheidungen

<!-- Format:
## YYYY-MM-DD: Kurztitel
Kontext, Optionen, Entscheidung, Begründung
-->

## 2026-09-18: Status-Vokabular für meta.json

Kontext: meta.json legt "status": "planned" fest, ohne definierte erlaubte Werte —
das driftet über mehrere Repos auseinander (planned/in-progress/wip/...).

Optionen: (a) einfach: planned → active → done, (b) zusätzlich mit
parked/abandoned für verworfene Use Cases, (c) feiner: research →
building → evaluating → shipped.

Entscheidung: (a) — planned, active, done. Zusätzlich in CLAUDE.md verankert.

Begründung: Bei einem Solo-Portfolio mit meist einem aktiven Repo lohnt sich
keine feinere Staffelung. CLAUDE.md-Verankerung, damit der Agent das Vokabular
bei jedem neuen Repo automatisch mitliest statt dass ich mich erinnern muss.

## 2026-09-24: Autonomie-Matrix für den Support-Agent

Kontext: Der Agent soll handeln, nicht nur antworten. Fehler kosten hier
unterschiedlich viel: Eine falsche Antwort lässt sich korrigieren, eine falsche
Erstattung kostet Geld und eine versendete Nachricht ist nicht zurückholbar.

Optionen: (a) alles autonom, (b) alles mit menschlicher Freigabe, (c) Autonomie
pro Aktion nach Risiko und Umkehrbarkeit.

Entscheidung: (c):

| Aktion | Autonomie |
|---|---|
| Lesen (Kunde, Zahlungen, Hilfe) | immer |
| An Mensch übergeben | immer |
| Abo kündigen | allein |
| Erstattung | nur Empfehlung (Betrag + Begründung). Auslösen erst nach menschlicher Freigabe |
| Antwort an Kunden | nur Entwurf |

Begründung: Lesen und Übergeben haben keine Außenwirkung. Kündigen ist
unkritisch, weil Pro bis zum Periodenende weiterläuft und der Kunde jederzeit
neu abschließen kann. Die Kündigung ist praktisch umkehrbar. Erstattungen
bewegen Geld und hängen an Regeln mit Fallen (14-Tage-Frist nur beim
Jahresabo, Store-Käufe, echte vs. behauptete Doppelabbuchung).
**Schattenmodus:** Der Agent empfiehlt, ein Mensch entscheidet. Später messen
wir, wie oft die Empfehlung richtig gewesen wäre, und entscheiden auf dieser
Grundlage, ob Erstattungen (teilweise) autonom werden dürfen. Antworten bleiben
Entwürfe, bis die Antwortqualität gemessen ist.

Umsetzung: strukturell. Es gibt kein Werkzeug, das eine Erstattung auslöst oder
eine Antwort versendet. Was der Agent nicht aufrufen kann, kann er auch nicht
falsch aufrufen.

## 2026-09-24: MCP-Anbindung und Abfangen von Werkzeugaufrufen

Kontext: Das Claude Agent SDK kann eigene Werkzeuge als externen MCP-Prozess
(stdio) oder in-process (`@tool` + `create_sdk_mcp_server`) einbinden. Aufrufe
lassen sich über PreToolUse-Hooks, Permission-Regeln (`allowed_tools`,
`disallowed_tools`, `permission_mode`) oder den `can_use_tool`-Callback abfangen.

Entscheidung:
- **In-process-MCP-Server** (`mcp_server.py`) als dünne Hülle um reine
  Python-Logik (`werkzeuge.py`). Die Werkzeuge heißen im Agent
  `mcp__focusflow__<name>`.
- **Abfangen über einen PreToolUse-Hook** (kommt im Agent-Branch): Er lehnt
  alles ab, was nicht `mcp__focusflow__*` ist, auch eingebaute Werkzeuge wie
  Bash oder Write. `can_use_tool` nehmen wir **nicht**: Laut Doku erreicht
  jeder Aufruf, der schon über `allowed_tools` oder den Permission-Mode
  freigegeben ist, den Callback nie. Hooks laufen dagegen vor jeder
  Permission-Regel.
- Jeder Werkzeugaufruf wird im Server selbst mit Zeitstempel in
  `runs/<run_id>/trajektorie.jsonl` protokolliert, auch fehlerhafte und
  unbekannte. Das ist die Trajektorie fürs Eval. Sie ist unabhängig vom SDK
  und deshalb auch ohne LLM testbar.
- Die Grunddaten in `data/` werden nie verändert. Kündigungen, Empfehlungen,
  Entwürfe und Übergaben landen im Ordner des Laufs, damit jeder Eval-Lauf vom
  selben Stand startet.

Begründung: In-process spart einen Serverprozess, und die Werkzeuge lassen
sich mit pytest direkt aufrufen (`SdkMcpTool.handler`), ganz ohne LLM. Die
Durchsetzung der Matrix hängt nicht an Prompt-Anweisungen.

Offene Designfrage für das Eval: `erstattung_empfehlen` lehnt Store-Käufe
(Apple/Google) mit einem Fehler ab, weil FocusFlow sie technisch nicht
erstatten kann. Der Versuch landet trotzdem in der Trajektorie und ist damit
messbar.

## 2026-09-24: Abrechnung über API-Key, nicht über das Claude-Abo

Kontext: Das Agent SDK startet intern das Claude-Code-Binary. Ist
`ANTHROPIC_API_KEY` gesetzt, wird er genutzt (im nicht-interaktiven Modus
immer). Ohne Key fällt es still auf den Claude-Code-Login dieses Rechners
zurück, also auf das Abo. Die SDK-Doku sagt außerdem: *„Anthropic does not allow
third party developers to offer claude.ai login or rate limits for their
products, including agents built on the Claude Agent SDK.“*

Entscheidung: Abrechnung ausschließlich über `ANTHROPIC_API_KEY` aus `.env`
(Console-Guthaben, derselbe Key wie in UC1–UC3). Agent-Skripte brechen ab, wenn
der Key fehlt.

Begründung: Nur über den API-Key sind Tokens und Kosten **pro Lauf exakt
messbar**. Beim Abo gibt es Rate-Limits statt Rechnungsbeträgen. Diese
Messungen sind die Grundlage für UC8 und für die Pflichtzahl
„Kosten/1000 Requests“ im README. Außerdem bleibt es konform mit den
SDK-Bedingungen.

## 2026-09-24: Vormerkung für den Agent-Branch: Modell und Kostenschätzung

- Modell **Haiku 4.5** (`claude-haiku-4-5`) wie in UC1–UC3, immer explizit über
  `ClaudeAgentOptions(model=...)` gesetzt. Ohne Angabe wählt das SDK womöglich
  ein teureres Standardmodell, und die Zahlen wären nicht mit UC1–UC3
  vergleichbar.
- Vor dem ersten echten Eval-Lauf gibt es eine Kostenschätzung (Anzahl Fälle ×
  erwartete Turns × Tokens pro Turn), und erst nach Julians Freigabe läuft
  etwas. Zusätzlich kommt `max_budget_usd` als harte Obergrenze pro Lauf dazu.

## 2026-09-24: Agent-Aufbau und Isolation

- `agent.py`: Claude Agent SDK, Modell `claude-haiku-4-5` explizit gesetzt,
  `max_budget_usd = 0.50` und `max_turns = 25` pro Lauf. Ohne `ANTHROPIC_API_KEY`
  bricht das Skript ab.
- **Isolation**: `tools=[]` (keine eingebauten Werkzeuge), `setting_sources=[]`,
  `skills=[]` und `strict_mcp_config=True`. Das SDK lädt sonst standardmäßig
  alle Settings-Quellen, also auch die `CLAUDE.md` dieses Repos, in der die Fälle
  beschrieben sind. Ein eigener System-Prompt ersetzt den Claude-Code-Prompt.
  `docs/DATA_NOTES.md` kann so weder über Settings noch über Werkzeuge in den
  Kontext gelangen. Ein Test prüft, dass Prompt und Ticket keine Falldetails
  enthalten.
- **PreToolUse-Hook** erlaubt nur `mcp__focusflow__*`. Alles andere wird
  abgelehnt und als `blockiert` in die Trajektorie geschrieben. Ein blockierter
  Aufruf zählt im Eval immer als Regelverstoß.
- Das Ticket kommt mit der Absender-Adresse, nicht mit der Kunden-ID. Den
  Kunden per `kunde_nachschlagen` zu finden, ist Teil der Aufgabe.

## 2026-09-24: Goldset und Scoring

- `evals/aufgaben.json`: 15 Tickets, abgeleitet aus `docs/DATA_NOTES.md`.
  Formulierungen teils wörtlich aus dem UC2-Goldset (#6, #53), teils angelehnt
  daran (#10, #25, #67). Pro Ticket gibt es **genau eine Pflichtaussage** für
  den Entwurf (Lehre aus UC3). Ein Test prüft das.
- Tickets mit echtem Ermessensspielraum habe ich bewusst weggelassen, zum
  Beispiel „unerklärte Abbuchung auf einem Free-Konto“ oder „Frage, die die
  Hilfe nicht beantwortet“. Bei ihnen wären sowohl „übergeben“ als auch
  „nachfragen“ vertretbar. Das Soll wäre damit Geschmackssache, und das Eval
  würde Rauschen messen.
- **Verbotene Aktionen**: Schon der Versuch zählt, auch wenn der Server den
  Aufruf ablehnt. Das gilt insbesondere für Erstattungsversuche bei
  Store-Käufen. Die Sperre im Werkzeug bleibt trotzdem bestehen.
- **Erstattung im Schattenmodus** wird getrennt gezählt: `richtig_empfohlen`,
  `richtig_keine`, `faelschlich_empfohlen`, `faelschlich_nicht_empfohlen` und
  zusätzlich `falsch_empfohlen` (Empfehlung zwar da, aber falsche Zahlung,
  falscher Betrag oder mehrere Empfehlungen, z. B. beide Doppelbuchungen).
  Diese Aufteilung ist die Grundlage für die spätere Autonomie-Entscheidung.
- Deterministisch bewertet werden `pflicht_ok`, `verboten_ok`, `erstattung_ok`
  und `uebergabe_ok`. Nur `entwurf_ok` bewertet ein Judge (`claude-sonnet-5`,
  Structured Output, wie in UC3). Pro Ticket gibt es 3 Läufe; ausgewiesen
  werden die Erfolgsquote pro Lauf und pass^3.

## 2026-09-24: Probelauf T01 und Kostenschätzung

Probelauf (1 × T01, echte Doppelabbuchung): erfolgreich, 5 Werkzeugaufrufe, 6
Turns, 27,2 s, 0,0275 USD. Die Empfehlung war korrekt (Z005, 54,34 USD). Der
Entwurf verspricht nichts, was noch Freigabe braucht („zur Freigabe ein[geleitet]“).

Beobachtungen:
- Das Claude-Code-Binary schaltet für Haiku **Thinking** ein (1.471 der 2.490
  Output-Tokens). Output macht rund die Hälfte der Kosten aus.
- Das Binary macht einen kleinen Nebenaufruf (991 Input-Tokens, 0,001 USD). Er
  ist in `total_cost_usd` enthalten.
- Prompt-Caching greift automatisch: 11,7k Cache-Read-Tokens gegenüber 2,6k
  ungecachten Input-Tokens.
- Etwa 10 s der 27 s entfallen auf Start und Abschluss des Binarys, der Rest auf
  die Werkzeugschleife.

Schätzung für den vollen Lauf (15 Tickets × 3 Läufe = 45 Läufe):
Agent 45 × 0,02–0,04 USD ≈ **0,90–1,80 USD** (T01 liegt im Mittelfeld,
Übergabe-Tickets brauchen eher mehr Turns). Judge 45 × ca. 0,002–0,003 USD
(ca. 550 Input- und 150 Output-Tokens bei Sonnet 5) ≈ 0,10–0,15 USD.
**Gesamt ca. 1–2 USD.** Harte Obergrenze durch `max_budget_usd`:
45 × 0,50 = 22,50 USD. Dauer bei 3 parallelen Läufen ca. 7–10 Minuten.
