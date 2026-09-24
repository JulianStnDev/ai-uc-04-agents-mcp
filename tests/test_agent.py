"""Agent-Konfiguration und PreToolUse-Hook – ohne LLM-Aufruf."""

import asyncio
import json

import pytest

import agent
from werkzeuge import Werkzeugkasten


def test_hook_erlaubt_nur_focusflow(tmp_path):
    k = Werkzeugkasten(run_id="h", runs_dir=tmp_path)
    hook = agent.nur_focusflow_hook(k)
    ok = asyncio.run(hook({"tool_name": "mcp__focusflow__kunde_nachschlagen", "tool_input": {}}, "id1", None))
    assert ok["hookSpecificOutput"]["permissionDecision"] == "allow"
    for name in ["Bash", "Read", "mcp__andere__x", "mcp__focusflowfake__x"]:
        nein = asyncio.run(hook({"tool_name": name, "tool_input": {"a": 1}}, "id2", None))
        assert nein["hookSpecificOutput"]["permissionDecision"] == "deny"
    log = [json.loads(z) for z in (k.run_dir / "trajektorie.jsonl").read_text().splitlines()]
    assert [e["werkzeug"] for e in log] == ["Bash", "Read", "mcp__andere__x", "mcp__focusflowfake__x"]
    assert all(e["blockiert"] and e["fehler"] for e in log)


def test_prompt_enthaelt_keine_falldetails():
    for t in agent.lade_aufgaben():
        prompt = agent.SYSTEM_PROMPT + agent.ticket_prompt(t)
        for verboten in ["DATA_NOTES", t["kernaussage_entwurf"], t["kunde_id"], "Schattenmodus"]:
            assert verboten not in prompt


def test_modell_und_budget_fest():
    assert agent.MODELL == "claude-haiku-4-5"
    assert 0 < agent.MAX_BUDGET_USD <= 1


def test_abbruch_ohne_api_key(monkeypatch):
    monkeypatch.setattr(agent, "load_dotenv", lambda *a, **k: None)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(SystemExit):
        agent.api_key_pruefen()
