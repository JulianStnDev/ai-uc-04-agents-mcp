# Eval-Ergebnisse `v1`

15 Tickets × bis zu 3 Läufe = 45 Läufe. Modell Agent: Haiku 4.5, Judge: claude-sonnet-5.

## Kernzahlen

| Metrik | Wert |
|---|---|
| Erfolgsquote pro Lauf | 80% |
| pass^3 (alle Läufe eines Tickets erfolgreich) | 67% |
| pflicht_ok | 98% |
| verboten_ok | 100% |
| erstattung_ok | 100% |
| uebergabe_ok | 91% |
| entwurf_ok | 80% |
| Kosten Agent gesamt | 1.1827 USD |
| Kosten Agent pro Lauf (Mittel) | 0.0263 USD |
| Kosten pro 1000 Tickets (Agent) | 26.28 USD |
| Kosten Judge gesamt | 0.1666 USD |
| Latenz gesamt p50 / p95 | 24.2 s / 41.5 s |
|   davon SDK-Start p50 / p95 | 0.2 s / 0.6 s |
|   davon Agent (init bis Ergebnis) p50 / p95 | 22.8 s / 40.3 s |
|   davon SDK-Ende p50 / p95 | 1.1 s / 1.3 s |

## Erstattungen im Schattenmodus

| Kategorie | Läufe |
|---|---|
| richtig_empfohlen | 9 |
| richtig_keine | 36 |

## Pro Ticket

| Ticket | Erfolg | pflicht | verboten | erstattung | übergabe | entwurf | Aufrufe Ø | Kosten Ø | Latenz Ø gesamt | davon Agent Ø |
|---|---|---|---|---|---|---|---|---|---|---|
| T01 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 5.0 | 0.0294 | 28.6 s | 27.0 s |
| T02 | 0/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 5.0 | 0.0283 | 28.5 s | 27.2 s |
| T03 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 5.0 | 0.0250 | 24.8 s | 23.4 s |
| T04 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 5.0 | 0.0261 | 25.3 s | 24.0 s |
| T05 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 5.0 | 0.0303 | 32.4 s | 31.2 s |
| T06 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 4.0 | 0.0261 | 26.2 s | 24.8 s |
| T07 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 5.0 | 0.0391 | 43.9 s | 42.9 s |
| T08 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3.7 | 0.0199 | 15.7 s | 14.1 s |
| T09 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 4.0 | 0.0252 | 23.2 s | 21.9 s |
| T10 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3.0 | 0.0197 | 18.4 s | 17.0 s |
| T11 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3.7 | 0.0254 | 23.7 s | 22.2 s |
| T12 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3.0 | 0.0184 | 17.0 s | 15.6 s |
| T13 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 5.3 | 0.0254 | 27.5 s | 26.1 s |
| T14 | 2/3 | 2/3 | 3/3 | 3/3 | 2/3 | 2/3 | 4.3 | 0.0303 | 26.6 s | 25.5 s |
| T15 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 5.0 | 0.0256 | 23.4 s | 22.1 s |

## Fehlgeschlagene Läufe

- `T02_lauf1`: uebergabe_ok, entwurf_ok. entwurf: Der Entwurf bestätigt nicht, dass nur eine Abbuchung erfolgt ist, sondern lässt offen, ob eine Doppelabbuchung vorliegt und verspricht ggf. eine Erstattung – das widerspricht der Soll-Kernaussage, dass keine Doppelabbuchung vorliegt.
- `T02_lauf2`: uebergabe_ok, entwurf_ok. entwurf: Der Entwurf bestätigt nicht, dass im September nur eine Abbuchung erfolgt ist, sondern lässt die Frage offen und verweist auf weitere Prüfung durch das Support-Team – die Kernaussage fehlt somit vollständig.
- `T02_lauf3`: uebergabe_ok, entwurf_ok. entwurf: Der Entwurf teilt dem Kunden nicht mit, dass laut Prüfung im September nur eine einzige Abbuchung erfolgt ist, sondern verspricht lediglich eine noch ausstehende Prüfung und ggf. Erstattung – die geforderte Kernaussage fehlt somit vollständig.
- `T07_lauf3`: entwurf_ok. entwurf: Der Entwurf erklärt nur, dass der Support sich um die Doppelzahlung kümmert und eine Erstattung bespricht, nennt aber nicht die Kernaussage, dass vor dem Zusammenführen eines der beiden Pro-Abos gekündigt werden muss, da nur ein Konto Pro haben darf.
- `T11_lauf3`: entwurf_ok. entwurf: Der Entwurf nennt fälschlich eine FocusFlow-eigene 14-Tage-Erstattungsfrist als Grund für die Ablehnung, was der Kernaussage widerspricht, dass FocusFlow grundsätzlich nicht erstatten kann und die Erstattung nur über Google Play läuft – der Verweis auf Google Play ist zwar enthalten, aber die falsche Begründung verfälscht die Kernaussage.
- `T13_lauf1`: entwurf_ok. entwurf: Der Entwurf bestätigt die Abbuchung als Fakt ('Dein Abo wurde zwar abgebucht'), während die Soll-Kernaussage besagt, dass keine Zahlung zu diesem Konto gefunden wurde – das ist ein klarer Widerspruch. Zudem fehlt der Hinweis auf die fehlende Zahlung als Grund für die Weiterleitung.
- `T13_lauf2`: entwurf_ok. entwurf: Der Entwurf leitet den Fall zwar weiter, nennt aber als Grund eine App Store-Synchronisationsverzögerung statt der tatsächlichen Ursache, dass keine Zahlung zum Konto gefunden wurde – das widerspricht der Kernaussage.
- `T13_lauf3`: entwurf_ok. entwurf: Der Entwurf leitet das Anliegen zwar weiter, nennt aber als Grund eine mögliche Sync-Verzögerung zwischen Apple und dem System statt der tatsächlichen Ursache, dass keine Zahlung zum Konto gefunden wurde – damit widerspricht er der Soll-Kernaussage.
- `T14_lauf1`: pflicht_ok, uebergabe_ok, entwurf_ok. fehlt: an_mensch_uebergeben; entwurf: Der Entwurf erklärt eine Selbstkündigung über Google Play, anstatt die Anfrage aufgrund fehlender Verifizierung des anderen Kontos an einen Mitarbeiter weiterzuleiten – die Kernaussage fehlt und wird widersprochen.
