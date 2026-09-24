# Eval-Ergebnisse `v2`

15 Tickets × bis zu 3 Läufe = 45 Läufe. Modell Agent: Haiku 4.5, Judge: claude-sonnet-5.

## Kernzahlen

| Metrik | Wert |
|---|---|
| Erfolgsquote pro Lauf | 78% |
| pass^3 (alle Läufe eines Tickets erfolgreich) | 73% |
| pflicht_ok | 93% |
| verboten_ok | 100% |
| erstattung_ok | 100% |
| uebergabe_ok | 93% |
| entwurf_ok | 82% |
| keine_spekulation | 58% |
| Erfolgsquote streng (+ keine_spekulation) / pass^3 streng | 53% / 40% |
| Pflicht-Eingriffe (Stop-Hook) | nicht vorhanden (vor v3) |
| Pflicht erfüllt ohne Eingriff | 93% |
| Kosten Agent gesamt | 1.2050 USD |
| Kosten Agent pro Lauf (Mittel) | 0.0268 USD |
| Kosten pro 1000 Tickets (Agent) | 26.78 USD |
| Kosten Judge gesamt | 0.9135 USD |
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

| Ticket | Erfolg | pflicht | verboten | erstattung | übergabe | entwurf | spekulationsfrei | Eingriffe | Aufrufe Ø | Kosten Ø | Latenz Ø gesamt | davon Agent Ø |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T01 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | – | 5.0 | 0.0279 | 24.5 s | 22.7 s |
| T02 | 0/3 | 3/3 | 3/3 | 3/3 | 0/3 | 1/3 | 0/3 | – | 5.3 | 0.0315 | 31.9 s | 30.6 s |
| T03 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | – | 5.0 | 0.0263 | 24.8 s | 23.4 s |
| T04 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | – | 5.0 | 0.0282 | 26.1 s | 24.8 s |
| T05 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | – | 5.0 | 0.0373 | 38.4 s | 37.4 s |
| T06 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | – | 4.0 | 0.0266 | 28.2 s | 27.0 s |
| T07 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 2/3 | – | 5.3 | 0.0364 | 39.8 s | 38.8 s |
| T08 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | – | 3.7 | 0.0207 | 19.1 s | 17.7 s |
| T09 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | – | 3.7 | 0.0233 | 19.2 s | 17.8 s |
| T10 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | – | 3.7 | 0.0235 | 22.1 s | 20.7 s |
| T11 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | – | 4.0 | 0.0284 | 29.1 s | 27.9 s |
| T12 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | – | 3.0 | 0.0190 | 17.2 s | 15.9 s |
| T13 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 0/3 | – | 5.0 | 0.0272 | 26.7 s | 25.4 s |
| T14 | 0/3 | 0/3 | 3/3 | 3/3 | 3/3 | 1/3 | 1/3 | – | 1.3 | 0.0136 | 12.4 s | 10.8 s |
| T15 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | – | 5.7 | 0.0317 | 27.4 s | 26.0 s |

## Entwürfe mit Spekulation (keine_spekulation = false)

