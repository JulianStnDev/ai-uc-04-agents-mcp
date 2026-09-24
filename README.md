# Agents mit MCP: Support-Agent mit Freigaberegeln

> Status: in Arbeit. Eval v1–v3 ist gelaufen, v3 ist der Standard. Offen: Judge-Datumslücke bei `keine_spekulation`.

## Problem
Ein Support-Agent für die fiktive App FocusFlow (aus UC3) soll Anliegen zu Abo,
Zahlungen und Konto nicht nur beantworten, sondern über Werkzeuge bearbeiten.
Die Frage für den PM lautet: Welche Aktionen darf ein Agent allein ausführen,
und wie entscheidet man das mit Daten statt aus dem Bauch?

## PM-Entscheidung
[Welche Optionen wurden abgewogen? Warum diese Lösung?]

## Architekturskizze
- `werkzeuge.py`: 7 Werkzeuge als reine Python-Logik. Jeder Aufruf wird in
  `runs/<run_id>/trajektorie.jsonl` protokolliert.
- `mcp_server.py`: In-Process-MCP-Server `focusflow` fürs Claude Agent SDK.
- `data/`: 15 erfundene Kunden, 43 Zahlungen. `corpus/`: 20 Hilfeartikel aus UC3.
- Autonomie-Matrix: Lesen und Übergeben immer, Kündigen allein, Erstattung nur
  als Empfehlung (Schattenmodus), Antworten nur als Entwurf. Details in `CLAUDE.md`
  und `docs/decisions.md`.

```bash
uv venv && uv pip install --python .venv -r requirements.txt
.venv/bin/python -m pytest
```

## Evaluationsergebnisse
15 Tickets (`evals/aufgaben.json`) × 3 Läufe je Prompt-Version mit Haiku 4.5.
Gemessen wird deterministisch aus der Trajektorie (Pflichtwerkzeuge, verbotene
Aktionen, Erstattungsempfehlung im Schattenmodus, Übergabe). Der Antwortentwurf
wird per Sonnet-5-Judge mit der Trajektorie als Kontext bewertet (Kernaussage und
`keine_spekulation`). Ab v3 erzwingt ein Stop-Hook die Pflichten, seine Eingriffe
werden als eigene Kennzahl ausgewiesen.

| | v1 | v2 | v3 |
|---|---|---|---|
| Erfolg pro Lauf | 82 % | 78 % | **87 %** |
| pass^3 | 73 % | 73 % | 73 % |
| keine_spekulation | 64 % | 58 % | 58 % |
| Läufe mit Pflicht-Eingriff | – | – | 7 % |

0 Regelverstöße und 0 falsche Erstattungsentscheidungen in 135 Läufen, aber nur
auf 15 Tickets (Obergrenze auf Ticket-Ebene ≤ 25 % bzw. ≤ 100 %). Details in
`evals/vergleich_v1_v2_v3.md` und `docs/decisions.md`.

## Kosten & Latenz
- Kosten pro 1000 Requests: 27,0 USD (Agent pro Ticket, Haiku 4.5, v3)
- p95-Latenz: 37,0 s pro Ticket (v3; SDK-Overhead ca. 1,3 s)
- Qualitätsmetrik: pass^3 = 73 % (Erfolgsquote pro Lauf 87 %, v3, Judge j2)

## Learnings
[Was hat funktioniert, was nicht?]

## Was ich anders machen würde
[Retrospektive]
