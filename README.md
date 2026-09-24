# Agents mit MCP: Support-Agent mit Freigaberegeln

> Status: in Arbeit. Eval v1 ist gelaufen, die Auswertung der Fehlerbilder ist offen.

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
15 Tickets (`evals/aufgaben.json`) × 3 Läufe mit Haiku 4.5. Gemessen wird
deterministisch aus der Trajektorie (Pflichtwerkzeuge, verbotene Aktionen,
Erstattungsempfehlung im Schattenmodus, Übergabe). Nur der Antwortentwurf wird
per Sonnet-5-Judge bewertet. v1: **80 % Erfolg pro Lauf, pass^3 67 %**,
0 Regelverstöße, 45/45 Erstattungsentscheidungen richtig. Details in
`evals/results_v1.md` und `docs/decisions.md`.

## Kosten & Latenz
- Kosten pro 1000 Requests: 26,28 USD (Agent pro Ticket, Haiku 4.5, v1)
- p95-Latenz: 41,5 s pro Ticket (davon ca. 1,3 s SDK-Overhead)
- Qualitätsmetrik: pass^3 = 67 % (Erfolgsquote pro Lauf 80 %)

## Learnings
[Was hat funktioniert, was nicht?]

## Was ich anders machen würde
[Retrospektive]
