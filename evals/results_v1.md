# Eval-Ergebnisse `v1`

15 Tickets × bis zu 3 Läufe = 45 Läufe. Modell Agent: Haiku 4.5, Judge: claude-sonnet-5.

## Kernzahlen

| Metrik | Wert |
|---|---|
| Erfolgsquote pro Lauf | 82% |
| pass^3 (alle Läufe eines Tickets erfolgreich) | 73% |
| pflicht_ok | 98% |
| verboten_ok | 100% |
| erstattung_ok | 100% |
| uebergabe_ok | 91% |
| entwurf_ok | 82% |
| keine_spekulation | 64% |
| Erfolgsquote streng (+ keine_spekulation) / pass^3 streng | 60% / 40% |
| Pflicht-Eingriffe (Stop-Hook) | nicht vorhanden (vor v3) |
| Pflicht erfüllt ohne Eingriff | 98% |
| Kosten Agent gesamt | 1.1827 USD |
| Kosten Agent pro Lauf (Mittel) | 0.0263 USD |
| Kosten pro 1000 Tickets (Agent) | 26.28 USD |
| Kosten Judge gesamt | 0.9018 USD |
| Latenz gesamt p50 / p95 | 24.2 s / 41.5 s |
|   davon SDK-Start p50 / p95 | 0.2 s / 0.6 s |
|   davon Agent (init bis Ergebnis) p50 / p95 | 22.8 s / 40.3 s |
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
| T01 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | – | 5.0 | 0.0294 | 28.6 s | 27.0 s |
| T02 | 0/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 1/3 | – | 5.0 | 0.0283 | 28.5 s | 27.2 s |
| T03 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | – | 5.0 | 0.0250 | 24.8 s | 23.4 s |
| T04 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | – | 5.0 | 0.0261 | 25.3 s | 24.0 s |
| T05 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | – | 5.0 | 0.0303 | 32.4 s | 31.2 s |
| T06 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | – | 4.0 | 0.0261 | 26.2 s | 24.8 s |
| T07 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 2/3 | – | 5.0 | 0.0391 | 43.9 s | 42.9 s |
| T08 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | – | 3.7 | 0.0199 | 15.7 s | 14.1 s |
| T09 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | – | 4.0 | 0.0252 | 23.2 s | 21.9 s |
| T10 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | – | 3.0 | 0.0197 | 18.4 s | 17.0 s |
| T11 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | – | 3.7 | 0.0254 | 23.7 s | 22.2 s |
| T12 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | – | 3.0 | 0.0184 | 17.0 s | 15.6 s |
| T13 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | – | 5.3 | 0.0254 | 27.5 s | 26.1 s |
| T14 | 2/3 | 2/3 | 3/3 | 3/3 | 2/3 | 2/3 | 2/3 | – | 4.3 | 0.0303 | 26.6 s | 25.5 s |
| T15 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | – | 5.0 | 0.0256 | 23.4 s | 22.1 s |

## Entwürfe mit Spekulation (keine_spekulation = false)