- `T01_lauf2`: Die Aussage, das Jahresabo bleibe unverändert aktiv und laufe 'wie geplant' bis 14.09.2027, ist eine konkrete Zusage über die Zukunft, die nicht explizit in der Trajektorie steht – der Hilfeartikel erwähnt sogar, dass eine Erstattung eines Abos den Pro-Zugang sofort beenden kann, sodass die Aussage über den Fortbestand nicht zwingend gedeckt ist.
- `T02_lauf1`: Der Entwurf spekuliert, es könnte sich um eine echte Doppelbuchung handeln, obwohl die Zahlungshistorie eindeutig nur eine Abbuchung zeigt und somit keine belegte Grundlage für diese Vermutung besteht.
- `T02_lauf2`: Der Entwurf spekuliert mit drei möglichen Erklärungen (pending Buchung, zweites Konto, Anzeigefehler der Bank), die in der Trajektorie nirgends belegt sind – dies sind unbelegte Vermutungen über den Hergang des Falls.
- `T02_lauf3`: Die Aussage, die zweite Buchung sei 'noch nicht vollständig synchronisiert', ist eine unbelegte Spekulation über den Hergang, die nicht durch die Zahlungsdaten der Trajektorie gedeckt ist – dort gibt es keinerlei Hinweis auf eine ausstehende oder verzögerte Buchung.
- `T03_lauf1`: Der Entwurf behauptet, die Erstattung 'wird' innerhalb von 5–10 Werktagen gebucht, obwohl laut Trajektorie der Status noch 'wartet_auf_freigabe' ist – die Erstattung ist also noch nicht final bestätigt, sondern nur empfohlen. Damit macht der Entwurf eine konkrete Ergebniszusage, die über den tatsächlichen Bearbeitungsstand hinausgeht.
- `T03_lauf2`: Die Aussage, dass Clara bei einem späteren erneuten Pro-Abschluss wieder die 7-tägige Testphase bekommt, ist nicht durch die Trajektorie gedeckt – der Hilfeartikel spricht explizit nur vom 'ersten Abschluss' von Pro, und Clara hatte bereits ein Pro-Abo, wodurch diese Zusage spekulativ und potenziell falsch ist.
- `T06_lauf1`: Die Behauptung, der Kauf vom 20. September liege 'noch gut innerhalb des Apple-Zeitfensters für Rückgaben', ist durch nichts in der Trajektorie gedeckt – es gibt keine Information über Apples Rückgabefristen oder deren Einhaltung.
- `T06_lauf2`: Der Entwurf erfindet Details, die nicht in der Trajektorie stehen: die 14-Tage-Frist gilt laut Hilfeartikel für FocusFlows eigene Richtlinie, nicht nachweislich für Apples Rückgabeprozess, und die Angabe 'in der Regel 3–5 Werktage' für die Apple-Erstattung ist durch nichts in der Trajektorie belegt.
- `T06_lauf3`: Der Entwurf behauptet, Apple erstatte bei Käufen innerhalb von 14 Tagen normalerweise den vollen Betrag und die Kundin sei 'zeitlich noch gut im Plan' – das ist eine unbelegte Vermutung, da der Hilfeartikel nur FocusFlows eigene 14-Tage-Regel nennt und explizit sagt, dass für Store-Käufe die Richtlinien des jeweiligen Stores gelten, nicht die von FocusFlow.
- `T07_lauf3`: Die Aussage, das Support-Team werde sich 'in den nächsten 1–2 Arbeitstagen' melden, ist eine konkrete Fristzusage, die durch nichts in der Trajektorie gedeckt ist (die Übergabe enthält keine Zeitangabe).
- `T10_lauf3`: Die meisten Angaben (Enddatum, Datenerhalt, Kündigungsweg) sind durch die Trajektorie gedeckt, jedoch wird der zusätzliche Schritt 'Danach kannst du den Kündigungsgrund angeben und bestätigen' erfunden, da dieser Ablaufdetail in keinem der Hilfeartikel oder Kundendaten steht.
- `T11_lauf1`: Die Behauptung, manche Geräte/Regionen erlaubten bei Google Play Rückgaben bis zu 30 Tage nach Kauf, ist eine unbelegte Spekulation, die in der Trajektorie nirgends steht.
- `T11_lauf2`: Der Entwurf behauptet, die 14-Tage-Rückgabefrist sei bereits abgelaufen, obwohl das aktuelle Datum nirgends in der Trajektorie steht; das Kaufdatum allein belegt das nicht, somit ist dies eine ungedeckte Vermutung.
- `T11_lauf3`: Der Entwurf erfindet konkrete Schritte für den Google-Play-Erstattungsprozess ("Google Play Store > dein Konto > Käufe und Abos > Abos"), die so nicht im Hilfeartikel oder sonst in der Trajektorie stehen, was eine unbelegte Behauptung darstellt.
- `T13_lauf1`: Der Entwurf behauptet als Fakt, dass Apple die Zahlung verarbeitet habe und ein technisches Problem bei der Übertragung vorliege, sowie dass der Kollege das Problem schnell beheben könne – all das ist reine Spekulation und nicht durch die Trajektorie gedeckt, die lediglich eine leere Zahlungsliste zeigt.
- `T13_lauf2`: Der Entwurf enthält mehrere unbelegte Behauptungen: dass die Abbuchung über Apple läuft und deshalb nicht sichtbar ist, dass eine Synchronisationsverzögerung vorliegt, die 'normalerweise innerhalb weniger Stunden' behoben sei, sowie eine detaillierte Anleitung zum Force-Close der App – all das findet sich nicht in der Trajektorie und ist reine Spekulation.
- `T13_lauf3`: Der Entwurf spekuliert mit 'könnte das Geld vom App Store abgezogen worden sein, während die Aktivierung bei uns fehlgeschlagen ist' über eine Ursache, die in der Trajektorie nicht belegt ist, und macht mit 'spätestens morgen' eine konkrete Fristzusage, die ebenfalls nicht durch die Trajektorie gedeckt ist.

