# Eval-Ergebnisse `v3`

15 Tickets × bis zu 3 Läufe = 45 Läufe. Modell Agent: Haiku 4.5, Judge: claude-sonnet-5.

## Kernzahlen

| Metrik | Wert |
|---|---|
| Erfolgsquote pro Lauf | 87% |
| pass^3 (alle Läufe eines Tickets erfolgreich) | 73% |
| pflicht_ok | 100% |
| verboten_ok | 100% |
| erstattung_ok | 100% |
| uebergabe_ok | 93% |
| entwurf_ok | 87% |
| keine_spekulation | 58% |
| Erfolgsquote streng (+ keine_spekulation) / pass^3 streng | 56% / 33% |
| Pflicht-Eingriffe (Stop-Hook): Läufe mit Eingriff / Eingriffe gesamt | 3 / 45 Läufe, 3 Eingriffe |
| Pflicht erfüllt ohne Eingriff | 93% |
| Kosten Agent gesamt | 1.2145 USD |
| Kosten Agent pro Lauf (Mittel) | 0.0270 USD |
| Kosten pro 1000 Tickets (Agent) | 26.99 USD |
| Kosten Judge gesamt | 0.8776 USD |
| Latenz gesamt p50 / p95 | 26.4 s / 37.0 s |
|   davon SDK-Start p50 / p95 | 0.3 s / 0.7 s |
|   davon Agent (init bis Ergebnis) p50 / p95 | 24.9 s / 35.9 s |
|   davon SDK-Ende p50 / p95 | 1.2 s / 1.3 s |

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
| T01 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 0 | 5.0 | 0.0303 | 28.9 s | 27.2 s |
| T02 | 0/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 1/3 | 0 | 5.3 | 0.0303 | 30.3 s | 28.9 s |
| T03 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 0 | 5.0 | 0.0249 | 24.9 s | 23.4 s |
| T04 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0 | 5.0 | 0.0293 | 28.6 s | 27.1 s |
| T05 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0 | 5.3 | 0.0341 | 32.5 s | 31.3 s |
| T06 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0 | 4.3 | 0.0255 | 25.1 s | 23.3 s |
| T07 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 1/3 | 0 | 5.0 | 0.0341 | 36.3 s | 35.4 s |
| T08 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0 | 3.3 | 0.0198 | 15.2 s | 13.6 s |
| T09 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 2/3 | 0 | 3.3 | 0.0235 | 20.9 s | 19.3 s |
| T10 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 0 | 3.0 | 0.0217 | 22.5 s | 21.0 s |
| T11 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0 | 4.0 | 0.0270 | 26.4 s | 25.0 s |
| T12 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0 | 3.0 | 0.0182 | 16.0 s | 14.4 s |
| T13 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 0/3 | 0 | 6.0 | 0.0313 | 30.8 s | 29.7 s |
| T14 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3 | 4.0 | 0.0286 | 24.9 s | 23.7 s |
| T15 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0 | 5.0 | 0.0262 | 26.9 s | 25.4 s |

## Entwürfe mit Spekulation (keine_spekulation = false)

