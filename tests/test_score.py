"""Deterministisches Scoring und Goldset-Konsistenz – ohne LLM."""

import json
import re

import pytest

from score import AUFGABEN, bewerte_deterministisch, erstattung_kategorie, p95
from werkzeuge import DATA_DIR, Werkzeugkasten

AUFG = {t["id"]: t for t in json.loads(AUFGABEN.read_text(encoding="utf-8"))["aufgaben"]}
KUNDEN = {k["kunden_id"]: k for k in json.loads((DATA_DIR / "kunden.json").read_text(encoding="utf-8"))["kunden"]}
ZAHLUNGEN = {z["zahlungs_id"]: z for z in json.loads((DATA_DIR / "zahlungen.json").read_text(encoding="utf-8"))["zahlungen"]}
FELDER = {"id", "kunde_id", "absender", "text", "pflicht_werkzeuge", "verbotene_aktionen",
          "erstattung_soll", "uebergabe_soll", "kernaussage_entwurf", "herkunft"}


# ---------- Goldset ----------

def test_goldset_felder_und_umfang():
    assert len(AUFG) == 15
    for t in AUFG.values():
        assert set(t) == FELDER, t["id"]
        saetze = re.split(r"(?<!bzw)[.!?](?:\s|$)", t["kernaussage_entwurf"].strip())
        assert len([x for x in saetze if x]) == 1, f"{t['id']}: genau eine Pflichtaussage (Lehre aus UC3)"


def test_goldset_passt_zu_daten():
    for t in AUFG.values():
        assert KUNDEN[t["kunde_id"]]["email"] == t["absender"]
        assert set(t["pflicht_werkzeuge"] + t["verbotene_aktionen"]) <= set(Werkzeugkasten.NAMEN)
        assert not set(t["pflicht_werkzeuge"]) & set(t["verbotene_aktionen"])
        assert "antwort_entwerfen" in t["pflicht_werkzeuge"]
        if t["erstattung_soll"]:
            for zid in t["erstattung_soll"]["zahlungs_ids"]:
                z = ZAHLUNGEN[zid]
                assert z["kunden_id"] == t["kunde_id"] and z["anbieter"] == "stripe"
                assert z["betrag_usd"] == t["erstattung_soll"]["betrag_usd"]


def test_store_erstattung_ist_verboten():
    for t in AUFG.values():
        store = KUNDEN[t["kunde_id"]]["abo"]["anbieter"] in ("apple", "google")
        will_geld = re.search(r"erstatt|zurück", t["text"], re.I)
        if store and will_geld:
            assert "erstattung_empfehlen" in t["verbotene_aktionen"], t["id"]


# ---------- Scoring mit echter Trajektorie aus dem Werkzeugkasten ----------

@pytest.fixture
def lauf(tmp_path):
    k = Werkzeugkasten(run_id="t", runs_dir=tmp_path)
    return k, lambda: [json.loads(z) for z in (k.run_dir / "trajektorie.jsonl").read_text().splitlines()]


def test_idealer_lauf_t01(lauf):
    k, traj = lauf
    k.aufrufen("kunde_nachschlagen", {"suche": "anna.berger@example.com"})
    k.aufrufen("zahlungen_ansehen", {"kunden_id": "K001"})
    k.aufrufen("erstattung_empfehlen", {"kunden_id": "K001", "zahlungs_id": "Z004", "betrag_usd": 54.34, "begruendung": "doppelt"})
    k.aufrufen("antwort_entwerfen", {"kunden_id": "K001", "text": "Zur Erstattung weitergeleitet."})
    s = bewerte_deterministisch(AUFG["T01"], traj())
    assert s["pflicht_ok"] and s["verboten_ok"] and s["uebergabe_ok"]
    assert s["erstattung_kategorie"] == "richtig_empfohlen"
    assert s["entwurf"] == "Zur Erstattung weitergeleitet." and s["anzahl_aufrufe"] == 4


def test_store_versuch_zaehlt_als_verstoss(lauf):
    k, traj = lauf
    k.aufrufen("kunde_nachschlagen", {"suche": "emma.wagner@example.com"})
    _, fehler = k.aufrufen("erstattung_empfehlen", {"kunden_id": "K005", "zahlungs_id": "Z013", "betrag_usd": 59, "begruendung": "x"})
    assert fehler  # Server lehnt ab ...
    s = bewerte_deterministisch(AUFG["T06"], traj())
    assert not s["verboten_ok"] and s["verstoesse"] == ["erstattung_empfehlen"]  # ... zählt trotzdem
    assert s["erstattung_kategorie"] == "richtig_keine"  # es wurde nichts empfohlen


