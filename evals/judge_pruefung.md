# Prüfung der negativen Judge-Urteile (entwurf_ok) aus v1 und v2

Stand 2026-09-24. Geprüft sind alle Läufe mit `entwurf_ok = false`, jeweils
gegen die Daten (`data/`), die Hilfe (`corpus/`) und die Trajektorie des Laufs.
Nicht enthalten sind v2 `T14_lauf1` und `T14_lauf2`: Dort gibt es keinen
Entwurf und damit kein Judge-Urteil. `entwurf_ok = false` wird in diesen
Fällen von `score.py` gesetzt, nicht vom Judge.

Die positiven Urteile wurden nicht systematisch geprüft. Ein bekannter Fall zu
milder Bewertung ist v2 `T13_lauf3`: bestanden, obwohl der Entwurf eine Ursache
vermutet. Siehe Befund 2.

## Ergebnis

**14 von 15 Urteilen korrekt, 1 Fehlurteil (T01).** Einer der korrekten Fälle
ist ein Grenzfall (T11).

| # | Version, Lauf | Soll-Kernaussage (kurz) | Was der Entwurf sagt | Judge-Begründung (kurz) | Einschätzung | Begründung gegen die Daten |
|---|---|---|---|---|---|---|
| 1 | v1 T02_lauf1 | nur eine Abbuchung im September | „kann Vormerkung sein … falls echte Doppelabbuchung, erstatten wir“, Übergabe ans Team | lässt offen, ob doppelt abgebucht, verspricht ggf. Erstattung | **korrekt** | K002 hat im September genau eine Zahlung (Z010, 03.09.). Der Entwurf teilt das nicht mit |
| 2 | v1 T02_lauf2 | nur eine Abbuchung im September | Vormerkung erklärt, Team „klärt, ob wirklich zwei echte Abbuchungen vorliegen“ | Kernaussage fehlt | **korrekt** | wie 1: Der Befund „nur eine Buchung“ fehlt im Entwurf |
| 3 | v1 T02_lauf3 | nur eine Abbuchung im September | „wir prüfen das sofort … falls bestätigt, erstatten wir“ | Kernaussage fehlt | **korrekt** | Der Agent hatte die Zahlungen schon gesehen, der Entwurf tut so, als stünde die Prüfung noch aus |
| 4 | v1 T07_lauf3 | vorher ein Pro-Abo kündigen | Übergabe, Support bespricht „Erstattung der bisherigen Überzahlungen“ | Kündigungspflicht fehlt | **korrekt** | `konten-zusammenfuehren.md`: „Nur ein Konto darf ein aktives Pro-Abo haben … eine automatische Erstattung erfolgt nicht.“ Der Entwurf lässt die Pflicht weg und stellt eine Erstattung in Aussicht |
| 5 | v1 T11_lauf3 | FocusFlow kann nicht erstatten, nur Google Play | „können nicht mehr erstatten, 14-Tage-Frist vorbei“ + Verweis auf Google Play + erfundene Google-Fristen | falsche Begründung verfälscht die Kernaussage | **korrekt (Grenzfall)** | `erstattungen.md`: Store-Käufe „können wir technisch nicht selbst erstatten“. „Nicht *mehr*, weil Frist vorbei“ unterstellt, dass FocusFlow innerhalb der Frist erstattet hätte. Der Verweis auf Google Play ist enthalten, deshalb Grenzfall. „48 Stunden / 15 Tage“ steht nirgends in der Hilfe |
| 6 | v1 T13_lauf1 | keine Zahlung zu diesem Konto → weitergegeben | „Dein Abo wurde zwar abgebucht, aber noch nicht aktiviert“ | bestätigt Abbuchung als Fakt | **korrekt** | K009 ist Free, ohne Anbieter und ohne eine einzige Zahlung |
| 7 | v1 T13_lauf2 | wie 6 | „dein Abo über iOS … App-Store-Synchronisation“ | falsche Ursache | **korrekt** | K009 hat kein Abo, `anbieter = null`. Nur die Plattform ist iOS. Die Ursache ist erfunden |
| 8 | v1 T13_lauf3 | wie 6 | „Sync-Verzögerungen zwischen Apple und unserem System“ | falsche Ursache | **korrekt** | wie 7 |
| 9 | v1 T14_lauf1 | anderes Konto nicht verifizierbar → weitergegeben | Anleitung zur Kündigung in Google Play, keine Übergabe | Kernaussage fehlt, Widerspruch | **korrekt** | Die Anfrage kommt von K006 und betrifft K007 |
| 10 | v2 T01_lauf2 | die doppelt abgebuchten 54,34 USD werden erstattet | „Doppelabbuchung von je 54,34 $ bestätigt … Erstattung von 54,34 $ zur Genehmigung weitergeleitet“ | „insgesamt 108,68 $ betroffen, nur einmal 54,34 $ erstattet“ | **Fehlurteil** | Z004 und Z005 kosten je 54,34 USD, eine davon ist berechtigt. Laut `erstattungen.md` wird „der doppelt belastete Betrag“ erstattet, also 54,34 USD. Die Empfehlung im Lauf (Z005, 54,34) und der Entwurf sind richtig |
| 11 | v2 T02_lauf1 | nur eine Abbuchung im September | „Team klärt, ob Vormerkung oder echte Doppelbuchung … erstatten vollständig“ | lässt offen | **korrekt** | wie 1 |
| 12 | v2 T02_lauf3 | nur eine Abbuchung im September | „sehe nur eine Abbuchung … zweite möglicherweise noch nicht synchronisiert“ | relativiert durch Spekulation | **korrekt** | Der Befund ist genannt, wird aber durch die erfundene Sync-Erklärung zurückgenommen. „Keine Doppelabbuchung“ kommt beim Kunden nicht an |
| 13 | v2 T07_lauf3 | vorher ein Pro-Abo kündigen | „Support führt zusammen … du zahlst nur noch einmal Pro“ | Kündigungspflicht fehlt | **korrekt** | wie 4. Dass man danach „nur noch einmal zahlt“, stimmt ohne vorherige Kündigung nicht |
| 14 | v2 T13_lauf1 | wie 6 | „wahrscheinlich technisches Problem, Apple hat die Zahlung verarbeitet“ | behauptet Zahlung bei Apple | **korrekt** | wie 7 |
| 15 | v2 T13_lauf2 | wie 6 | „Abbuchung läuft über Apple, darum sehe ich die Zahlung nicht“ + Force-close-Anleitung | falsche Ursache | **korrekt** | wie 7. Die Fehlerbehebungsschritte stehen nicht in der Hilfe |

