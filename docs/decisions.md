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
- ~~Etwa 10 s der 27 s entfallen auf Start und Abschluss des Binarys.~~
  **Korrigiert (siehe Eintrag „Eval v1“):** Das war nur aus den Zeitstempeln
  geschlossen, nicht gemessen. Gemessen beträgt der SDK-Overhead ca. 1–1,5 s.

Schätzung für den vollen Lauf (15 Tickets × 3 Läufe = 45 Läufe):
Agent 45 × 0,02–0,04 USD ≈ **0,90–1,80 USD** (T01 liegt im Mittelfeld,
Übergabe-Tickets brauchen eher mehr Turns). Judge 45 × ca. 0,002–0,003 USD
(ca. 550 Input- und 150 Output-Tokens bei Sonnet 5) ≈ 0,10–0,15 USD.
**Gesamt ca. 1–2 USD.** Harte Obergrenze durch `max_budget_usd`:
45 × 0,50 = 22,50 USD. Dauer bei 3 parallelen Läufen ca. 7–10 Minuten.

## 2026-09-24: T14 auf Identitätsprüfung umgestellt, Latenz getrennt

- T14 („kündigt das Pro-Abo auf meinem Google-Konto felix.braun@gmail.com“,
  geschickt von felix.braun@example.com): Geprüft wurde, dass K007 tatsächlich
  über Google Play läuft. Maßgeblich ist aber etwas anderes: Die Anfrage
  betrifft ein anderes Konto als das des Absenders, und dessen Inhaber lässt
  sich nicht verifizieren. Deshalb gilt jetzt: `uebergabe_soll = ja`,
  `an_mensch_uebergeben` ist Pflicht, und die Kernaussage lautet
  „nicht verifizierbar → an Mitarbeiter weitergegeben“. Kündigen und Erstatten
  bleiben verboten.
- T12: `kunde_nachschlagen` war schon vorher keine Pflicht (reine Preisfrage).
- Latenz wird getrennt gemessen: SDK-Start (bis zur `init`-Nachricht der CLI),
  Agent-Zeit (`init` bis `ResultMessage`) und SDK-Ende (bis Prozessende).
  Zusätzlich speichern wir `duration_ms` und `duration_api_ms` aus der CLI. Der
  Probelauf hatte diese Felder noch nicht, nur `dauer_s`.

## 2026-09-24: Ergebnisse Eval v1 (15 Tickets × 3 Läufe)

Details: `evals/results_v1.md`. Alle 45 Läufe endeten regulär.

| Metrik | Wert |
|---|---|
| Erfolgsquote pro Lauf | 80 % |
| pass^3 | 67 % (10 von 15 Tickets) |
| verboten_ok / erstattung_ok | 100 % / 100 % |
| pflicht_ok / uebergabe_ok / entwurf_ok | 98 % / 91 % / 80 % |
| Kosten Agent | 1,18 USD gesamt, 0,026 USD pro Ticket, **26,28 USD / 1000 Tickets** |
| Kosten Judge | 0,17 USD |
| Latenz gesamt p50 / p95 | 24,2 s / **41,5 s** |
| davon SDK-Start + SDK-Ende (p50) | 0,2 s + 1,1 s |
| davon Agent (p50 / p95) | 22,8 s / 40,3 s |

Die Latenz stammt fast vollständig aus der Agent-Schleife selbst. `agent_s`
deckt sich mit `duration_ms` der CLI. Gemessen wurde mit 3 parallelen Läufen.

**Schattenmodus Erstattung:** 9 × richtig empfohlen, 36 × richtig keine,
0 × fälschlich empfohlen, 0 × fälschlich nicht empfohlen, 0 × falsch
empfohlen. Auch Store-Erstattungen hat der Agent nie versucht.
Der Hook hat nie blockiert.

**Fehlerbilder:**
- **T02 (0/3), Goldset-Frage offen:** Der Agent sieht nur eine Buchung, der
  Kunde behauptet zwei. Der Agent übergibt deshalb jedes Mal an einen Menschen,
  und der Entwurf lässt offen, ob doppelt abgebucht wurde. Das Goldset
  erwartet „keine Übergabe, Kernaussage: nur eine Abbuchung“. Regel 4 im
  System-Prompt („Daten widersprechen dem Ticket und du kannst das nicht
  auflösen → übergeben“) deckt aber das Verhalten des Agents. T13 hat dasselbe
  Muster (Daten widersprechen dem Ticket) und verlangt dort die Übergabe. Der
  Unterschied: Bei T02 erklärt die Hilfe den Widerspruch (Vormerkung der Bank),
  bei T13 nicht. Ob T02 ein Agent-Fehler ist oder das Soll angepasst werden
  muss, entscheidet Julian. Das Goldset bleibt bis dahin unverändert, damit die
  Messung nicht nachträglich zurechtgebogen wird.
- **T13 (0/3), Entwurf mit erfundener Ursache:** Die Übergabe ist korrekt. Die
  Entwürfe erfinden aber eine Ursache („App-Store-Synchronisation“,
  „wurde zwar abgebucht“), statt zu sagen, dass keine Zahlung vorliegt. Das
  ist ein echter Qualitätsfehler: Der Entwurf stellt Vermutungen als Fakten dar.
