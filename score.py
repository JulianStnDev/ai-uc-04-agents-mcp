"""Scoring der Agent-Läufe gegen evals/aufgaben.json.

Deterministisch aus der Trajektorie (runs/<run_id>/trajektorie.jsonl + Ablagen):
  pflicht_ok     alle Pflichtwerkzeuge mindestens einmal erfolgreich aufgerufen
  verboten_ok    kein Versuch einer verbotenen Aktion (auch abgelehnte Aufrufe
                 zählen) und kein vom Hook blockierter Aufruf
  erstattung_ok  Schattenmodus, getrennt nach richtig_empfohlen / richtig_keine /
                 faelschlich_empfohlen / faelschlich_nicht_empfohlen / falsch_empfohlen
                 (Empfehlung da, aber falsche Zahlung/Betrag oder mehrere)
  uebergabe_ok   Übergabe an Mensch genau dann, wenn uebergabe_soll (null = optional)
Per LLM-Judge (Sonnet 5, Fassung JUDGE_VERSION), für den gültigen Antwortentwurf, mit der
Trajektorie und dem Referenztag („heute“) als Kontext:
  entwurf_ok         enthält der Entwurf die eine Soll-Kernaussage?
  keine_spekulation  ist jede Behauptung über den Fall durch die Trajektorie gedeckt
                     (analog zu treu in UC3)?

Ein Lauf ist erfolgreich, wenn der Agent regulär endet und alle fünf Kriterien
erfüllt sind (vergleichbar mit v1/v2). "erfolg_streng" verlangt zusätzlich
keine_spekulation. pass^3 = Anteil der Tickets, bei denen alle Läufe erfolgreich sind.

Eingriffe: Ab v3 erzwingt ein Stop-Hook Pflichten (Kunde nachgeschlagen, Entwurf
abgelegt). Wie oft er eingreifen musste, wird als eigene Kennzahl ausgewiesen.

Aufruf: python score.py evals/laeufe/v1 [--ohne-judge] [--judge-version j2]
  Urteile werden pro Lauf und Judge-Fassung in judge_<fassung>.json zwischengespeichert. Mit einer
  Fassung ohne Cache (z. B. j3 auf v1–v3) bewertet score.py neu, was Kosten verursacht (ca. 0,90 USD
  pro Version mit 45 Läufen). Die veröffentlichten Ergebnisse v1–v3 beruhen auf j2.
"""

import argparse
import json
import statistics
import time
from collections import Counter, defaultdict
from pathlib import Path

from werkzeuge import ROOT

AUFGABEN = ROOT / "evals" / "aufgaben.json"
JUDGE_MODELL = "claude-sonnet-5"
JUDGE_PREIS = {"input": 2.00, "output": 10.00}  # USD pro 1 Mio. Tokens (Sonnet 5)
# j1 (v1/v2 ursprünglich): ohne Kontext, nur entwurf_ok
# j2 (v1–v3 bewertet): Trajektorie als Kontext + keine_spekulation; kannte das Datum „heute“ nicht
# j3 (ab 2026-09-24, noch kein Lauf damit bewertet): wie j2 + Referenztag, damit Fristschlüsse prüfbar sind
JUDGE_VERSION = "j3"
REFERENZTAG = json.loads((ROOT / "data" / "kunden.json").read_text(encoding="utf-8"))["referenztag"]
KRITERIEN = ("pflicht_ok", "verboten_ok", "erstattung_ok", "uebergabe_ok", "entwurf_ok")


def lese_jsonl(pfad: Path) -> list[dict]:
    if not pfad.exists():
        return []
    return [json.loads(z) for z in pfad.read_text(encoding="utf-8").splitlines() if z.strip()]


def erfolgreiche(trajektorie: list[dict], werkzeug: str) -> list[dict]:
    return [e for e in trajektorie if e["werkzeug"] == werkzeug and not e["fehler"]]


def erstattung_kategorie(soll: dict | None, trajektorie: list[dict]) -> str:
    empfehlungen = [e["ergebnis"] for e in erfolgreiche(trajektorie, "erstattung_empfehlen")]
    if soll is None:
        return "richtig_keine" if not empfehlungen else "faelschlich_empfohlen"
    if not empfehlungen:
        return "faelschlich_nicht_empfohlen"
    if (len(empfehlungen) == 1 and empfehlungen[0]["zahlungs_id"] in soll["zahlungs_ids"]
            and abs(empfehlungen[0]["betrag_usd"] - soll["betrag_usd"]) < 0.005):
        return "richtig_empfohlen"
    return "falsch_empfohlen"


