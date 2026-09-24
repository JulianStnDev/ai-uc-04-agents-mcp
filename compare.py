"""Vergleich zweier Eval-Läufe (z. B. v1 vs. v2) je Metrik und je Ticket.

Liest evals/scores_<a>.jsonl und evals/scores_<b>.jsonl (von score.py erzeugt)
und schreibt evals/vergleich_<a>_<b>.md. Besonders wichtig sind Tickets, die
schlechter werden: Ein Prompt-Fix für einige Tickets kann andere verschlechtern
(Kopplungseffekt).

Aufruf: python compare.py v1 v2 [--fall T13:5 --fall T14:1] [--einordnung evals/einordnung_v1_v2.md]
  --fall TICKET:REGEL schreibt ein Fallbeispiel komplett aus (Ticket, Prompt-Regel
  aus v2 samt v1-Fassung, Werkzeugaufrufe, Entwurf, Judge-Urteil, jeweils v1 und v2).
"""

import argparse
import json
import re
import statistics
from collections import defaultdict

from score import KRITERIEN, p95
from werkzeuge import ROOT


def lade(name: str) -> dict[str, list[dict]]:
    pro_ticket = defaultdict(list)
    for zeile in (ROOT / "evals" / f"scores_{name}.jsonl").read_text(encoding="utf-8").splitlines():
        z = json.loads(zeile)
        pro_ticket[z["ticket_id"]].append(z)
    return pro_ticket


def kennzahlen(pt: dict[str, list[dict]]) -> dict[str, float]:
    alle = [z for zs in pt.values() for z in zs]
    q = lambda key: sum(z[key] is True for z in alle) / len(alle)
    werte = lambda key: [z[key] for z in alle if z.get(key) is not None]
    return {
        "Erfolgsquote pro Lauf": q("erfolg"),
        "pass^3": sum(all(z["erfolg"] for z in zs) for zs in pt.values()) / len(pt),
        **{k: q(k) for k in KRITERIEN},
        "Kosten pro Ticket (USD)": statistics.mean(werte("kosten_usd")),
        "Werkzeugaufrufe pro Ticket": statistics.mean(werte("anzahl_aufrufe")),
        "Latenz p50 (s)": statistics.median(werte("dauer_s")),
        "Latenz p95 (s)": p95(werte("dauer_s")),
        "Agent-Zeit p95 (s)": p95(werte("agent_s")),
    }


# v2-Regel -> entsprechende v1-Regel (None = in v2 neu)
REGEL_V1 = {1: 1, 2: 2, 3: 3, 4: 4, 5: None, 6: 5}


def regel(prompt: str, nr: int | None) -> str:
    if nr is None:
        return "(in dieser Fassung nicht vorhanden)"
    m = re.search(rf"^{nr}\. (.+)$", prompt, re.M)
    return m.group(1) if m else "?"


def kernergebnis(e: dict) -> str:
    r = e["ergebnis"]
    if e["fehler"]:
        return f"FEHLER: {r.get('fehler', '')}"
    w = e["werkzeug"]
    if w == "kunde_nachschlagen":
        return "; ".join(f"{k['kunden_id']} {k['abo']['stufe']}, {k['abo']['anbieter'] or '–'}, {k['abo']['status'] or '–'}"
                         for k in r["treffer"]) or "kein Treffer"
    if w == "zahlungen_ansehen":
        return f"{len(r['zahlungen'])} Zahlungen" + (": " + ", ".join(
            f"{z['zahlungs_id']} {z['datum']} {z['betrag_usd']:.2f} {z['anbieter']}" for z in r["zahlungen"][-3:]) if r["zahlungen"] else "")
    if w == "hilfe_durchsuchen":
        return ", ".join(f"{t['datei']} ({t['stand']})" for t in r["treffer"]) or "keine Treffer"
    if w == "erstattung_empfehlen":
        return f"Empfehlung {r['zahlungs_id']} {r['betrag_usd']:.2f} USD, {r['status']}"
    if w == "abo_kuendigen":
        return f"gekündigt zum {r['wirksam_zum']}"
    if w == "an_mensch_uebergeben":
        return f"Übergabe {r['uebergabe_id']} ({r['prioritaet']})"
    if w == "antwort_entwerfen":
        return "Entwurf gespeichert"
    return json.dumps(r, ensure_ascii=False)[:120]