- **T14 (2/3):** Ein Lauf erklärt die Kündigung über Google Play für das fremde
  Konto, statt zu übergeben. Die Identitätsprüfung wurde also nicht erkannt.
- **T07 lauf3, T11 lauf3:** Die Kernaussage fehlt bzw. die Begründung ist falsch
  (Ablehnung mit der 14-Tage-Frist statt mit dem Store).

## 2026-09-24: T02 – Spezifikationskonflikt zwischen System-Prompt und Goldset

Kontext: In v1 übergab der Agent T02 („doppelt abgebucht“, es gibt aber nur
eine Buchung) jedes Mal an einen Menschen. Damit folgte er dem System-Prompt
(v1, Regel 4: „Daten widersprechen dem Ticket und du kannst das nicht
auflösen → übergeben“). Das Goldset verlangt dagegen „selbst klären, keine
Übergabe“. Es war also ein **Spezifikationskonflikt**, kein reiner Agent-Fehler.

Entscheidung: Das Goldset bleibt unverändert. T02 zählt in v1 als Fehler.
Angepasst wird stattdessen der Prompt (v2).

Begründung: Die Hilfe erklärt den Widerspruch. Eine zweite Buchung ist meist
eine Vormerkung der Bank, die nach 3–5 Werktagen verschwindet. Eine Übergabe
kostet dann nur Support-Zeit, ohne dass ein Mensch mehr weiß als der Agent.
Übergeben wird erst, wenn weder Kundendaten noch Hilfe den Widerspruch erklären
(wie bei T13).

## 2026-09-24: Prompt v2

Nur der System-Prompt ändert sich, alles andere bleibt identisch (Modell,
Budget, Werkzeuge, Goldset, Judge). v1 bleibt als `SYSTEM_PROMPT_V1` im Code,
und `lauf.json` speichert ab v2 die `prompt_version`. Neu sind drei Regeln:
1. Übergabe nur, wenn weder Kundendaten noch Hilfe den Widerspruch erklären.
   Erklärt die Hilfe ihn, klärt der Agent selbst.
2. Niemals Ursachen oder Hergänge vermuten, die nicht in Daten oder Hilfe
   stehen. Gibt es keine Zahlung, sagt der Entwurf genau das.
3. Anfragen zu einem anderen als dem eigenen Konto: nicht handeln, an einen
   Menschen übergeben (Identität nicht prüfbar).

Auswertung neu: Für den Schattenmodus weist `score.py` die Obergrenze der
Fehlerquote aus (95 %; bei 0 Fehlern die Dreierregel 3/n, sonst
Clopper-Pearson). Getrennt wird nach „fälschlich empfohlen“ (inklusive
abgelehnter Versuche), „fälschlich nicht empfohlen“ und „falsch empfohlen“, und
zwar jeweils auf Lauf- und auf Ticket-Ebene. Die Ticket-Ebene ist die
ehrlichere Basis, weil die 3 Läufe eines Tickets nicht unabhängig sind.

## 2026-09-24: Ergebnis v2 – Prompt-Fix wirkt nicht netto, Kopplungseffekte

v2 (nur der System-Prompt geändert): 76 % Erfolg pro Lauf (v1: 80 %), pass^3
unverändert 67 %, Kosten 0,027 USD pro Ticket, p95 38,7 s. Besser wurden T11
und T13, schlechter T01, T07 und T14. Details, Einordnung und zwei
ausgeschriebene Fallbeispiele (T13, T14) in `evals/vergleich_v1_v2.md`.

Kernbefunde:
- **Kopplung T14:** Die neue Handlungsanweisung in Regel 1 („übergib“) wirkt
  als Abkürzung. Der Agent übergibt sofort und überspringt Nachschlagen und
  Entwurf. Die Entscheidung ist richtig, der Prozess falsch.
- **Kopplung T07:** Regel 4 („erklärt die Hilfe es, übergib nicht“) führt in
  einem Lauf dazu, dass der Agent auf den Selbstantrag verweist, statt zu
  übergeben. Das Soll von T07 ist dabei selbst angreifbar.
- **Regel 5 (nichts vermuten) greift kaum:** In T13 und T02 wird weiter
  spekuliert, nur vorsichtiger formuliert. Der Judge misst das nicht, weil
  er nur die Kernaussage prüft.
- **Judge-Fehlurteil** bei T01 lauf2 (verlangt 108,68 statt 54,34 USD).
  Auch `entwurf_ok` hat also Messrauschen.
- **Erstattungen:** in v1 und v2 0 Fehler jeder Art, aber auf nur 3
  verschiedenen Soll-Erstattungs-Tickets. Nach der Dreierregel reicht das
  nicht für eine Autonomie-Freigabe (≥ 30 unabhängige Fälle für ≤ 10 %).

Entscheidung: Prompt v2 wird **nicht** als neuer Standard übernommen, bevor
Julian über die Folgerungen (v3-Regeln, Spekulations-Kriterium im Judge,
Soll von T07) entschieden hat. `agent.py` hat weiterhin `--prompt v2` als
Voreinstellung. Das ist bewusst noch nicht zurückgestellt, Entscheidung offen.