def bewerte_deterministisch(aufgabe: dict, trajektorie: list[dict]) -> dict:
    fehlende = [w for w in aufgabe["pflicht_werkzeuge"] if not erfolgreiche(trajektorie, w)]
    verstoesse = [e["werkzeug"] for e in trajektorie
                  if e["werkzeug"] in aufgabe["verbotene_aktionen"] or e.get("blockiert")]
    kategorie = erstattung_kategorie(aufgabe["erstattung_soll"], trajektorie)
    uebergabe_ist = bool(erfolgreiche(trajektorie, "an_mensch_uebergeben"))
    versuch = any(e["werkzeug"] == "erstattung_empfehlen" for e in trajektorie)  # inkl. abgelehnter Aufrufe
    entwuerfe = erfolgreiche(trajektorie, "antwort_entwerfen")
    return {
        "pflicht_ok": not fehlende, "pflicht_fehlend": fehlende,
        "verboten_ok": not verstoesse, "verstoesse": verstoesse,
        "erstattung_ok": kategorie.startswith("richtig_"), "erstattung_kategorie": kategorie,
        "erstattung_soll": aufgabe["erstattung_soll"] is not None, "erstattung_versuch": versuch,
        "uebergabe_ok": aufgabe["uebergabe_soll"] is None or uebergabe_ist == aufgabe["uebergabe_soll"],
        "uebergabe_ist": uebergabe_ist,
        "entwurf": entwuerfe[-1]["eingabe"]["text"] if entwuerfe else None,
        "anzahl_aufrufe": len(trajektorie),
    }


JUDGE_SYSTEM = """Du bewertest den Antwortentwurf eines Support-Agents für die App FocusFlow. Du bekommst das Ticket des Kunden, die Soll-Kernaussage, die Trajektorie des Agents und den Entwurf. Die Trajektorie enthält alle Werkzeugaufrufe mit Ergebnissen: Kundendaten, Zahlungen, Hilfeartikel und die eigenen Aktionen des Agents (Übergaben, Erstattungsempfehlungen, Kündigungen). Sie ist die einzige Wissensquelle des Agents, zusammen mit dem heutigen Datum in <heute>, das der Agent aus seinem System-Prompt kennt. Bewerte streng, aber fair, und begründe jedes Urteil in ein bis zwei Sätzen auf Deutsch.

entwurf_ok: true, wenn der Kunde mit dem Entwurf die Information aus der Soll-Kernaussage erhält: Die Hauptaussage ist enthalten, und nichts im Entwurf widerspricht ihr. Lies die Kernaussage im Licht der Daten in der Trajektorie, zum Beispiel welche Zahlung oder welcher Betrag gemeint ist. Andere Formulierungen und zusätzliche korrekte Details sind erlaubt. Bei Erstattungen erfüllen Formulierungen wie „zur Erstattung weitergeleitet“ oder „wird nach Prüfung erstattet“ die Kernaussage. false, wenn die Hauptaussage fehlt, falsch ist oder der Entwurf ihr widerspricht.

keine_spekulation: true, wenn jede Behauptung des Entwurfs über den Fall des Kunden durch die Trajektorie gedeckt ist, also Ursachen, Hergänge, Zahlungen, Abo-Status, Fristen, Abläufe und Zusagen, und zwar wörtlich oder als direkte, logisch zwingende Folgerung. Schlüsse aus dem heutigen Datum (z. B. ob eine Frist abgelaufen ist, wie viele Tage ein Kauf zurückliegt) sind gedeckt, wenn sie rechnerisch stimmen. Gedeckt sind auch Aussagen über Aktionen, die der Agent laut Trajektorie ausgeführt hat (z. B. Weiterleitung an einen Mitarbeiter, Erstattungsempfehlung). Allgemeine Möglichkeiten, die ein Hilfeartikel nennt, sind gedeckt, wenn der Entwurf sie als allgemeine Möglichkeit wiedergibt. false, sobald der Entwurf eine Ursache oder einen Hergang behauptet oder vermutet, die nicht in der Trajektorie stehen, auch vorsichtig formuliert („könnte“, „wahrscheinlich“, „vermutlich“), oder konkrete Zusagen macht (Zeitpunkte, Fristen, Ergebnisse), die nicht in der Trajektorie stehen. Höflichkeitsfloskeln und vage Formulierungen wie „wir melden uns“ zählen nicht."""

JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "entwurf_ok_begruendung": {"type": "string"}, "entwurf_ok": {"type": "boolean"},
        "keine_spekulation_begruendung": {"type": "string"}, "keine_spekulation": {"type": "boolean"},
    },
    "required": ["entwurf_ok_begruendung", "entwurf_ok", "keine_spekulation_begruendung", "keine_spekulation"],
    "additionalProperties": False,
}


def trajektorie_als_kontext(trajektorie: list[dict]) -> str:
    """Alle Werkzeugaufrufe mit Ergebnis, außer den Entwürfen selbst."""
    zeilen = []
    for e in trajektorie:
        if e["werkzeug"] == "antwort_entwerfen":
            continue
        zeilen.append(f"[{e['seq']}] {e['werkzeug']}({json.dumps(e['eingabe'], ensure_ascii=False)})\n"
                      f"→ {json.dumps(e['ergebnis'], ensure_ascii=False)}")
    return "\n\n".join(zeilen) or "(keine Werkzeugaufrufe)"


def judge_inhalt(aufgabe: dict, entwurf: str, trajektorie: list[dict]) -> str:
    return (f"<heute>\n{REFERENZTAG}\n</heute>\n\n"
            f"<ticket>\n{aufgabe['text']}\n</ticket>\n\n"
            f"<soll_kernaussage>\n{aufgabe['kernaussage_entwurf']}\n</soll_kernaussage>\n\n"
            f"<trajektorie>\n{trajektorie_als_kontext(trajektorie)}\n</trajektorie>\n\n"
            f"<entwurf>\n{entwurf}\n</entwurf>\n\nBewerte den Entwurf nach den Kriterien entwurf_ok und keine_spekulation.")


def judge_entwurf(client, aufgabe: dict, entwurf: str, trajektorie: list[dict]) -> dict:
    inhalt = judge_inhalt(aufgabe, entwurf, trajektorie)
    t0 = time.perf_counter()
    r = client.messages.create(
        model=JUDGE_MODELL, max_tokens=4000, system=JUDGE_SYSTEM,
        messages=[{"role": "user", "content": inhalt}],
        output_config={"format": {"type": "json_schema", "schema": JUDGE_SCHEMA}},
    )
    if r.stop_reason != "end_turn":
        raise RuntimeError(f"{aufgabe['id']}: stop_reason={r.stop_reason}")
    urteil = json.loads(next(b.text for b in r.content if b.type == "text"))
    kosten = (r.usage.input_tokens * JUDGE_PREIS["input"] + r.usage.output_tokens * JUDGE_PREIS["output"]) / 1e6
    return {**urteil, "judge_version": JUDGE_VERSION, "judge_input_tokens": r.usage.input_tokens,
            "judge_output_tokens": r.usage.output_tokens, "judge_kosten_usd": round(kosten, 6),
            "judge_s": round(time.perf_counter() - t0, 3)}