- `T01_lauf2`: Die Aussage 'Das ist ein Fehler von unserer Seite' ist eine unbelegte Ursachenbehauptung, die nirgends in der Trajektorie steht – dort wird nur die doppelte Belastung festgestellt, nicht deren Ursache.
- `T02_lauf1`: Die Aussage, das Team werde sich 'in den nächsten Stunden' melden, ist eine konkrete zeitliche Zusage, die in der Trajektorie nicht enthalten ist und somit spekulativ ist.
- `T02_lauf2`: Die Zusage 'erstatten wir dir den doppelten Betrag sofort' ist eine konkrete, nicht durch die Trajektorie gedeckte Festlegung auf Zeitpunkt und Ergebnis, da laut Daten nur eine Zahlung vorliegt und der Fall erst zur Klärung übergeben wurde.
- `T04_lauf1`: Der Entwurf erfindet mit der Aussage 'in den nächsten 1–2 Tagen überprüfen' eine konkrete Frist für die interne Prüfung, die in der Trajektorie nirgends genannt wird (dort steht nur 'wartet_auf_freigabe').
- `T04_lauf3`: Der Satz 'die 59$ hätten nicht abgebucht werden sollen, wenn du nicht kündigen wolltest' unterstellt einen Fehler beim Abbuchen, obwohl laut Trajektorie das Abo aktiv war und die automatische Verlängerung planmäßig erfolgte – diese Bewertung des Hergangs ist nicht durch die Daten gedeckt.
- `T06_lauf1`: Der Entwurf enthält mehrere unbelegte Behauptungen: die 14-Tage-Frist und 'problemlose' Erstattung bei Apple stammen aus der FocusFlow-eigenen Richtlinie, nicht aus Angaben über Apples Prozess, ebenso sind die konkreten UI-Schritte bei Apple ('Ich möchte diese Zahlung nicht erstatten') und die Dauer 'ein paar Tage' nicht in der Trajektorie belegt.
- `T06_lauf2`: Die Aussage 'Apple kümmert sich dann um die volle Rückerstattung' ist eine konkrete Ergebniszusage, die nicht durch die Trajektorie gedeckt ist – der Hilfeartikel sagt lediglich, dass dort die Richtlinien des jeweiligen Stores gelten, nicht dass eine volle Erstattung garantiert ist. Auch die Formulierung 'Apple hat die volle Kontrolle über diese Transaktionen' geht über die im Artikel genannte technische Unmöglichkeit hinaus.
- `T06_lauf3`: Die Aussage, Apple bearbeite solche Anträge 'normalerweise sehr zügig', ist eine unbelegte Spekulation, die in der Trajektorie nicht vorkommt und dem Kunden eine konkrete Erwartung suggeriert.
- `T07_lauf3`: Der Entwurf verspricht eine 'Erstattung der bisherigen Überzahlungen', obwohl der Hilfeartikel ausdrücklich festhält, dass eine automatische Erstattung des gekündigten Abos nicht erfolgt und die Trajektorie keine Erstattungszusage enthält – das ist eine unbelegte, konkrete Zusage.
- `T09_lauf2`: Die meisten Aussagen sind durch Kundendaten und den Hilfeartikel gedeckt, aber die Formulierung 'in den letzten anderthalb Wochen' setzt ein aktuelles Datum voraus, das nirgends in der Trajektorie angegeben ist, und ist damit eine unbelegte konkrete Zeitangabe.
- `T11_lauf2`: Der Entwurf behauptet, die 14-Tage-Frist sei bereits abgelaufen, obwohl in der Trajektorie kein aktuelles Datum vorliegt, mit dem das Kaufdatum (02.03.2026) verglichen werden könnte – dies ist eine unbelegte Zeitangabe/Vermutung.
- `T11_lauf3`: Der Entwurf erfindet konkrete Fristen für Google Play ('üblicherweise bis 48 Stunden nach Kauf, je nach Fall auch bis 15 Tage'), die in der Trajektorie nirgends stehen – dort wird nur allgemein auf die Richtlinien des jeweiligen Stores verwiesen, ohne Zahlen zu nennen. Zudem wird die 14-Tage-Frist als Ablehnungsgrund genannt, obwohl laut Artikel bei Store-Käufen ohnehin keine eigene Erstattung möglich ist, unabhängig von der Frist.
- `T13_lauf1`: Die Aussage 'Dein Abo wurde zwar abgebucht' ist durch die Trajektorie nicht gedeckt, da die Zahlungsabfrage keine Zahlung ergab, und die konkrete Zusage 'Jemand aus unserem Team wird sich noch heute bei dir melden' ist eine Frist, die in der Trajektorie nicht vorkommt.
- `T13_lauf2`: Der Entwurf behauptet, das Problem 'könne gelegentlich bei der App Store-Synchronisation passieren' – dies ist eine spekulative Ursachenzuschreibung, die in der Trajektorie nicht als Tatsache, sondern höchstens als Vermutung des Agents in der internen Übergabe steht, und wird dem Kunden fälschlich als plausible Erklärung präsentiert.
- `T13_lauf3`: Der Entwurf behauptet als Erklärung 'Sync-Verzögerungen zwischen Apple und unserem System' bzw. 'technischer Fehler', obwohl dies in der Trajektorie nur als vage Vermutung des Agents im Übergabegrund steht, nicht als festgestellte Tatsache. Zudem wird eine konkrete Frist ('1–2 Werktagen') zugesagt, die in der Trajektorie nicht vorkommt.
- `T14_lauf2`: Der Entwurf behauptet unbelegt, das Team könne 'schnell' verifizieren und werde danach das Abo kündigen – beides sind konkrete Zusagen zu Tempo und Ergebnis, die in der Trajektorie nicht enthalten sind.