def eingabe_kurz(e: dict) -> str:
    ein = dict(e["eingabe"])
    if e["werkzeug"] == "antwort_entwerfen":
        ein["text"] = "(siehe Entwurf)"
    t = json.dumps(ein, ensure_ascii=False)
    return (t[:260] + " …") if len(t) > 260 else t


def zelle(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def lauf_block(version: str, z: dict) -> list[str]:
    run_dir = ROOT / "evals" / "laeufe" / version / z["run_id"]
    traj = [json.loads(x) for x in (run_dir / "trajektorie.jsonl").read_text(encoding="utf-8").splitlines()]
    out = [f"**{version}, `{z['run_id']}`**: {'bestanden' if z['erfolg'] else 'nicht bestanden'} "
           f"({', '.join(f'{k} {chr(10003) if z[k] else chr(10007)}' for k in KRITERIEN)}; "
           f"{z['anzahl_aufrufe']} Aufrufe, {z['dauer_s']:.1f} s, {z['kosten_usd']:.4f} USD)", "",
           "| # | Werkzeug | Eingabe | Kernergebnis |", "|---|---|---|---|"]
    out += [f"| {e['seq']} | {e['werkzeug']} | {zelle(eingabe_kurz(e))} | {zelle(kernergebnis(e))} |" for e in traj]
    out += ["", "Entwurf:", ""] + ["> " + zeile for zeile in (z["entwurf"] or "(kein Entwurf)").splitlines()]
    out += ["", f"Judge (entwurf_ok = {z.get('entwurf_ok')}): {z.get('entwurf_ok_begruendung', '–')}", ""]
    return out


def waehle_lauf(zs: list[dict], erfolg: bool | None) -> dict:
    """Erster Lauf mit dem gewünschten Ergebnis. None = mehrheitliches Ergebnis des Tickets."""
    if erfolg is None:
        erfolg = sum(z["erfolg"] for z in zs) * 2 > len(zs)
    zs = sorted(zs, key=lambda z: z["run_id"])
    return next((z for z in zs if z["erfolg"] == erfolg), zs[0])


def fallbeispiel(tid: str, nr: int, a: str, b: str, A: dict, B: dict) -> list[str]:
    import agent
    ticket = next(t for t in agent.lade_aufgaben() if t["id"] == tid)
    ea, eb = sum(z["erfolg"] for z in A[tid]), sum(z["erfolg"] for z in B[tid])
    out = [f"### {tid}: {ea}/{len(A[tid])} in {a} → {eb}/{len(B[tid])} in {b}", "",
           f"Ticket (von {ticket['absender']}):", "", f"> {ticket['text']}", "",
           f"Soll: Übergabe {'ja' if ticket['uebergabe_soll'] else 'nein'}, "
           f"Erstattung {ticket['erstattung_soll'] or 'keine'}, verboten: {', '.join(ticket['verbotene_aktionen']) or '–'}. "
           f"Kernaussage: „{ticket['kernaussage_entwurf']}“", "",
           f"Relevante Prompt-Regel ({b}, Nr. {nr}):", "", f"> {regel(agent.SYSTEM_PROMPT_V2, nr)}", "",
           f"Dieselbe Regel in {a}:", "", f"> {regel(agent.SYSTEM_PROMPT_V1, REGEL_V1[nr])}", ""]
    # Besser: gescheiterter Lauf vorher vs. bestandener nachher; schlechter: umgekehrt; gleich: jeweils Mehrheit
    vorher, nachher = (False, True) if eb > ea else (True, False) if eb < ea else (None, None)
    out += lauf_block(a, waehle_lauf(A[tid], vorher)) + lauf_block(b, waehle_lauf(B[tid], nachher))
    return out


def main(a: str, b: str, faelle: list[str], einordnung: str | None = None):
    A, B = lade(a), lade(b)
    ka, kb = kennzahlen(A), kennzahlen(B)
    out = [f"# Vergleich `{a}` vs. `{b}`", "", "## Je Metrik", "", f"| Metrik | {a} | {b} | Δ |", "|---|---|---|---|"]
    for key in ka:
        prozent = "USD" not in key and "(s)" not in key and "Werkzeug" not in key
        fmt = (lambda x: f"{x:.0%}") if prozent else (lambda x: f"{x:.4f}" if "USD" in key else f"{x:.1f}")
        delta = kb[key] - ka[key]
        d = f"{delta * 100:+.0f} Pp." if prozent else (f"{delta:+.4f}" if "USD" in key else f"{delta:+.1f}")
        out.append(f"| {key} | {fmt(ka[key])} | {fmt(kb[key])} | {d} |")

    out += ["", "## Je Ticket", "",
            f"| Ticket | Erfolg {a} | Erfolg {b} | Trend | Veränderte Kriterien ({a} → {b}) |", "|---|---|---|---|---|"]
    besser, schlechter = [], []
    for tid in sorted(set(A) | set(B)):
        ea, eb = sum(z["erfolg"] for z in A[tid]), sum(z["erfolg"] for z in B[tid])
        trend = "besser" if eb > ea else "schlechter" if eb < ea else "gleich"
        (besser if trend == "besser" else schlechter if trend == "schlechter" else []).append(tid)
        diffs = []
        for k in KRITERIEN:
            ca, cb = sum(z[k] is True for z in A[tid]), sum(z[k] is True for z in B[tid])
            if ca != cb:
                diffs.append(f"{k} {ca}/{len(A[tid])} → {cb}/{len(B[tid])}")
        out.append(f"| {tid} | {ea}/{len(A[tid])} | {eb}/{len(B[tid])} | {trend} | {'; '.join(diffs) or '–'} |")

    out += ["", "## Kopplungseffekt", "",
            f"- Besser geworden: {', '.join(besser) or 'keins'}",
            f"- Schlechter geworden: {', '.join(schlechter) or 'keins'}"]
    for tid in schlechter:
        for z in B[tid]:
            if not z["erfolg"]:
                gruende = [k for k in KRITERIEN if z[k] is False]
                detail = z.get("entwurf_ok_begruendung", "") if z.get("entwurf_ok") is False else ""
                out.append(f"  - `{z['run_id']}`: {', '.join(gruende)}. {detail}".rstrip())
    if einordnung:
        out += ["", (ROOT / einordnung).read_text(encoding="utf-8").strip()]
    if faelle:
        out += ["", "## Fallbeispiele", "",
                "Auswahl der Läufe: Bei einem verbesserten Ticket steht ein gescheiterter Lauf der alten Version neben einem "
                "bestandenen der neuen, bei einem verschlechterten umgekehrt (jeweils der erste passende Lauf). Die Zählung x/3 "
                "in der Überschrift zeigt, wie typisch der gezeigte Lauf ist.", ""]
        for f in faelle:
            tid, nr = f.split(":")
            out += fallbeispiel(tid, int(nr), a, b, A, B)
    text = "\n".join(out) + "\n"
    (ROOT / "evals" / f"vergleich_{a}_{b}.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--fall", action="append", default=[], help="TICKET:REGELNR (Regel im Prompt von b)")
    ap.add_argument("--einordnung", help="Markdown-Datei mit manueller Einordnung, wird nach dem Kopplungseffekt eingefügt")
    x = ap.parse_args()
    main(x.a, x.b, x.fall, x.einordnung)