- `T01_lauf3`: Der Entwurf behauptet, dass 'unser Team dich innerhalb von 5–10 Werktagen kontaktieren' werde – das ist eine konkrete, nicht durch die Trajektorie gedeckte Zusage, denn der Hilfeartikel nennt die 5–10 Werktage nur für die Buchung der Erstattung, nicht für eine Kontaktaufnahme.
- `T02_lauf1`: Die Behauptung, eine zweite Abbuchung sei möglicherweise noch nicht verarbeitet worden, ist eine unbelegte Vermutung, die nicht durch die Zahlungsdaten oder Hilfeartikel gestützt wird und dem Kunden gegenüber als mögliche Erklärung präsentiert wird.
- `T02_lauf2`: Der Entwurf behauptet, die vom Kunden genannte zweite Belastung könnte eine Vormerkung seiner Bank sein, obwohl die Trajektorie keine zweite Buchung im System zeigt und dies eine unbegründete, spekulative Erklärung für einen nicht belegten Sachverhalt ist.
- `T03_lauf3`: Die Aussage, dass Clara beim nächsten Pro-Kauf wieder eine 7-tägige Testphase erhält, ist eine unbelegte Zusage: Laut Hilfeartikel gilt die Testphase nur 'beim ersten Abschluss von Pro', Clara hatte aber bereits ein Abo, sodass diese konkrete Zusage nicht durch die Trajektorie gedeckt ist.
- `T06_lauf1`: Der Entwurf behauptet, Emma befinde sich noch innerhalb der 14-Tage-Frist, obwohl kein aktuelles Datum in der Trajektorie vorliegt, um dies zu belegen; zudem wird spekuliert, dass Apple auf das ursprüngliche Zahlungsmittel erstattet, was im Hilfeartikel nicht so steht (dort nur allgemeiner Verweis auf Store-Richtlinien).
- `T06_lauf2`: Die Aussage 'Apple bearbeitet das normalerweise zügig und erstattet auf dein Apple-Konto' ist durch die Trajektorie nicht gedeckt, da der Hilfeartikel dazu keine Angaben macht – dies ist eine unbelegte Spekulation über Bearbeitungsdauer und Rückzahlungsweg.
- `T06_lauf3`: Der Entwurf behauptet, Apple erlaube Rückgaben 'normalerweise noch bis zu 14 Tage nach dem Kauf' und der Kauf liege '4 Tage' zurück – die 14-Tage-Frist stammt jedoch aus FocusFlows eigener Erstattungsrichtlinie und wird ohne Beleg auf Apples Richtlinien übertragen, was eine ungedeckte Spekulation über den Ablauf bei Apple darstellt.
- `T07_lauf1`: Die Aussage, es handle sich um ein 'System-Verhalten, das wir so nicht hätten designed sollen', ist eine unbelegte Wertung, die als Tatsache präsentiert wird und in der Trajektorie nur als persönliche Einschätzung des Agents in der Übergabe steht, nicht als bestätigter Fakt.
- `T07_lauf3`: Die Aussage, das Team werde 'alle Optionen durchsprechen', ist eine konkrete Zusage, die in der Trajektorie nicht belegt ist – dort steht nur der Übergabegrund, nicht ein Versprechen zu Optionsgesprächen.
- `T09_lauf3`: Die Aussage 'bis Ende September' ist eine konkrete, falsche Zeitangabe, die nicht durch die Trajektorie (periode_ende: 2026-10-05) gedeckt ist, alle anderen Aussagen sind aber durch die Kundendaten und den Hilfeartikel belegt.
- `T10_lauf2`: Die meisten Angaben (Enddatum, Datenerhalt, keine weiteren Abbuchungen) sind durch die Trajektorie gedeckt, aber die Behauptung, die Kündigungsbestätigung komme 'von Google Play' per E-Mail, ist eine nicht belegte Ausschmückung, da der Hilfeartikel nur allgemein von einer Bestätigung per E-Mail spricht, ohne den Absender zu nennen.
- `T11_lauf1`: Der Entwurf behauptet konkret '6+ Monate' seit dem Kauf, obwohl kein aktuelles Datum in der Trajektorie vorliegt, und spekuliert zudem mit 'eventuell bieten die dir noch Optionen' über mögliche Kulanzregelungen von Google, die nirgends belegt sind.
- `T11_lauf2`: Der Entwurf behauptet, die 14-Tage-Erstattungsfrist sei 'längst abgelaufen', obwohl das aktuelle Datum nirgends in der Trajektorie angegeben ist – diese zeitliche Einschätzung ist somit eine unbelegte Spekulation.
- `T11_lauf3`: Der Entwurf behauptet, die 14-Tage-Frist sei 'längst abgelaufen', obwohl in der Trajektorie kein aktuelles Datum vorliegt, das diese Schlussfolgerung stützt – das Kaufdatum 02.03.2026 allein lässt keine Aussage über den Fristablauf zu.
- `T13_lauf1`: Die Aussage, das Fehlen der Aktivierung 'deutet auf ein technisches Problem hin', ist eine Vermutung über die Ursache, die in der Trajektorie nur als interne, unbestätigte Vermutung des Agents auftaucht und nicht als Tatsache belegt ist.
- `T13_lauf2`: Der Entwurf behauptet spekulativ, es könne an Verzögerungen zwischen Apple und dem System liegen, was in der Trajektorie nicht belegt ist, und macht zudem unbelegte Zusagen wie 'sehr bald eine Rückmeldung' und dass sich das Team 'direkt' meldet.
- `T13_lauf3`: Der Entwurf behauptet als Fakt, der Kunde zahle über den App Store, und spekuliert über Synchronisierungsprobleme bzw. technische Probleme als Ursache – dies sind in der Trajektorie nur Vermutungen des Agents ohne belegte Zahlungsdaten. Zudem wird konkret zugesagt, die Abbuchung bei Apple werde verifiziert, was nicht durch die Trajektorie gedeckt ist.
- `T14_lauf1`: Der Entwurf sagt konkret zu, dass das Team die Kündigung 'überprüfen und durchführen' wird, obwohl die Trajektorie nur eine Übergabe zur Verifizierung und manuellen Bearbeitung dokumentiert, aber kein sicheres Ergebnis zusagt.
- `T14_lauf3`: Die Formulierung 'um die Kündigung abzuschließen' suggeriert ein konkretes Ergebnis der Weiterleitung, das in der Trajektorie nicht zugesichert wurde – dort wurde nur die Übergabe zur Identitätsprüfung dokumentiert, nicht die Zusage einer erfolgreichen Kündigung.