## Fehlgeschlagene Läufe

- `T02_lauf1`: uebergabe_ok, entwurf_ok. entwurf: Der Entwurf teilt Ben nicht klar mit, dass laut FocusFlow-System im September nur eine Abbuchung über 6,99 USD verzeichnet ist – die Kernaussage fehlt, stattdessen wird nur allgemein auf Vormerkung oder echte Doppelbuchung verwiesen.
- `T02_lauf2`: uebergabe_ok, entwurf_ok. entwurf: Die Soll-Kernaussage, dass im September nachweislich nur eine Abbuchung über 6,99 USD erfolgt ist, wird im Entwurf nicht vermittelt; stattdessen bleibt offen, ob eine echte Doppelbuchung vorliegt, und der Fall wird zur Klärung weitergeleitet, was der klaren Aussage widerspricht.
- `T02_lauf3`: uebergabe_ok, entwurf_ok. entwurf: Die Soll-Kernaussage – dass laut Zahlungsdaten im September nur eine Abbuchung über 6,99 USD erfolgt ist und keine Doppelabbuchung vorliegt – wird im Entwurf nicht vermittelt; stattdessen wird nur angekündigt, dies noch zu prüfen. Damit fehlt die eigentliche Hauptaussage.
- `T07_lauf3`: entwurf_ok. entwurf: Die Kernaussage, dass eines der beiden Pro-Abos vor der Zusammenführung gekündigt werden muss und auslaufen muss, weil nur ein Konto Pro haben darf, fehlt im Entwurf vollständig. Stattdessen wird nur pauschal auf eine spätere Klärung durch den Support verwiesen.
- `T13_lauf1`: entwurf_ok. entwurf: Der Entwurf erwähnt zwar die Übergabe an ein Team, nennt aber nicht den entscheidenden Grund (keine Zahlung zum Konto auffindbar) und behauptet stattdessen fälschlich, die Abbuchung sei bestätigt – das widerspricht der Kernaussage, die ja gerade besagt, dass keine Zahlung gefunden wurde.
- `T13_lauf2`: entwurf_ok. entwurf: Die Kernaussage – dass die Weiterleitung erfolgt, weil zu diesem Konto keine Zahlung zu finden ist – fehlt im Entwurf. Stattdessen wird eine andere, unbelegte Ursache (App Store-Synchronisationsproblem) genannt, was der eigentlichen Begründung widerspricht bzw. sie verschleiert.
- `T13_lauf3`: entwurf_ok. entwurf: Der Entwurf teilt zwar mit, dass der Fall an ein Team weitergeleitet wurde, nennt aber nicht den in der Trajektorie festgehaltenen Grund – dass zu diesem Konto keine Zahlung gefunden wurde. Stattdessen wird eine andere, nicht belegte Erklärung (Sync-Fehler mit Apple) präsentiert, wodurch die Soll-Kernaussage nicht vermittelt wird.
- `T14_lauf1`: pflicht_ok, uebergabe_ok, entwurf_ok. fehlt: an_mensch_uebergeben; entwurf: Die Soll-Kernaussage verlangt, dass die Anfrage wegen Nichtverifizierbarkeit des anderen Kontos an einen Mitarbeiter weitergegeben wird. Der Entwurf erwähnt weder eine Verifizierungsproblematik noch eine Weiterleitung, sondern erklärt dem Kunden direkt, wie er selbst in Google Play kündigen kann – das widerspricht der geforderten Eskalation.