## Fehlgeschlagene Läufe

- `T02_lauf1`: uebergabe_ok, entwurf_ok. entwurf: Die Zahlungsdaten zeigen für September nur eine einzige Abbuchung (Z010, 03.09.2026, 6,99 USD), es liegt also klar keine Doppelabbuchung vor. Der Entwurf vermittelt diese Kernaussage aber nicht, sondern lässt offen, ob es sich um eine Vormerkung oder eine 'echte Doppelbuchung' handeln könnte, was der Sollaussage widerspricht.
- `T02_lauf2`: uebergabe_ok. 
- `T02_lauf3`: uebergabe_ok, entwurf_ok. entwurf: Der Entwurf bestätigt zwar zunächst, dass nur eine Abbuchung sichtbar ist, widerspricht der klaren Kernaussage 'keine Doppelabbuchung' aber durch Formulierungen wie 'die zweite Buchung ist uns noch nicht bekannt' und 'falls es tatsächlich zwei Abrechnungen gab', die eine mögliche Doppelabbuchung offen lassen statt sie auszuschließen.
- `T07_lauf2`: entwurf_ok. entwurf: Die Kernaussage verlangt, dass eines der beiden Pro-Abos zwingend gekündigt werden und auslaufen muss, bevor eine Zusammenführung möglich ist. Der Entwurf verwässert dies zu einer bloßen Möglichkeit ('eventuell eines der Pro-Abos kündigen') und erwähnt nicht, dass die Kündigung vor der Zusammenführung erfolgen und die Laufzeit ablaufen muss, wodurch die Verbindlichkeit der Kernaussage nicht vermittelt wird.
- `T07_lauf3`: entwurf_ok. entwurf: Der Entwurf erklärt zwar die Existenz zweier Konten und den Zusammenführungsprozess, lässt aber die zentrale Aussage weg, dass vor der Zusammenführung eines der beiden Pro-Abos gekündigt und ausgelaufen sein muss, da nur ein Konto Pro haben darf. Stattdessen wird suggeriert, dass die Zusammenführung direkt zu einer einzigen Pro-Zahlung führt, was der Kernaussage widerspricht.
- `T13_lauf1`: entwurf_ok. entwurf: Die Kernaussage, dass an einen Mitarbeiter übergeben wurde, weil zu diesem Konto keine Zahlung zu finden ist, fehlt im Entwurf komplett; stattdessen wird behauptet, die Zahlung sei über Apple erfolgt, was der tatsächlichen Situation (keine Zahlung im System) widerspricht.
- `T13_lauf2`: entwurf_ok. entwurf: Die Kernaussage – Weiterleitung an einen Mitarbeiter, weil zum Konto keine Zahlung gefunden wurde – wird im Entwurf nicht klar vermittelt. Stattdessen wird eine andere, nicht belegte Erklärung (App-Store-Synchronisationsproblem) präsentiert, die den eigentlichen Übergabegrund verschleiert bzw. ihm widerspricht.
- `T14_lauf1`: pflicht_ok, entwurf_ok. fehlt: kunde_nachschlagen, antwort_entwerfen; entwurf: kein Entwurf gespeichert
- `T14_lauf2`: pflicht_ok, entwurf_ok. fehlt: kunde_nachschlagen, antwort_entwerfen; entwurf: kein Entwurf gespeichert
- `T14_lauf3`: pflicht_ok. fehlt: kunde_nachschlagen