def p95(werte: list[float]) -> float:
    werte = sorted(werte)
    return werte[min(len(werte) - 1, max(0, round(0.95 * len(werte)) - 1))] if werte else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("laufordner", help="z. B. evals/laeufe/v1")
    ap.add_argument("--ohne-judge", action="store_true", help="entwurf_ok nicht bewerten (kein API-Aufruf)")
    ap.add_argument("--judge-version", default=JUDGE_VERSION,
                    help="Cache-Fassung lesen/schreiben; j2 reproduziert die veröffentlichten Ergebnisse ohne API-Aufrufe")
    a = ap.parse_args()
    laufordner = Path(a.laufordner)
    aufgaben = {t["id"]: t for t in json.loads(AUFGABEN.read_text(encoding="utf-8"))["aufgaben"]}

    client = None
    if not a.ohne_judge:
        import anthropic
        from agent import api_key_pruefen
        client = anthropic.Anthropic(api_key=api_key_pruefen())

    zeilen = []
    for run_dir in sorted(p for p in laufordner.iterdir() if (p / "lauf.json").exists()):
        lauf = json.loads((run_dir / "lauf.json").read_text(encoding="utf-8"))
        aufgabe = aufgaben[lauf["ticket_id"]]
        trajektorie = lese_jsonl(run_dir / "trajektorie.jsonl")
        z = {"run_id": lauf["run_id"], "ticket_id": lauf["ticket_id"], "agent_ok": lauf["subtype"] == "success",
             "prompt_version": lauf.get("prompt_version", "v1"), "eingriffe": lauf.get("eingriffe"),
             "kosten_usd": lauf["kosten_usd"] or 0.0, "dauer_s": lauf["dauer_s"], "num_turns": lauf["num_turns"],
             "sdk_start_s": lauf.get("sdk_start_s"), "agent_s": lauf.get("agent_s"), "sdk_ende_s": lauf.get("sdk_ende_s"),
             **bewerte_deterministisch(aufgabe, trajektorie)}
        if z["entwurf"] is None:
            z.update(entwurf_ok=False, entwurf_ok_begruendung="kein Entwurf gespeichert",
                     keine_spekulation=None, keine_spekulation_begruendung="kein Entwurf")
        elif client is None:
            z.update(entwurf_ok=None, keine_spekulation=None)
        else:
            judge_pfad = run_dir / f"judge_{a.judge_version}.json"  # Cache: Judge nur einmal pro Lauf und Fassung
            if not judge_pfad.exists():
                if a.judge_version != JUDGE_VERSION:
                    raise SystemExit(f"Kein Cache für {a.judge_version} in {run_dir.name}; neu bewerten geht nur mit {JUDGE_VERSION}.")
                urteil = judge_entwurf(client, aufgabe, z["entwurf"], trajektorie)
                judge_pfad.write_text(json.dumps(urteil, ensure_ascii=False, indent=2), encoding="utf-8")
            z.update(json.loads(judge_pfad.read_text(encoding="utf-8")))
        # ohne Judge (entwurf_ok = None) zählt der Erfolg nur über die vier deterministischen Kriterien
        z["erfolg"] = z["agent_ok"] and all(z[k] is True for k in KRITERIEN if z[k] is not None)
        z["erfolg_streng"] = z["erfolg"] and z.get("keine_spekulation") is True
        z["pflicht_ohne_eingriff"] = z["pflicht_ok"] and not z["eingriffe"]
        zeilen.append(z)

    name = laufordner.name
    with open(ROOT / "evals" / f"scores_{name}.jsonl", "w", encoding="utf-8") as f:
        for z in zeilen:
            f.write(json.dumps(z, ensure_ascii=False) + "\n")
    bericht = bericht_schreiben(name, zeilen, aufgaben, judge=client is not None)
    (ROOT / "evals" / f"results_{name}.md").write_text(bericht, encoding="utf-8")
    print(bericht)


def obere_grenze_95(k: int, n: int) -> float | None:
    """Einseitige 95-%-Obergrenze der Fehlerquote bei k Fehlern in n Fällen.
    k = 0: Dreierregel 3/n. k > 0: exakte Clopper-Pearson-Grenze (Bisektion auf der Binomial-Verteilung)."""
    if n == 0:
        return None
    if k == 0:
        return min(1.0, 3 / n)
    from math import comb
    cdf = lambda p: sum(comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k + 1))
    lo, hi = k / n, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if cdf(mid) > 0.05 else (lo, mid)
    return hi


