# Projekt-Kontext

## Problem
Ein Support-Agent für die fiktive Habit-Tracker-App **FocusFlow** (bekannt aus UC3)
bearbeitet Kundenanliegen rund um Abo, Zahlungen und Konto. Anders als in UC3
beantwortet er nicht nur Fragen, sondern **handelt** über Werkzeuge eines eigenen
MCP-Servers (Claude Agent SDK): Kunden nachschlagen, Zahlungen prüfen, Hilfe
durchsuchen, kündigen, Erstattungen empfehlen, Antworten entwerfen, an Menschen
übergeben. Die Kernfrage ist, **wie viel Autonomie** der Agent bekommen darf.
Die Antwort soll datenbasiert fallen, nicht aus dem Bauch.

- `data/`: erfundene Kunden und Zahlungen mit gezielt eingebauten Fällen. Die
  Details stehen in `docs/DATA_NOTES.md`. Diese Datei ist nur für Menschen und
  darf **nie** in einen Prompt.
- `corpus/`: Kopie der 20 Hilfeartikel aus UC3, einschließlich ihrer Fallen
  (siehe UC3 `docs/CORPUS_NOTES.md`).
- Referenztag der Daten („heute“): **2026-09-24**.

## Autonomie-Matrix

| Aktion | Werkzeug | Autonomie |
|---|---|---|
| Lesen (Kunde, Zahlungen, Hilfe) | `kunde_nachschlagen`, `zahlungen_ansehen`, `hilfe_durchsuchen` | immer |
| An Mensch übergeben | `an_mensch_uebergeben` | immer |
| Abo kündigen | `abo_kuendigen` | allein (nur Web-Abos; wirkt zum Periodenende) |
| Erstattung | `erstattung_empfehlen` | **nur Empfehlung**. Auslösen erst nach menschlicher Freigabe (Schattenmodus) |
| Antwort an Kunden | `antwort_entwerfen` | **nur Entwurf**, nichts wird versendet |

Durchsetzung: strukturell. Es gibt kein Werkzeug, das Geld bewegt oder eine
Nachricht versendet. Im Agent-Branch kommt ein PreToolUse-Hook dazu, der alles
außerhalb von `mcp__focusflow__*` ablehnt. Schattenmodus heißt: Wir messen, wie
oft die Erstattungsempfehlung richtig gewesen wäre, und entscheiden danach, ob
Erstattungen mehr Autonomie bekommen.

## Erwartete Artefakte
- README.md nach Schema (Problem, PM-Entscheidung, Architektur, Eval, Kosten/Latenz, Learnings)
- meta.json gepflegt (status ausschließlich: planned | active | done)
- evals/ mit Datensatz + Ergebnissen
- docs/decisions.md mit datierten Entscheidungen

## Erlaubte Libraries
- claude-agent-sdk, anthropic, python-dotenv (+ pytest für Tests)
- Direkt gegen das SDK, kein LangChain/LlamaIndex
- MCP-Server in-process über `create_sdk_mcp_server`, kein separater Serverprozess

## Modell & Abrechnung
- Modell: **Haiku 4.5** (`claude-haiku-4-5`) wie in UC1–UC3, immer explizit über
  `ClaudeAgentOptions(model=...)` setzen. Das SDK-Standardmodell ist teurer.
- Abrechnung **nur über `ANTHROPIC_API_KEY`** aus `.env`, nie über den
  Claude-Abo-Login. Agent-Skripte brechen ab, wenn der Key fehlt.
- Vor dem ersten echten Eval-Lauf: Kostenschätzung vorlegen und Freigabe abwarten.

## Stil
- Python, einfache Skripte statt Frameworks
- Drei Zahlen im README Pflicht: Kosten/1000 Requests, p95-Latenz, Qualitätsmetrik

## Arbeitsweise
- Nie direkt auf `main` committen. Pro Arbeitspaket ein Feature-Branch
  (`feat/...`, `fix/...`), am Ende Pull Request öffnen (kein `gh`: Branch
  pushen und Link zum PR-Anlegen ausgeben).
- Merge macht Julian selbst nach Review.
- `.env` (ANTHROPIC_API_KEY) ist gitignored und wird nie committet.
- Setup: `uv venv && uv pip install --python .venv -r requirements.txt`, Tests: `.venv/bin/python -m pytest`