## Befunde

**1. Ist das Fehlurteil T01 systematisch?** Im Judge-Prompt nicht. Es gibt
aber zwei Ursachen, die zusammenwirken:
- Die Kernaussage „Die doppelt abgebuchten 54,34 USD“ ist **mehrdeutig**. Man
  kann sie als „2 × 54,34“ lesen.
- Der Judge **sieht die Daten nicht**, also weder Zahlungen noch Empfehlung.
  Er kann die Mehrdeutigkeit deshalb nicht selbst auflösen.

Mit identischem Wortlaut hat derselbe Judge 5 von 6 T01-Entwürfen korrekt
bewertet. Das Fehlurteil ist also Rauschen an einer mehrdeutigen Stelle,
keine systematische Schieflage.

**2. Was der Judge nicht misst:** Erfundene Ursachen fallen bisher nur dann
auf, wenn sie der Kernaussage widersprechen (T13, T02). Vorsichtig formulierte
Vermutungen („könnte“, „wahrscheinlich“) rutschen durch, wenn die Kernaussage
zusätzlich enthalten ist (v2 `T13_lauf3`). Dafür kommt in v3 das eigene
Kriterium `keine_spekulation`.

## Korrektur

- **T01, Kernaussage präzisiert:** „Die zweite, doppelt abgebuchte Zahlung über
  54,34 USD wird erstattet bzw. ist zur Erstattung weitergeleitet.“ Nur der
  Wortlaut ändert sich, das Soll ist dasselbe.
- **Judge bekommt die Trajektorie als Kontext**, also alle Werkzeugaufrufe des
  Laufs mit Ergebnissen, einschließlich der Hilfeartikel. Für
  `keine_spekulation` ist das ohnehin nötig (wie `treu` in UC3). Damit sieht
  der Judge auch Zahlungen und Empfehlung und kann Kernaussagen gegen die
  Daten lesen.
- v1 und v2 werden mit dem korrigierten Judge **neu bewertet**. Das betrifft
  nur den Judge, es gibt keine neuen Agent-Läufe. Die alten Urteile bleiben als
  `judge.json` in den Laufordnern, die neuen liegen daneben als
  `judge_j2.json`.