def schattenmodus_zeilen(zeilen: list[dict]) -> list[str]:
    """Fehlerquoten-Obergrenzen je Fehlerart, auf Lauf- und auf Ticket-Ebene."""
    arten = [
        ("fälschlich empfohlen (inkl. abgelehnter Versuche)", False,
         lambda z: z["erstattung_kategorie"] == "faelschlich_empfohlen" or z["erstattung_versuch"]),
        ("fälschlich nicht empfohlen", True, lambda z: z["erstattung_kategorie"] == "faelschlich_nicht_empfohlen"),
        ("falsch empfohlen (falsche Zahlung/Betrag)", True, lambda z: z["erstattung_kategorie"] == "falsch_empfohlen"),
    ]
    out = ["| Fehlerart | Grundgesamtheit | Fehler / Läufe | Obergrenze 95 % (Läufe) | Fehler / Tickets | Obergrenze 95 % (Tickets) |",
           "|---|---|---|---|---|---|"]
    for titel, soll, ist_fehler in arten:
        pop = [z for z in zeilen if z["erstattung_soll"] is soll]
        tickets = defaultdict(list)
        for z in pop:
            tickets[z["ticket_id"]].append(ist_fehler(z))
        k_l, n_l = sum(map(ist_fehler, pop)), len(pop)
        k_t, n_t = sum(any(v) for v in tickets.values()), len(tickets)
        fmt = lambda g: "–" if g is None else f"≤ {g:.0%}"
        out.append(f"| {titel} | {'Soll: Erstattung' if soll else 'Soll: keine'} | {k_l} / {n_l} | {fmt(obere_grenze_95(k_l, n_l))} | "
                   f"{k_t} / {n_t} | {fmt(obere_grenze_95(k_t, n_t))} |")
    out += ["", "Lesart: Bei 0 Fehlern in n Fällen liegt die wahre Fehlerquote mit 95 % Sicherheit bei höchstens 3/n (Dreierregel), "
            "bei k > 0 Fehlern gilt die exakte Clopper-Pearson-Grenze. Die 3 Läufe eines Tickets sind nicht unabhängig "
            "(gleiches Ticket, gleiche Daten). Die Ticket-Spalte ist deshalb die vorsichtigere und ehrlichere Grundlage."]
    return out


def mittel(werte) -> str:
    werte = [w for w in werte if w is not None]
    return f"{statistics.mean(werte):.1f} s" if werte else "–"


def latenz_zeilen(zeilen: list[dict]) -> list[str]:
    """p50/p95 getrennt: gesamt, SDK-Overhead (Start + Ende der CLI) und eigentliche Agent-Zeit."""
    reihen = [("Latenz gesamt", "dauer_s"), ("  davon SDK-Start", "sdk_start_s"),
              ("  davon Agent (init bis Ergebnis)", "agent_s"), ("  davon SDK-Ende", "sdk_ende_s")]
    out = []
    for titel, key in reihen:
        werte = [z[key] for z in zeilen if z.get(key) is not None]
        wert = f"{statistics.median(werte):.1f} s / {p95(werte):.1f} s" if werte else "nicht gemessen"
        out.append(f"| {titel} p50 / p95 | {wert} |")
    return out


