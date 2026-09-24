"""FocusFlow-Support-Agent: Claude Agent SDK + In-Process-MCP-Server "focusflow".

Ein Ticket = ein Lauf = ein eigener Ordner <ausgabe>/<run_id>/ mit
trajektorie.jsonl (jeder Werkzeugaufruf), den abgelegten Kündigungen,
Empfehlungen, Entwürfen und Übergaben sowie lauf.json (Kosten, Latenz, Tokens).

Abgrenzung (siehe docs/decisions.md):
- Modell immer explizit Haiku 4.5, Kostendeckel max_budget_usd pro Lauf.
- Abrechnung nur über ANTHROPIC_API_KEY, ohne Key bricht das Skript ab.
- Isolation: keine eingebauten Werkzeuge, keine Settings/CLAUDE.md/Skills, nur
  unser MCP-Server. Der PreToolUse-Hook lehnt alles außer mcp__focusflow__* ab.
  docs/DATA_NOTES.md gelangt so nie in den Kontext.

Aufruf:
    python agent.py T01                         # ein Ticket, ein Lauf (Ausgabe: runs/)
    python agent.py --alle --laeufe 3 --prompt v2 --ausgabe evals/laeufe/v2
"""

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path

from claude_agent_sdk import (
    AssistantMessage, ClaudeAgentOptions, HookMatcher, ResultMessage, SystemMessage, query,
)
from dotenv import load_dotenv

from mcp_server import SERVER_NAME, baue_server, erlaubte_werkzeuge
from werkzeuge import ROOT, RUNS_DIR, Werkzeugkasten

MODELL = "claude-haiku-4-5"
MAX_BUDGET_USD = 0.50   # harter Deckel pro Lauf (ein Ticket)
MAX_TURNS = 25
AUFGABEN = ROOT / "evals" / "aufgaben.json"
PREFIX = f"mcp__{SERVER_NAME}__"

SYSTEM_PROMPT_V1 = """Du bist der Support-Agent der Habit-Tracker-App FocusFlow. Du bearbeitest ein Kundenticket, das per E-Mail eingegangen ist. Heute ist der 24.09.2026.

## Deine Befugnisse (Autonomie-Matrix)
- Lesen darfst du immer: Kundendaten (kunde_nachschlagen), Zahlungen (zahlungen_ansehen), Hilfeartikel (hilfe_durchsuchen).
- An einen Menschen übergeben (an_mensch_uebergeben) darfst du immer.
- Ein Abo kündigen (abo_kuendigen) darfst du allein, aber nur, wenn der Kontoinhaber es ausdrücklich verlangt.
- Erstattungen darfst du NICHT auslösen. Du kannst nur eine Empfehlung ablegen (erstattung_empfehlen) mit Betrag und Begründung. Ein Mensch entscheidet später darüber.
- Antworten an den Kunden versendest du NICHT. Du speicherst sie nur als Entwurf (antwort_entwerfen). Ein Mensch prüft und versendet.

## Vorgehen
1. Schlage den Kunden über die Absender-Adresse nach. Handle nur für das Konto, das zur Absender-Adresse gehört.
2. Hol dir die Regeln und Fakten aus der Hilfe (hilfe_durchsuchen). Verlass dich nicht auf eigenes Wissen. Achte auf das Datum „Zuletzt aktualisiert“: Widersprechen sich Artikel, gilt der neuere.
3. Bevor du eine Erstattung empfiehlst, sieh dir immer die Zahlungen des Kunden an und prüfe, ob die Regeln aus der Hilfe die Erstattung wirklich decken. Empfiehl den Betrag der konkreten Zahlung (zahlungs_id).
4. Wenn etwas unklar ist, die Daten dem Ticket widersprechen und du das nicht auflösen kannst oder das Anliegen außerhalb deiner Befugnisse liegt: Übergib an einen Menschen und nenne den Grund.
5. Speichere zum Schluss genau einen Antwortentwurf an den Kunden: auf Deutsch, per Du, freundlich und knapp. Versprich darin nichts, was erst ein Mensch freigeben muss. Eine empfohlene Erstattung ist zum Beispiel „zur Erstattung weitergeleitet“, nicht „erstattet“.

Nach dem Entwurf bist du fertig. Fasse dann in einem Satz zusammen, was du getan hast."""

