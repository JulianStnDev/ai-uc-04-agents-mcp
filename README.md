# Agents mit MCP: Support-Agent mit Freigaberegeln

> Status: in Arbeit. Bisher stehen Daten, MCP-Server und Tests. Noch keine LLM-Aufrufe.

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
[Wie wurde gemessen? Ergebnisse?]

## Kosten & Latenz
- Kosten pro 1000 Requests: [Zahl]
- p95-Latenz: [Zahl]
- Qualitätsmetrik: [Zahl/Beschreibung]

## Learnings
[Was hat funktioniert, was nicht?]

## Was ich anders machen würde
[Retrospektive]