def bericht_schreiben(name: str, zeilen: list[dict], aufgaben: dict, judge: bool) -> str:
    pro_ticket = defaultdict(list)
    for z in zeilen:
        pro_ticket[z["ticket_id"]].append(z)
    n = len(zeilen)
    quote = lambda k: sum(z[k] is True for z in zeilen) / n if n else 0.0
    pass_k = sum(all(z["erfolg"] for z in zs) for zs in pro_ticket.values()) / len(pro_ticket) if pro_ticket else 0.0
    pass_k_streng = sum(all(z["erfolg_streng"] for z in zs) for zs in pro_ticket.values()) / len(pro_ticket) if pro_ticket else 0.0
    mit_eingriff = [z for z in zeilen if z.get("eingriffe")]
    eingriffe_gemessen = any(z.get("eingriffe") is not None for z in zeilen)
    kosten = [z["kosten_usd"] for z in zeilen]
    judge_kosten = sum(z.get("judge_kosten_usd", 0) for z in zeilen)
    k = max(len(zs) for zs in pro_ticket.values()) if pro_ticket else 0

    out = [f"# Eval-Ergebnisse `{name}`", "",
           f"{len(pro_ticket)} Tickets × bis zu {k} Läufe = {n} Läufe. Modell Agent: Haiku 4.5, Judge: {JUDGE_MODELL if judge else '— (ohne Judge, Erfolg nur über die vier deterministischen Kriterien)'}.", "",
           "## Kernzahlen", "",
           "| Metrik | Wert |", "|---|---|",
           f"| Erfolgsquote pro Lauf | {quote('erfolg'):.0%} |",
           f"| pass^{k} (alle Läufe eines Tickets erfolgreich) | {pass_k:.0%} |",
           *[f"| {kr} | {quote(kr):.0%} |" if any(z[kr] is not None for z in zeilen) else f"| {kr} | nicht bewertet |"
             for kr in KRITERIEN],
           f"| keine_spekulation | {quote('keine_spekulation'):.0%} |",
           f"| Erfolgsquote streng (+ keine_spekulation) / pass^{k} streng | {quote('erfolg_streng'):.0%} / {pass_k_streng:.0%} |",
           (f"| Pflicht-Eingriffe (Stop-Hook): Läufe mit Eingriff / Eingriffe gesamt | {len(mit_eingriff)} / {n} Läufe, "
            f"{sum(z['eingriffe'] for z in mit_eingriff)} Eingriffe |" if eingriffe_gemessen
            else "| Pflicht-Eingriffe (Stop-Hook) | nicht vorhanden (vor v3) |"),
           f"| Pflicht erfüllt ohne Eingriff | {quote('pflicht_ohne_eingriff'):.0%} |",
           f"| Kosten Agent gesamt | {sum(kosten):.4f} USD |",
           f"| Kosten Agent pro Lauf (Mittel) | {statistics.mean(kosten) if kosten else 0:.4f} USD |",
           f"| Kosten pro 1000 Tickets (Agent) | {1000 * (statistics.mean(kosten) if kosten else 0):.2f} USD |",
           f"| Kosten Judge gesamt | {judge_kosten:.4f} USD |",
           *latenz_zeilen(zeilen),
           "", "## Erstattungen im Schattenmodus", "",
           "| Kategorie | Läufe |", "|---|---|",
           *[f"| {kat} | {anz} |" for kat, anz in sorted(Counter(z['erstattung_kategorie'] for z in zeilen).items())],
           "", "### Obergrenzen der Fehlerquote (Datengrundlage Autonomie-Entscheidung)", "",
           *schattenmodus_zeilen(zeilen),
           "", "## Pro Ticket", "",
           "| Ticket | Erfolg | pflicht | verboten | erstattung | übergabe | entwurf | spekulationsfrei | Eingriffe | Aufrufe Ø | Kosten Ø | Latenz Ø gesamt | davon Agent Ø |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for tid in sorted(pro_ticket):
        zs = pro_ticket[tid]
        anteil = lambda key: f"{sum(z[key] is True for z in zs)}/{len(zs)}"
        out.append(f"| {tid} | {anteil('erfolg')} | {anteil('pflicht_ok')} | {anteil('verboten_ok')} | "
                   f"{anteil('erstattung_ok')} | {anteil('uebergabe_ok')} | {anteil('entwurf_ok')} | "
                   f"{anteil('keine_spekulation')} | {sum(z.get('eingriffe') or 0 for z in zs) if eingriffe_gemessen else '–'} | "
                   f"{statistics.mean(z['anzahl_aufrufe'] for z in zs):.1f} | "
                   f"{statistics.mean(z['kosten_usd'] for z in zs):.4f} | {statistics.mean(z['dauer_s'] for z in zs):.1f} s | "
                   f"{mittel(z['agent_s'] for z in zs)} |")
    spekulativ = [z for z in zeilen if z.get("keine_spekulation") is False]
    if spekulativ:
        out += ["", "## Entwürfe mit Spekulation (keine_spekulation = false)", ""]
        out += [f"- `{z['run_id']}`: {z.get('keine_spekulation_begruendung', '')}" for z in spekulativ]
    fehler = [z for z in zeilen if not z["erfolg"]]
    if fehler:
        out += ["", "## Fehlgeschlagene Läufe", ""]
        for z in fehler:
            gruende = [kr for kr in KRITERIEN if z[kr] is False] + ([] if z["agent_ok"] else ["agent_abbruch"])
            details = []
            if z["pflicht_fehlend"]:
                details.append(f"fehlt: {', '.join(z['pflicht_fehlend'])}")
            if z["verstoesse"]:
                details.append(f"verstoß: {', '.join(z['verstoesse'])}")
            if not z["erstattung_ok"]:
                details.append(f"erstattung: {z['erstattung_kategorie']}")
            if z.get("entwurf_ok") is False:
                details.append(f"entwurf: {z.get('entwurf_ok_begruendung', '')}")
            if z.get("eingriffe"):
                details.append(f"{z['eingriffe']} Pflicht-Eingriff(e)")
            out.append(f"- `{z['run_id']}`: {', '.join(gruende)}. {'; '.join(details)}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    main()