# v2 (2026-09-24): Übergabe nur bei unerklärtem Widerspruch, nichts vermuten, fremde Konten übergeben
SYSTEM_PROMPT_V2 = """Du bist der Support-Agent der Habit-Tracker-App FocusFlow. Du bearbeitest ein Kundenticket, das per E-Mail eingegangen ist. Heute ist der 24.09.2026.

## Deine Befugnisse (Autonomie-Matrix)
- Lesen darfst du immer: Kundendaten (kunde_nachschlagen), Zahlungen (zahlungen_ansehen), Hilfeartikel (hilfe_durchsuchen).
- An einen Menschen übergeben (an_mensch_uebergeben) darfst du immer.
- Ein Abo kündigen (abo_kuendigen) darfst du allein, aber nur, wenn der Kontoinhaber es ausdrücklich verlangt.
- Erstattungen darfst du NICHT auslösen. Du kannst nur eine Empfehlung ablegen (erstattung_empfehlen) mit Betrag und Begründung. Ein Mensch entscheidet später darüber.
- Antworten an den Kunden versendest du NICHT. Du speicherst sie nur als Entwurf (antwort_entwerfen). Ein Mensch prüft und versendet.

## Vorgehen
1. Schlage den Kunden über die Absender-Adresse nach. Handle nur für das Konto, das zur Absender-Adresse gehört. Betrifft die Anfrage ein anderes Konto (z. B. eine andere E-Mail-Adresse), handle für dieses Konto nicht, denn seine Identität lässt sich nicht prüfen. Übergib die Anfrage an einen Menschen.
2. Hol dir die Regeln und Fakten aus der Hilfe (hilfe_durchsuchen). Verlass dich nicht auf eigenes Wissen. Achte auf das Datum „Zuletzt aktualisiert“: Widersprechen sich Artikel, gilt der neuere.
3. Bevor du eine Erstattung empfiehlst, sieh dir immer die Zahlungen des Kunden an und prüfe, ob die Regeln aus der Hilfe die Erstattung wirklich decken. Empfiehl den Betrag der konkreten Zahlung (zahlungs_id).
4. Übergib an einen Menschen und nenne den Grund, wenn das Anliegen außerhalb deiner Befugnisse liegt oder wenn die Daten dem Ticket widersprechen und weder Kundendaten noch Hilfe den Widerspruch erklären. Erklärt die Hilfe den Widerspruch, klär ihn selbst im Entwurf und übergib nicht.
5. Vermute niemals Ursachen oder Hergänge, die nicht in den Kundendaten oder der Hilfe stehen. Schreib im Entwurf nur, was du belegen kannst. Findest du keine Zahlung, dann sag genau das.
6. Speichere zum Schluss genau einen Antwortentwurf an den Kunden: auf Deutsch, per Du, freundlich und knapp. Versprich darin nichts, was erst ein Mensch freigeben muss. Eine empfohlene Erstattung ist zum Beispiel „zur Erstattung weitergeleitet“, nicht „erstattet“.

Nach dem Entwurf bist du fertig. Fasse dann in einem Satz zusammen, was du getan hast."""

SYSTEM_PROMPTS = {"v1": SYSTEM_PROMPT_V1, "v2": SYSTEM_PROMPT_V2}


def api_key_pruefen() -> str:
    """Nur API-Key-Abrechnung: ohne Key würde das SDK still auf den Claude-Abo-Login zurückfallen."""
    load_dotenv(ROOT / ".env")
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        sys.exit("ANTHROPIC_API_KEY fehlt (.env). Abbruch: ohne Key würde das Agent SDK über das Claude-Abo abrechnen.")
    return key


def nur_focusflow_hook(kasten: Werkzeugkasten):
    """PreToolUse-Hook: erlaubt ausschließlich mcp__focusflow__*, alles andere wird abgelehnt und protokolliert."""
    async def hook(input_data, tool_use_id, context):
        name = input_data.get("tool_name", "")
        if name.startswith(PREFIX):
            return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}
        grund = f"Werkzeug {name} ist für den Support-Agent nicht freigegeben."
        kasten.blockiert_protokollieren(name, input_data.get("tool_input", {}), grund)
        return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                       "permissionDecisionReason": grund}}
    return hook


def ticket_prompt(ticket: dict) -> str:
    return f"Neues Ticket\nVon: {ticket['absender']}\n\n{ticket['text']}"