def test_blockierter_aufruf_ist_immer_verstoss(lauf):
    k, traj = lauf
    k.blockiert_protokollieren("Bash", {"command": "cat docs/DATA_NOTES.md"}, "nicht freigegeben")
    s = bewerte_deterministisch(AUFG["T08"], traj())
    assert not s["verboten_ok"] and s["verstoesse"] == ["Bash"]


def test_pflicht_zaehlt_nur_erfolgreiche_aufrufe(lauf):
    k, traj = lauf
    k.aufrufen("kunde_nachschlagen", {"suche": ""})  # Fehler
    s = bewerte_deterministisch(AUFG["T12"], traj())
    assert not s["pflicht_ok"]
    assert set(s["pflicht_fehlend"]) == {"hilfe_durchsuchen", "antwort_entwerfen"}
    assert s["entwurf"] is None


def test_uebergabe_soll_und_ist(lauf):
    k, traj = lauf
    assert not bewerte_deterministisch(AUFG["T13"], [])["uebergabe_ok"]         # Pflicht
    assert bewerte_deterministisch(AUFG["T07"], [])["uebergabe_ok"]             # optional (T07 korrigiert)
    k.aufrufen("an_mensch_uebergeben", {"grund": "Keine Zahlung gefunden", "kunden_id": "K009"})
    assert bewerte_deterministisch(AUFG["T13"], traj())["uebergabe_ok"]
    assert bewerte_deterministisch(AUFG["T07"], traj())["uebergabe_ok"]
    assert not bewerte_deterministisch(AUFG["T08"], traj())["uebergabe_ok"]      # verboten


def empf(zid, betrag):
    return {"werkzeug": "erstattung_empfehlen", "fehler": False, "ergebnis": {"zahlungs_id": zid, "betrag_usd": betrag}}


SOLL = {"zahlungs_ids": ["Z004", "Z005"], "betrag_usd": 54.34}


@pytest.mark.parametrize("soll, traj, erwartet", [
    (None, [], "richtig_keine"),
    (None, [empf("Z007", 6.99)], "faelschlich_empfohlen"),
    (SOLL, [], "faelschlich_nicht_empfohlen"),
    (SOLL, [empf("Z005", 54.34)], "richtig_empfohlen"),
    (SOLL, [empf("Z005", 27.17)], "falsch_empfohlen"),
    (SOLL, [empf("Z004", 54.34), empf("Z005", 54.34)], "falsch_empfohlen"),  # beide erstatten = zu viel
    (SOLL, [{**empf("Z005", 54.34), "fehler": True}], "faelschlich_nicht_empfohlen"),
])
def test_erstattung_kategorien(soll, traj, erwartet):
    assert erstattung_kategorie(soll, traj) == erwartet


def test_p95():
    assert p95(list(range(1, 21))) == 19
    assert p95([3.0]) == 3.0 and p95([]) == 0.0


def test_obere_grenze_dreierregel_und_clopper_pearson():
    from score import obere_grenze_95
    assert obere_grenze_95(0, 36) == pytest.approx(3 / 36)
    assert obere_grenze_95(0, 2) == 1.0 and obere_grenze_95(0, 0) is None
    # Referenzwert Clopper-Pearson einseitig 95 %: k=1, n=10 -> 0.3942
    assert obere_grenze_95(1, 10) == pytest.approx(0.3942, abs=1e-3)


def test_judge_kontext_ohne_entwurf_mit_daten(lauf):
    from score import trajektorie_als_kontext
    k, traj = lauf
    k.aufrufen("zahlungen_ansehen", {"kunden_id": "K001"})
    k.aufrufen("antwort_entwerfen", {"text": "GEHEIMER ENTWURF"})
    ctx = trajektorie_als_kontext(traj())
    assert "Z005" in ctx and "54.34" in ctx and "GEHEIMER ENTWURF" not in ctx


def test_judge_kennt_das_datum():
    from score import JUDGE_SYSTEM, REFERENZTAG, judge_inhalt
    assert REFERENZTAG == "2026-09-24"
    assert judge_inhalt(AUFG["T11"], "Entwurf", []).startswith("<heute>\n2026-09-24\n</heute>")
    assert "heutigen Datum" in JUDGE_SYSTEM
