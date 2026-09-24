"""Vergleich mehrerer Eval-Läufe (z. B. v1, v2, v3) je Metrik und je Ticket.

Liest evals/scores_<version>.jsonl (von score.py erzeugt) und schreibt
evals/vergleich_<v1>_<v2>_..md. Besonders wichtig sind Tickets, die schlechter
werden: Ein Prompt-Fix für einige Tickets kann andere verschlechtern
(Kopplungseffekt).

Aufruf:
  python compare.py v1 v2 v3 --fall T14:Konto --fall T13:Vermute --einordnung evals/einordnung_v1_v2_v3.md
  --fall TICKET:STICHWORT schreibt ein Fallbeispiel komplett aus. Das Stichwort findet die
  relevante Regel in jedem Prompt (die Nummern unterscheiden sich zwischen den Versionen).
"""

import argparse
import json
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


def kennzahlen(pt: dict[str, list[dict]]) -> dict[str, float | None]:
    alle = [z for zs in pt.values() for z in zs]
    q = lambda key: sum(z.get(key) is True for z in alle) / len(alle)
    werte = lambda key: [z[key] for z in alle if z.get(key) is not None]
    eingriffe = werte("eingriffe")
    return {
        "Erfolgsquote pro Lauf": q("erfolg"),
        "pass^3": sum(all(z["erfolg"] for z in zs) for zs in pt.values()) / len(pt),
        **{k: q(k) for k in KRITERIEN},
        "keine_spekulation": q("keine_spekulation"),
        "Erfolgsquote streng (+ keine_spekulation)": q("erfolg_streng"),
        "pass^3 streng": sum(all(z["erfolg_streng"] for z in zs) for zs in pt.values()) / len(pt),
        "Pflicht erfüllt ohne Eingriff": q("pflicht_ohne_eingriff"),
        "Läufe mit Pflicht-Eingriff": (sum(1 for e in eingriffe if e) / len(alle)) if eingriffe else None,
        "Kosten pro Ticket (USD)": statistics.mean(werte("kosten_usd")),
        "Werkzeugaufrufe pro Ticket": statistics.mean(werte("anzahl_aufrufe")),
        "Latenz p50 (s)": statistics.median(werte("dauer_s")),
        "Latenz p95 (s)": p95(werte("dauer_s")),
    }


def fmt(key: str, x) -> str:
    if x is None:
        return "–"
    if "USD" in key:
        return f"{x:.4f}"
    if "(s)" in key or "Werkzeug" in key:
        return f"{x:.1f}"
    return f"{x:.0%}"


def regel(prompt: str, stichwort: str) -> str:
    treffer = [z for z in prompt.splitlines() if stichwort in z and z[:2].rstrip(".").isdigit()]
    return treffer[0] if treffer else "(in dieser Fassung nicht vorhanden)"


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
        return "Entwurf gespeichert" + (f" (ersetzt {r['ersetzt']})" if r.get("ersetzt") else "")
    return json.dumps(r, ensure_ascii=False)[:120]


def eingabe_kurz(e: dict) -> str:
    ein = dict(e["eingabe"])
    if e["werkzeug"] == "antwort_entwerfen":
        ein["text"] = "(siehe Entwurf)" if not e["fehler"] else str(ein.get("text", ""))[:40] + " …"
    t = json.dumps(ein, ensure_ascii=False)
    return (t[:260] + " …") if len(t) > 260 else t


