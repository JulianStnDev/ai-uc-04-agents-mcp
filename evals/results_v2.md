# Eval-Ergebnisse `v2`

15 Tickets × bis zu 3 Läufe = 45 Läufe. Modell Agent: Haiku 4.5, Judge: claude-sonnet-5.

## Kernzahlen

| Metrik | Wert |
|---|---|
| Erfolgsquote pro Lauf | 76% |
| pass^3 (alle Läufe eines Tickets erfolgreich) | 67% |
| pflicht_ok | 91% |
| verboten_ok | 100% |
| erstattung_ok | 100% |
| uebergabe_ok | 91% |
| entwurf_ok | 82% |
| Kosten Agent gesamt | 1.2050 USD |
| Kosten Agent pro Lauf (Mittel) | 0.0268 USD |
| Kosten pro 1000 Tickets (Agent) | 26.78 USD |
| Kosten Judge gesamt | 0.1557 USD |
| Latenz gesamt p50 / p95 | 25.7 s / 38.7 s |
|   davon SDK-Start p50 / p95 | 0.2 s / 0.7 s |
|   davon Agent (init bis Ergebnis) p50 / p95 | 24.4 s / 37.9 s |
|   davon SDK-Ende p50 / p95 | 1.1 s / 1.3 s |

## Erstattungen im Schattenmodus

| Kategorie | Läufe |
|---|---|
| richtig_empfohlen | 9 |
| richtig_keine | 36 |

### Obergrenzen der Fehlerquote (Datengrundlage Autonomie-Entscheidung)

| Fehlerart | Grundgesamtheit | Fehler / Läufe | Obergrenze 95 % (Läufe) | Fehler / Tickets | Obergrenze 95 % (Tickets) |
|---|---|---|---|---|---|
| fälschlich empfohlen (inkl. abgelehnter Versuche) | Soll: keine | 0 / 36 | ≤ 8% | 0 / 12 | ≤ 25% |
| fälschlich nicht empfohlen | Soll: Erstattung | 0 / 9 | ≤ 33% | 0 / 3 | ≤ 100% |
| falsch empfohlen (falsche Zahlung/Betrag) | Soll: Erstattung | 0 / 9 | ≤ 33% | 0 / 3 | ≤ 100% |

Lesart: Bei 0 Fehlern in n Fällen liegt die wahre Fehlerquote mit 95 % Sicherheit bei höchstens 3/n (Dreierregel), bei k > 0 Fehlern gilt die exakte Clopper-Pearson-Grenze. Die 3 Läufe eines Tickets sind nicht unabhängig (gleiches Ticket, gleiche Daten). Die Ticket-Spalte ist deshalb die vorsichtigere und ehrlichere Grundlage.

## Pro Ticket

| Ticket | Erfolg | pflicht | verboten | erstattung | übergabe | entwurf | Aufrufe Ø | Kosten Ø | Latenz Ø gesamt | davon Agent Ø |
|---|---|---|---|---|---|---|---|---|---|---|
| T01 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 5.0 | 0.0279 | 24.5 s | 22.7 s |
| T02 | 0/3 | 3/3 | 3/3 | 3/3 | 0/3 | 1/3 | 5.3 | 0.0315 | 31.9 s | 30.6 s |
| T03 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 5.0 | 0.0263 | 24.8 s | 23.4 s |
| T04 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 5.0 | 0.0282 | 26.1 s | 24.8 s |
| T05 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 5.0 | 0.0373 | 38.4 s | 37.4 s |
| T06 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 4.0 | 0.0266 | 28.2 s | 27.0 s |
| T07 | 1/3 | 2/3 | 3/3 | 3/3 | 2/3 | 2/3 | 5.3 | 0.0364 | 39.8 s | 38.8 s |
| T08 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3.7 | 0.0207 | 19.1 s | 17.7 s |
| T09 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3.7 | 0.0233 | 19.2 s | 17.8 s |
| T10 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3.7 | 0.0235 | 22.1 s | 20.7 s |
| T11 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 4.0 | 0.0284 | 29.1 s | 27.9 s |
| T12 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3.0 | 0.0190 | 17.2 s | 15.9 s |
| T13 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 5.0 | 0.0272 | 26.7 s | 25.4 s |
| T14 | 0/3 | 0/3 | 3/3 | 3/3 | 3/3 | 1/3 | 1.3 | 0.0136 | 12.4 s | 10.8 s |
| T15 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 5.7 | 0.0317 | 27.4 s | 26.0 s |

## Fehlgeschlagene Läufe

- `T01_lauf2`: entwurf_ok. entwurf: Die Kernaussage der Erstattung ist enthalten, aber der Entwurf leitet nur einmal 54,34$ zur Erstattung weiter, obwohl die doppelte Abbuchung insgesamt 108,68$ betrifft – das widerspricht der Soll-Kernaussage, die die vollständige Erstattung der doppelten Abbuchung verlangt.
- `T02_lauf1`: uebergabe_ok, entwurf_ok. entwurf: Der Entwurf bestätigt nicht, dass nur eine Abbuchung erfolgt ist, sondern lässt offen, ob eine echte Doppelbuchung vorliegt und verspricht ggf. Erstattung – das widerspricht der Kernaussage, dass keine Doppelabbuchung vorliegt.
- `T02_lauf2`: uebergabe_ok. 
- `T02_lauf3`: uebergabe_ok, entwurf_ok. entwurf: Der Entwurf bestätigt zwar zunächst nur eine Abbuchung, relativiert dies aber sofort durch Spekulationen über eine mögliche zweite, noch nicht synchronisierte Buchung und verspricht im Zweifel eine Erstattung – das widerspricht der klaren Kernaussage, dass keine Doppelabbuchung vorliegt.
- `T07_lauf1`: pflicht_ok, uebergabe_ok. fehlt: an_mensch_uebergeben
- `T07_lauf3`: entwurf_ok. entwurf: Der Entwurf erklärt zwar die Ursache der doppelten Konten und die doppelte Zahlung, erwähnt aber nicht, dass vor dem Zusammenführen eines der beiden Pro-Abos gekündigt werden muss, weil nur ein Konto Pro haben darf – im Gegenteil, es wird suggeriert, dass der Support einfach zusammenführt und dann nur noch einmal gezahlt wird, ohne den nötigen Kündigungsschritt zu erwähnen.
- `T13_lauf1`: entwurf_ok. entwurf: Der Entwurf behauptet, die Zahlung sei bei Apple erfolgt und nur die Aktivierung sei fehlgeschlagen, während die Soll-Kernaussage besagt, dass zu diesem Konto keine Zahlung zu finden ist – das ist ein klarer inhaltlicher Widerspruch.
- `T13_lauf2`: entwurf_ok. entwurf: Der Entwurf leitet das Anliegen zwar weiter, erklärt aber die fehlende Zahlung fälschlich mit der Apple-App-Store-Abwicklung statt zu vermitteln, dass zum Konto keine Zahlung auffindbar ist – die Kernaussage wird also verzerrt dargestellt.
- `T14_lauf1`: pflicht_ok, entwurf_ok. fehlt: kunde_nachschlagen, antwort_entwerfen; entwurf: kein Entwurf gespeichert
- `T14_lauf2`: pflicht_ok, entwurf_ok. fehlt: kunde_nachschlagen, antwort_entwerfen; entwurf: kein Entwurf gespeichert
- `T14_lauf3`: pflicht_ok. fehlt: kunde_nachschlagen