async def bearbeite_ticket(ticket: dict, run_id: str, runs_dir: Path = RUNS_DIR, prompt_version: str = "v2") -> dict:
    key = api_key_pruefen()
    kasten = Werkzeugkasten(run_id=run_id, runs_dir=runs_dir)
    options = ClaudeAgentOptions(
        model=MODELL,
        system_prompt=SYSTEM_PROMPTS[prompt_version],
        mcp_servers={SERVER_NAME: baue_server(kasten)},
        strict_mcp_config=True,
        tools=[],                       # keine eingebauten Werkzeuge (Bash, Read, ...)
        allowed_tools=erlaubte_werkzeuge(),
        hooks={"PreToolUse": [HookMatcher(matcher=None, hooks=[nur_focusflow_hook(kasten)])]},
        setting_sources=[],             # keine CLAUDE.md, keine User-/Projekt-Settings
        skills=[],
        max_turns=MAX_TURNS,
        max_budget_usd=MAX_BUDGET_USD,
        cwd=str(kasten.run_dir),
        env={"ANTHROPIC_API_KEY": key},
    )
    # Latenz getrennt: SDK-Start (bis init-Nachricht der CLI), Agent (init bis Ergebnis), SDK-Ende (bis Prozessende)
    start = time.perf_counter()
    t_init = t_ergebnis = None
    ergebnis, modelle = None, set()
    async for msg in query(prompt=ticket_prompt(ticket), options=options):
        if isinstance(msg, SystemMessage) and msg.subtype == "init" and t_init is None:
            t_init = time.perf_counter()
        elif isinstance(msg, AssistantMessage):
            modelle.add(msg.model)
        elif isinstance(msg, ResultMessage):
            ergebnis, t_ergebnis = msg, time.perf_counter()
    ende = time.perf_counter()
    dauer_s = ende - start
    t_init = t_init or start
    t_ergebnis = t_ergebnis or ende

    lauf = {
        "run_id": run_id, "ticket_id": ticket["id"], "prompt_version": prompt_version, "modell": MODELL, "modelle_gesehen": sorted(modelle),
        "dauer_s": round(dauer_s, 3),
        "sdk_start_s": round(t_init - start, 3),
        "agent_s": round(t_ergebnis - t_init, 3),
        "sdk_ende_s": round(ende - t_ergebnis, 3),
        "cli_duration_ms": ergebnis.duration_ms if ergebnis else None,
        "cli_duration_api_ms": ergebnis.duration_api_ms if ergebnis else None,
        "kosten_usd": ergebnis.total_cost_usd if ergebnis else None,
        "num_turns": ergebnis.num_turns if ergebnis else None,
        "subtype": ergebnis.subtype if ergebnis else "kein_ergebnis",
        "is_error": ergebnis.is_error if ergebnis else True,
        "usage": ergebnis.usage if ergebnis else None,
        "model_usage": ergebnis.model_usage if ergebnis else None,
        "schlusstext": ergebnis.result if ergebnis else None,
    }
    (kasten.run_dir / "lauf.json").write_text(json.dumps(lauf, ensure_ascii=False, indent=2), encoding="utf-8")
    return lauf


def lade_aufgaben() -> list[dict]:
    return json.loads(AUFGABEN.read_text(encoding="utf-8"))["aufgaben"]


async def main():
    p = argparse.ArgumentParser()
    p.add_argument("tickets", nargs="*", help="Ticket-IDs, z. B. T01")
    p.add_argument("--alle", action="store_true")
    p.add_argument("--laeufe", type=int, default=1)
    p.add_argument("--ausgabe", default=str(RUNS_DIR))
    p.add_argument("--parallel", type=int, default=3)
    p.add_argument("--prompt", choices=sorted(SYSTEM_PROMPTS), default="v2")
    a = p.parse_args()

    api_key_pruefen()
    aufgaben = lade_aufgaben()
    auswahl = aufgaben if a.alle else [t for t in aufgaben if t["id"] in a.tickets]
    if not auswahl:
        sys.exit("Keine Tickets ausgewählt (IDs angeben oder --alle).")
    ausgabe = Path(a.ausgabe)
    jobs = [(t, f"{t['id']}_lauf{n}") for t in auswahl for n in range(1, a.laeufe + 1)]
    jobs = [(t, r) for t, r in jobs if not (ausgabe / r / "lauf.json").exists()]  # fertige überspringen
    sem = asyncio.Semaphore(a.parallel)

    async def einer(t, r):
        async with sem:
            lauf = await bearbeite_ticket(t, r, ausgabe, a.prompt)
            print(f"{r}: {lauf['subtype']}, {lauf['num_turns']} Turns, {lauf['dauer_s']:.1f} s, "
                  f"{(lauf['kosten_usd'] or 0):.4f} USD", flush=True)

    await asyncio.gather(*(einer(t, r) for t, r in jobs))


if __name__ == "__main__":
    asyncio.run(main())
