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