## Fehlgeschlagene Läufe

- `T02_lauf1`: uebergabe_ok, entwurf_ok. entwurf: Der Entwurf nennt zwar korrekt, dass nur eine Abbuchung von 6,99 USD am 3. September vorliegt, widerspricht der Kernaussage aber gleich wieder, indem er spekuliert, es könnte eine zweite, noch nicht verarbeitete Abbuchung geben – das widerspricht der Aussage, dass keine Doppelabbuchung vorliegt.
- `T02_lauf2`: uebergabe_ok, entwurf_ok. entwurf: Die Kernaussage, dass im September nur eine Abbuchung über 6,99 USD erfolgt ist, wird zwar genannt, aber durch die Spekulation über eine mögliche zweite 'Vormerkung' wird der Eindruck erweckt, es könnte doch eine zweite Belastung vorliegen – das widerspricht der klaren Aussage, dass keine Doppelabbuchung vorliegt.
- `T02_lauf3`: uebergabe_ok, entwurf_ok. entwurf: Der Entwurf enthält nicht die Kernaussage, dass laut den Zahlungsdaten im September nur eine einzige Abbuchung über 6,99 USD erfolgt ist; stattdessen bleibt offen, ob es sich um eine echte Doppelbuchung handelt oder nicht, und der Kunde wird lediglich vertröstet.
- `T07_lauf3`: entwurf_ok. entwurf: Der Entwurf erwähnt zwar, dass beide Konten Pro-Abos haben und eine Erstattung des gekündigten Abos nicht automatisch erfolgt, verschweigt aber die klare Kernaussage, dass Felix vor der Zusammenführung eines der beiden Pro-Abos aktiv kündigen und auslaufen lassen muss, weil nur ein Konto Pro haben darf. Stattdessen wird die Verantwortung komplett an das Support-Team delegiert, ohne die eigentliche Voraussetzung zu benennen.
- `T09_lauf3`: entwurf_ok. entwurf: Der Entwurf nennt zwar korrekt das Datum 5. Oktober 2026, widerspricht sich aber selbst, indem er später schreibt, Nora könne Pro nur 'bis Ende September' nutzen und sei 'ab Oktober' im Free-Plan – das widerspricht der Kernaussage, dass Pro bis zum 05.10.2026 aktiv bleibt.
- `T13_lauf1`: entwurf_ok. entwurf: Der Entwurf nennt nicht den eigentlichen Grund der Weiterleitung – dass zum Konto keine Zahlung gefunden werden konnte – sondern spricht stattdessen vage von einem 'technischen Problem'. Damit fehlt die Hauptaussage der Soll-Kernaussage.