def zelle(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def haken(x) -> str:
    return "–" if x is None else ("✓" if x else "✗")


def lauf_block(version: str, z: dict) -> list[str]:
    run_dir = ROOT / "evals" / "laeufe" / version / z["run_id"]
    traj = [json.loads(x) for x in (run_dir / "trajektorie.jsonl").read_text(encoding="utf-8").splitlines()]
    kriterien = ", ".join(f"{k} {haken(z.get(k))}" for k in (*KRITERIEN, "keine_spekulation"))
    eingriff = f", {z['eingriffe']} Pflicht-Eingriff(e)" if z.get("eingriffe") else ""
    out = [f"**{version}, `{z['run_id']}`**: {'bestanden' if z['erfolg'] else 'nicht bestanden'} "
           f"({kriterien}; {z['anzahl_aufrufe']} Aufrufe{eingriff}, {z['dauer_s']:.1f} s, {z['kosten_usd']:.4f} USD)", "",
           "| # | Werkzeug | Eingabe | Kernergebnis |", "|---|---|---|---|"]
    out += [f"| {e['seq']} | {e['werkzeug']} | {zelle(eingabe_kurz(e))} | {zelle(kernergebnis(e))} |" for e in traj]
    out += ["", "Entwurf:", ""] + ["> " + zeile for zeile in (z["entwurf"] or "(kein Entwurf)").splitlines()]
    out += ["", f"Judge: entwurf_ok = {z.get('entwurf_ok')}: {z.get('entwurf_ok_begruendung', '–')}", "",
            f"keine_spekulation = {z.get('keine_spekulation')}: {z.get('keine_spekulation_begruendung', '–')}", ""]
    return out


def waehle_lauf(zs: list[dict], erfolg: bool | None) -> dict:
    """Erster Lauf mit dem gewünschten Ergebnis. None = mehrheitliches Ergebnis des Tickets."""
    if erfolg is None:
        erfolg = sum(z["erfolg"] for z in zs) * 2 > len(zs)
    zs = sorted(zs, key=lambda z: z["run_id"])
    return next((z for z in zs if z["erfolg"] == erfolg), zs[0])


def fallbeispiel(tid: str, stichwort: str, versionen: list[str], daten: dict) -> list[str]:
    import agent
    ticket = next(t for t in agent.lade_aufgaben() if t["id"] == tid)
    erfolge = {v: sum(z["erfolg"] for z in daten[v][tid]) for v in versionen}
    letzte = versionen[-1]
    ueber = " → ".join(f"{erfolge[v]}/{len(daten[v][tid])} in {v}" for v in versionen)
    soll_ueb = {True: "ja", False: "nein", None: "optional"}[ticket["uebergabe_soll"]]
    out = [f"### {tid}: {ueber}", "",
           f"Ticket (von {ticket['absender']}):", "", f"> {ticket['text']}", "",
           f"Soll: Übergabe {soll_ueb}, Erstattung {ticket['erstattung_soll'] or 'keine'}, "
           f"verboten: {', '.join(ticket['verbotene_aktionen']) or '–'}. Kernaussage: „{ticket['kernaussage_entwurf']}“", "",
           "Relevante Prompt-Regel je Version:", ""]
    out += [f"- **{v}:** {regel(agent.SYSTEM_PROMPTS[v], stichwort)}" for v in versionen] + [""]
    # Letzte Version: das Ergebnis, das den Trend zeigt; frühere Versionen: nach Möglichkeit das Gegenteil
    besser = erfolge[letzte] > max(erfolge[v] for v in versionen[:-1])
    schlechter = erfolge[letzte] < min(erfolge[v] for v in versionen[:-1])
    ziel = True if besser else False if schlechter else None
    for v in versionen[:-1]:
        out += lauf_block(v, waehle_lauf(daten[v][tid], None if ziel is None else not ziel))
    out += lauf_block(letzte, waehle_lauf(daten[letzte][tid], ziel))
    return out


def main(versionen: list[str], faelle: list[str], einordnung: str | None):
    daten = {v: lade(v) for v in versionen}
    kz = {v: kennzahlen(daten[v]) for v in versionen}
    kopf = " | ".join(versionen)
    out = [f"# Vergleich {', '.join(f'`{v}`' for v in versionen)}", "",
           "Alle Versionen bewertet mit Judge j2 (Trajektorie als Kontext, entwurf_ok + keine_spekulation) "
           "und dem korrigierten Goldset (T01 präzisiert, T07 Übergabe optional).", "",
           "## Je Metrik", "", f"| Metrik | {kopf} | Δ {versionen[-1]} vs. {versionen[0]} |", "|---" * (len(versionen) + 2) + "|"]
    for key in kz[versionen[0]]:
        a, b = kz[versionen[0]][key], kz[versionen[-1]][key]
        if a is None or b is None:
            d = "–"
        elif "USD" in key:
            d = f"{b - a:+.4f}"
        elif "(s)" in key or "Werkzeug" in key:
            d = f"{b - a:+.1f}"
        else:
            d = f"{(b - a) * 100:+.0f} Pp."
        out.append(f"| {key} | {' | '.join(fmt(key, kz[v][key]) for v in versionen)} | {d} |")

    out += ["", "## Je Ticket", "",
            f"| Ticket | {' | '.join('Erfolg ' + v for v in versionen)} | Trend {versionen[-2]} → {versionen[-1]} | "
            f"Veränderte Kriterien ({versionen[-2]} → {versionen[-1]}) |", "|---" * (len(versionen) + 3) + "|"]
    besser, schlechter = [], []
    vorher, nachher = daten[versionen[-2]], daten[versionen[-1]]
    for tid in sorted(nachher):
        e = [sum(z["erfolg"] for z in daten[v][tid]) for v in versionen]
        trend = "besser" if e[-1] > e[-2] else "schlechter" if e[-1] < e[-2] else "gleich"
        (besser if trend == "besser" else schlechter if trend == "schlechter" else []).append(tid)
        diffs = []
        for k in (*KRITERIEN, "keine_spekulation"):
            ca, cb = sum(z.get(k) is True for z in vorher[tid]), sum(z.get(k) is True for z in nachher[tid])
            if ca != cb:
                diffs.append(f"{k} {ca}/{len(vorher[tid])} → {cb}/{len(nachher[tid])}")
        out.append(f"| {tid} | {' | '.join(f'{x}/3' for x in e)} | {trend} | {'; '.join(diffs) or '–'} |")

    out += ["", f"## Kopplungseffekt ({versionen[-2]} → {versionen[-1]})", "",
            f"- Besser geworden: {', '.join(besser) or 'keins'}",
            f"- Schlechter geworden: {', '.join(schlechter) or 'keins'}"]
    for tid in schlechter:
        for z in nachher[tid]:
            if not z["erfolg"]:
                gruende = [k for k in KRITERIEN if z[k] is False]
                detail = z.get("entwurf_ok_begruendung", "") if z.get("entwurf_ok") is False else ""
                out.append(f"  - `{z['run_id']}`: {', '.join(gruende)}. {detail}".rstrip())
    if einordnung:
        out += ["", (ROOT / einordnung).read_text(encoding="utf-8").strip()]
    if faelle:
        out += ["", "## Fallbeispiele", "",
                f"Auswahl der Läufe: Bei einem Ticket, das in {versionen[-1]} besser ist, steht ein bestandener "
                f"{versionen[-1]}-Lauf neben gescheiterten Läufen der früheren Versionen, bei einem schlechteren umgekehrt. "
                "Bei gleichem Ergebnis zeigt jede Version ihren mehrheitlichen Ausgang. Gewählt wird jeweils der erste "
                "passende Lauf. Die Zählung x/3 in der Überschrift zeigt, wie typisch der gezeigte Lauf ist.", ""]
        for f in faelle:
            tid, stichwort = f.split(":", 1)
            out += fallbeispiel(tid, stichwort, versionen, daten)
    text = "\n".join(out) + "\n"
    (ROOT / "evals" / f"vergleich_{'_'.join(versionen)}.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("versionen", nargs="+")
    ap.add_argument("--fall", action="append", default=[], help="TICKET:STICHWORT der relevanten Prompt-Regel")
    ap.add_argument("--einordnung", help="Markdown-Datei mit manueller Einordnung")
    x = ap.parse_args()
    main(x.versionen, x.fall, x.einordnung)
