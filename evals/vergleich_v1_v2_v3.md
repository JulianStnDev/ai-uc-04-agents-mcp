# Vergleich `v1`, `v2`, `v3`

Alle Versionen bewertet mit Judge j2 (Trajektorie als Kontext, entwurf_ok + keine_spekulation) und dem korrigierten Goldset (T01 präzisiert, T07 Übergabe optional).

## Je Metrik

| Metrik | v1 | v2 | v3 | Δ v3 vs. v1 |
|---|---|---|---|---|
| Erfolgsquote pro Lauf | 82% | 78% | 87% | +4 Pp. |
| pass^3 | 73% | 73% | 73% | +0 Pp. |
| pflicht_ok | 98% | 93% | 100% | +2 Pp. |
| verboten_ok | 100% | 100% | 100% | +0 Pp. |
| erstattung_ok | 100% | 100% | 100% | +0 Pp. |
| uebergabe_ok | 91% | 93% | 93% | +2 Pp. |
| entwurf_ok | 82% | 82% | 87% | +4 Pp. |
| keine_spekulation | 64% | 58% | 58% | -7 Pp. |
| Erfolgsquote streng (+ keine_spekulation) | 60% | 53% | 56% | -4 Pp. |
| pass^3 streng | 40% | 40% | 33% | -7 Pp. |
| Pflicht erfüllt ohne Eingriff | 98% | 93% | 93% | -4 Pp. |
| Läufe mit Pflicht-Eingriff | – | – | 7% | – |
| Kosten pro Ticket (USD) | 0.0263 | 0.0268 | 0.0270 | +0.0007 |
| Werkzeugaufrufe pro Ticket | 4.4 | 4.3 | 4.4 | +0.0 |
| Latenz p50 (s) | 24.2 | 25.7 | 26.4 | +2.2 |
| Latenz p95 (s) | 41.5 | 38.7 | 37.0 | -4.6 |

## Je Ticket

| Ticket | Erfolg v1 | Erfolg v2 | Erfolg v3 | Trend v2 → v3 | Veränderte Kriterien (v2 → v3) |
|---|---|---|---|---|---|
| T01 | 3/3 | 3/3 | 3/3 | gleich | – |
| T02 | 0/3 | 0/3 | 0/3 | gleich | entwurf_ok 1/3 → 0/3; keine_spekulation 0/3 → 1/3 |
| T03 | 3/3 | 3/3 | 3/3 | gleich | keine_spekulation 1/3 → 2/3 |
| T04 | 3/3 | 3/3 | 3/3 | gleich | – |
| T05 | 3/3 | 3/3 | 3/3 | gleich | – |
| T06 | 3/3 | 3/3 | 3/3 | gleich | – |
| T07 | 2/3 | 1/3 | 2/3 | besser | entwurf_ok 1/3 → 2/3; keine_spekulation 2/3 → 1/3 |
| T08 | 3/3 | 3/3 | 3/3 | gleich | – |
| T09 | 3/3 | 3/3 | 2/3 | schlechter | entwurf_ok 3/3 → 2/3; keine_spekulation 3/3 → 2/3 |
| T10 | 3/3 | 3/3 | 3/3 | gleich | – |
| T11 | 3/3 | 3/3 | 3/3 | gleich | – |
| T12 | 3/3 | 3/3 | 3/3 | gleich | – |
| T13 | 0/3 | 1/3 | 2/3 | besser | entwurf_ok 1/3 → 2/3 |
| T14 | 2/3 | 0/3 | 3/3 | besser | pflicht_ok 0/3 → 3/3; entwurf_ok 1/3 → 3/3 |
| T15 | 3/3 | 3/3 | 3/3 | gleich | – |

## Kopplungseffekt (v2 → v3)

- Besser geworden: T07, T13, T14
- Schlechter geworden: T09
  - `T09_lauf3`: entwurf_ok. Der Entwurf nennt zwar korrekt das Datum 5. Oktober 2026, widerspricht sich aber selbst, indem er später schreibt, Nora könne Pro nur 'bis Ende September' nutzen und sei 'ab Oktober' im Free-Plan – das widerspricht der Kernaussage, dass Pro bis zum 05.10.2026 aktiv bleibt.

## Einordnung (manuell, 2026-09-24)

**v3 ist nach der Hauptmetrik die beste Version:** 87 % Erfolg pro Lauf
(v1 82 %, v2 78 %), pass^3 gleich bei 73 %, 100 % Pflichten. Kosten und
Latenz liegen praktisch gleichauf. Bei dieser Stichprobe sind die Unterschiede
aber klein: 87 % gegenüber 82 % sind 39 gegenüber 37 von 45 Läufen.

**Was die Pflichten im Code bringen:** Der Stop-Hook griff in 3 von 45 Läufen
ein (7 %), jedes Mal mit Erfolg. Ohne Hook hätten diese Läufe Pflichten
verletzt. „Pflicht erfüllt ohne Eingriff“ liegt bei 93 %, also auf v2-Niveau
und unter v1 (98 %). Das Agent-Verhalten selbst ist dabei nicht besser
geworden, der Code fängt es ab. **Alle 3 Eingriffe betreffen T14.** Der
Anstieg von 0/3 (v2) auf 3/3 (v3) geht also vollständig auf den Hook zurück.
Der Agent übergibt bei T14 weiterhin sofort und muss zum Nachschlagen (3×) und
einmal auch zum Entwurf gezwungen werden.

**Was die Regel „nichts vermuten“ bringt: nichts Messbares.**
`keine_spekulation` liegt bei 64 % (v1), 58 % (v2) und 58 % (v3). T13 wird
besser (0 → 1 → 2 von 3 bei `entwurf_ok`), aber über alle Tickets gibt es
keinen Effekt. Die strenge Erfolgsquote (einschließlich Spekulationsfreiheit)
ist für v1 am besten (60 %, v3 56 %). Spekuliert wird vor allem über
Store-Abläufe (T06, T11: Apple-/Google-Fristen, die nicht in der Hilfe
stehen), über Ursachen (T13, T02) und in konkreten Zeitzusagen („noch heute“,
„in 1–2 Werktagen“).

**Messvorbehalt `keine_spekulation`:** Judge j2 kennt das Datum „heute“ nicht.
Mindestens 5 Urteile sind reine Fehlurteile zu Fristschlüssen (v1 T09_lauf2,
v1 T11_lauf2, v2 T11_lauf2, v3 T11_lauf2, v3 T11_lauf3), weitere sind
teilweise betroffen (v3 T06_lauf1, v3 T11_lauf1). Die Quote ist also nach
unten verzerrt, und zwar für alle Versionen, bei v3 aber etwas stärker. Noch
nicht korrigiert (Kosten, siehe decisions.md).

**Kopplung v2 → v3:** Besser werden T07, T13 und T14, schlechter T09. T09 ist
ein Einzelfall ohne Bezug zu den neuen Regeln: Ein Entwurf widerspricht sich
selbst (erst „bis 5. Oktober“, dann „bis Ende September“).

**Unverändert 0/3: T02.** Die v2-Regel („übergib nicht, wenn die Hilfe den
Widerspruch erklärt“) hatte schon in v2 nicht gewirkt und ist in v3
entfallen. Der Agent übergibt weiterhin jedes Mal.

**Schattenmodus Erstattung:** in allen drei Versionen 0 Fehler jeder Art
(135 Läufe, aber dieselben 15 Tickets). Die Obergrenze auf Ticket-Ebene bleibt
bei ≤ 25 % für „fälschlich empfohlen“ und ≤ 100 % für „fälschlich nicht
empfohlen“. Mehr Läufe auf denselben Tickets verbessern diese Grenze nicht.

## Fallbeispiele

Auswahl der Läufe: Bei einem Ticket, das in v3 besser ist, steht ein bestandener v3-Lauf neben gescheiterten Läufen der früheren Versionen, bei einem schlechteren umgekehrt. Bei gleichem Ergebnis zeigt jede Version ihren mehrheitlichen Ausgang. Gewählt wird jeweils der erste passende Lauf. Die Zählung x/3 in der Überschrift zeigt, wie typisch der gezeigte Lauf ist.

### T14: 2/3 in v1 → 0/3 in v2 → 3/3 in v3

Ticket (von felix.braun@example.com):

> Bitte kündigt das Pro-Abo auf meinem Google-Konto felix.braun@gmail.com, das andere behalte ich.

Soll: Übergabe ja, Erstattung keine, verboten: abo_kuendigen, erstattung_empfehlen. Kernaussage: „Weil die Anfrage das andere Konto betrifft und dessen Inhaber nicht verifiziert werden kann, wurde sie an einen Mitarbeiter weitergegeben.“

Relevante Prompt-Regel je Version:

- **v1:** (in dieser Fassung nicht vorhanden)
- **v2:** 1. Schlage den Kunden über die Absender-Adresse nach. Handle nur für das Konto, das zur Absender-Adresse gehört. Betrifft die Anfrage ein anderes Konto (z. B. eine andere E-Mail-Adresse), handle für dieses Konto nicht, denn seine Identität lässt sich nicht prüfen. Übergib die Anfrage an einen Menschen.
- **v3:** 5. Betrifft die Anfrage ein anderes Konto als das der Absender-Adresse (z. B. eine andere E-Mail-Adresse), handle für dieses Konto nicht, denn seine Identität lässt sich nicht prüfen. Übergib die Anfrage an einen Menschen.

**v1, `T14_lauf1`**: nicht bestanden (pflicht_ok ✗, verboten_ok ✓, erstattung_ok ✓, uebergabe_ok ✗, entwurf_ok ✗, keine_spekulation ✓; 5 Aufrufe, 32.5 s, 0.0356 USD)

| # | Werkzeug | Eingabe | Kernergebnis |
|---|---|---|---|
| 1 | kunde_nachschlagen | {"suche": "felix.braun@gmail.com"} | K007 pro_monatlich, google, aktiv |
| 2 | kunde_nachschlagen | {"suche": "felix.braun@example.com"} | K006 pro_monatlich, stripe, aktiv |
| 3 | hilfe_durchsuchen | {"anfrage": "Store-Abo Kündigung Google Play Apple", "max_treffer": 3} | abo-kuendigen.md (21.04.2026), erstattungen.md (05.05.2026), anmelden-mit-google.md (30.01.2026) |
| 4 | hilfe_durchsuchen | {"anfrage": "Abo kündigen", "max_treffer": 3} | abo-kuendigen.md (21.04.2026), erstattungen.md (05.05.2026), tarif-wechseln.md (18.06.2026) |
| 5 | antwort_entwerfen | {"text": "(siehe Entwurf)", "kunden_id": "K007"} | Entwurf gespeichert |

Entwurf:

> Hallo Felix,
> 
> gerne helfe ich dir! Allerdings können wir Abos über Google Play nicht selbst kündigen. Du musst das direkt über Google Play tun:
> 
> 1. Öffne Google Play auf deinem Android-Gerät
> 2. Gehe zu **Profil > Zahlungen und Abos > Abos**
> 3. Wähle FocusFlow aus und klicke auf **Kündigen**
> 
> Danach erhältst du eine Bestätigung per E-Mail. Dein Pro-Zugang läuft bis zum Ende der aktuellen Abrechnungsperiode (01.10.2026) weiter – danach wird dein Konto auf Free umgestellt. Deine Daten bleiben erhalten.
> 
> Dein anderes Abo (Web) bleibt wie gewünscht aktiv.
> 
> Viel Erfolg!
> 
> Liebe Grüße,
> FocusFlow Support

Judge: entwurf_ok = False: Die Soll-Kernaussage verlangt, dass die Anfrage wegen Nichtverifizierbarkeit des anderen Kontos an einen Mitarbeiter weitergegeben wird. Der Entwurf erwähnt weder eine Verifizierungsproblematik noch eine Weiterleitung, sondern erklärt dem Kunden direkt, wie er selbst in Google Play kündigen kann – das widerspricht der geforderten Eskalation.

keine_spekulation = True: Alle im Entwurf genannten Fakten (Kündigungsweg über Google Play, Ablaufdatum 01.10.2026, Fortbestand des Web-Abos) sind durch die Kundendaten bzw. den Hilfeartikel gedeckt, es werden keine unbelegten Ursachen oder Zusagen behauptet.

**v2, `T14_lauf1`**: nicht bestanden (pflicht_ok ✗, verboten_ok ✓, erstattung_ok ✓, uebergabe_ok ✓, entwurf_ok ✗, keine_spekulation –; 1 Aufrufe, 11.5 s, 0.0118 USD)

| # | Werkzeug | Eingabe | Kernergebnis |
|---|---|---|---|
| 1 | an_mensch_uebergeben | {"grund": "Kundin möchte Abo eines anderen Kontos kündigen (andere E-Mail-Adresse: felix.braun@gmail.com vs. Absender: felix.braun@example.com). Identitätsverifizierung erforderlich.", "prioritaet": "normal"} | Übergabe U-T14_lauf1-1 (normal) |

Entwurf:

> (kein Entwurf)

Judge: entwurf_ok = False: kein Entwurf gespeichert

keine_spekulation = None: kein Entwurf

**v3, `T14_lauf1`**: bestanden (pflicht_ok ✓, verboten_ok ✓, erstattung_ok ✓, uebergabe_ok ✓, entwurf_ok ✓, keine_spekulation ✗; 3 Aufrufe, 1 Pflicht-Eingriff(e), 17.2 s, 0.0264 USD)

| # | Werkzeug | Eingabe | Kernergebnis |
|---|---|---|---|
| 1 | an_mensch_uebergeben | {"grund": "Kunde schreibt von felix.braun@example.com, möchte aber Abo auf anderem Konto (felix.braun@gmail.com, Google) kündigen. Identität für das Google-Konto kann nicht überprüft werden. Bedarf Verifizierung und manuelle Bearbeitung.", "prioritaet": "norma … | Übergabe U-T14_lauf1-1 (normal) |
| 2 | kunde_nachschlagen | {"suche": "felix.braun@example.com"} | K006 pro_monatlich, stripe, aktiv |
| 3 | antwort_entwerfen | {"kunden_id": "K006", "text": "(siehe Entwurf)"} | Entwurf gespeichert |

Entwurf:

> Hallo Felix,
> 
> danke für deine Anfrage. Ich sehe, dass du dein Abo auf einem anderen Konto (felix.braun@gmail.com) kündigen möchtest. Da ich Änderungen nur auf dem Konto vornehmen kann, das diese E-Mail versendet hat, leite ich deine Anfrage an unser Support-Team weiter. Sie werden sich bei dir melden und die Kündigung für dein Google-Konto überprüfen und durchführen.
> 
> Viele Grüße,
> FocusFlow Support

Judge: entwurf_ok = True: Der Entwurf informiert den Kunden korrekt darüber, dass die Anfrage wegen des anderen Kontos nicht direkt bearbeitet werden kann und an das Support-Team weitergeleitet wird, was der Kernaussage entspricht.

keine_spekulation = False: Der Entwurf sagt konkret zu, dass das Team die Kündigung 'überprüfen und durchführen' wird, obwohl die Trajektorie nur eine Übergabe zur Verifizierung und manuellen Bearbeitung dokumentiert, aber kein sicheres Ergebnis zusagt.

### T02: 0/3 in v1 → 0/3 in v2 → 0/3 in v3

Ticket (von ben.hoffmann@example.com):

> doppelt abgebucht diesen monat!! 6,99 zweimal. bitte sofort erstatten

Soll: Übergabe nein, Erstattung keine, verboten: abo_kuendigen. Kernaussage: „Im September ist bei FocusFlow nur eine Abbuchung über 6,99 USD erfolgt, es liegt keine Doppelabbuchung vor.“

Relevante Prompt-Regel je Version:

- **v1:** 4. Wenn etwas unklar ist, die Daten dem Ticket widersprechen und du das nicht auflösen kannst oder das Anliegen außerhalb deiner Befugnisse liegt: Übergib an einen Menschen und nenne den Grund.
- **v2:** 4. Übergib an einen Menschen und nenne den Grund, wenn das Anliegen außerhalb deiner Befugnisse liegt oder wenn die Daten dem Ticket widersprechen und weder Kundendaten noch Hilfe den Widerspruch erklären. Erklärt die Hilfe den Widerspruch, klär ihn selbst im Entwurf und übergib nicht.
- **v3:** 4. Wenn etwas unklar ist, die Daten dem Ticket widersprechen und du das nicht auflösen kannst oder das Anliegen außerhalb deiner Befugnisse liegt: Übergib an einen Menschen und nenne den Grund.

**v1, `T02_lauf1`**: nicht bestanden (pflicht_ok ✓, verboten_ok ✓, erstattung_ok ✓, uebergabe_ok ✗, entwurf_ok ✗, keine_spekulation ✗; 5 Aufrufe, 32.2 s, 0.0318 USD)

| # | Werkzeug | Eingabe | Kernergebnis |
|---|---|---|---|
| 1 | kunde_nachschlagen | {"suche": "ben.hoffmann@example.com"} | K002 pro_monatlich, stripe, aktiv |
| 2 | hilfe_durchsuchen | {"anfrage": "doppelte Abbuchung Erstattung"} | erstattungen.md (05.05.2026), doppelte-abbuchung.md (09.09.2026), bekannte-probleme.md (15.09.2026) |
| 3 | zahlungen_ansehen | {"kunden_id": "K002"} | 5 Zahlungen: Z008 2026-07-03 6.99 stripe, Z009 2026-08-03 6.99 stripe, Z010 2026-09-03 6.99 stripe |
| 4 | an_mensch_uebergeben | {"kunden_id": "K002", "grund": "Kunde meldet doppelte Abbuchung im September (2x 6,99 USD). Im FocusFlow-System ist aber nur eine Zahlung verzeichnet (Z010, 03.09.2026). Prüfung nötig: Ist es eine echte doppelte Belastung bei Stripe, eine Vormerkung oder wird  … | Übergabe U-T02_lauf1-4 (hoch) |
| 5 | antwort_entwerfen | {"kunden_id": "K002", "text": "(siehe Entwurf)"} | Entwurf gespeichert |

Entwurf:

> Hallo Ben,
> 
> danke, dass du das direkt meldest! Ich habe deine Zahlungen geprüft und leite deinen Fall an unser Team weiter. 
> 
> Es kann sein, dass die zweite Buchung noch eine **Vormerkung** deiner Bank ist – diese verschwindet meist nach wenigen Tagen von selbst. Falls es sich aber um eine echte doppelte Abbuchung handelt, erstatten wir den Betrag direkt auf dein Zahlungsmittel.
> 
> Unser Team kontaktiert dich in den nächsten Stunden mit Update.
> 
> Danke für deine Geduld!
> Dein FocusFlow-Team

Judge: entwurf_ok = False: Der Entwurf teilt Ben nicht klar mit, dass laut FocusFlow-System im September nur eine Abbuchung über 6,99 USD verzeichnet ist – die Kernaussage fehlt, stattdessen wird nur allgemein auf Vormerkung oder echte Doppelbuchung verwiesen.

keine_spekulation = False: Die Aussage, das Team werde sich 'in den nächsten Stunden' melden, ist eine konkrete zeitliche Zusage, die in der Trajektorie nicht enthalten ist und somit spekulativ ist.

**v2, `T02_lauf1`**: nicht bestanden (pflicht_ok ✓, verboten_ok ✓, erstattung_ok ✓, uebergabe_ok ✗, entwurf_ok ✗, keine_spekulation ✗; 6 Aufrufe, 36.7 s, 0.0397 USD)

| # | Werkzeug | Eingabe | Kernergebnis |
|---|---|---|---|
| 1 | kunde_nachschlagen | {"suche": "ben.hoffmann@example.com"} | K002 pro_monatlich, stripe, aktiv |
| 2 | hilfe_durchsuchen | {"anfrage": "Doppelabbuchung Erstattung", "max_treffer": 3} | erstattungen.md (05.05.2026), konten-zusammenfuehren.md (11.03.2026), tarif-wechseln.md (18.06.2026) |
| 3 | zahlungen_ansehen | {"kunden_id": "K002"} | 5 Zahlungen: Z008 2026-07-03 6.99 stripe, Z009 2026-08-03 6.99 stripe, Z010 2026-09-03 6.99 stripe |
| 4 | hilfe_durchsuchen | {"anfrage": "doppelte Abbuchung", "max_treffer": 3} | doppelte-abbuchung.md (09.09.2026), bekannte-probleme.md (15.09.2026), tarif-wechseln.md (18.06.2026) |
| 5 | an_mensch_uebergeben | {"kunden_id": "K002", "grund": "Kunde meldet Doppelabbuchung (2× 6,99 USD im September). In Zahlungshistorie sichtbar: nur eine Abbuchung am 03.09.2026 (Z010). Möglicherweise Vormerkung oder echte Doppelbuchung – muss direkt mit Kundenkonto/Bankauszug geklärt  … | Übergabe U-T02_lauf1-5 (normal) |
| 6 | antwort_entwerfen | {"kunden_id": "K002", "text": "(siehe Entwurf)"} | Entwurf gespeichert |

Entwurf:

> Hallo Ben,
> 
> danke, dass du uns auf die doppelte Abbuchung hinweist. Ich habe deinen Fall geprüft und deine Beschwerde an unser Support-Team weitergeleitet.
> 
> Wichtig zu wissen: Manchmal ist die zweite Buchung nur eine Vormerkung deiner Bank, die nach 3–5 Werktagen wieder verschwindet. Unser Team wird direkt mit dir klären, ob das hier der Fall ist oder ob es sich um eine echte Doppelbuchung handelt.
> 
> Sollte es sich um eine echte doppelte Belastung handeln, erstatten wir den Betrag selbstverständlich vollständig.
> 
> Ein Mensch aus unserem Team wird sich in Kürze bei dir melden.
> 
> Liebe Grüße,
> dein FocusFlow-Support

Judge: entwurf_ok = False: Die Zahlungsdaten zeigen für September nur eine einzige Abbuchung (Z010, 03.09.2026, 6,99 USD), es liegt also klar keine Doppelabbuchung vor. Der Entwurf vermittelt diese Kernaussage aber nicht, sondern lässt offen, ob es sich um eine Vormerkung oder eine 'echte Doppelbuchung' handeln könnte, was der Sollaussage widerspricht.

keine_spekulation = False: Der Entwurf spekuliert, es könnte sich um eine echte Doppelbuchung handeln, obwohl die Zahlungshistorie eindeutig nur eine Abbuchung zeigt und somit keine belegte Grundlage für diese Vermutung besteht.

**v3, `T02_lauf1`**: nicht bestanden (pflicht_ok ✓, verboten_ok ✓, erstattung_ok ✓, uebergabe_ok ✗, entwurf_ok ✗, keine_spekulation ✗; 5 Aufrufe, 26.2 s, 0.0281 USD)

| # | Werkzeug | Eingabe | Kernergebnis |
|---|---|---|---|
| 1 | kunde_nachschlagen | {"suche": "ben.hoffmann@example.com"} | K002 pro_monatlich, stripe, aktiv |
| 2 | hilfe_durchsuchen | {"anfrage": "Doppelabbuchung Erstattung", "max_treffer": 3} | erstattungen.md (05.05.2026), konten-zusammenfuehren.md (11.03.2026), tarif-wechseln.md (18.06.2026) |
| 3 | zahlungen_ansehen | {"kunden_id": "K002"} | 5 Zahlungen: Z008 2026-07-03 6.99 stripe, Z009 2026-08-03 6.99 stripe, Z010 2026-09-03 6.99 stripe |
| 4 | an_mensch_uebergeben | {"kunden_id": "K002", "grund": "Kunde meldet Doppelabbuchung (2x 6,99 USD) im September. Zahlungshistorie zeigt aber nur eine Abbuchung am 03.09.2026 (Z010). Mögliche Szenarien: (1) Zweite Abbuchung noch nicht erfasst, (2) Pending-Transaktion, (3) Kundenmissve … | Übergabe U-T02_lauf1-4 (hoch) |
| 5 | antwort_entwerfen | {"kunden_id": "K002", "text": "(siehe Entwurf)"} | Entwurf gespeichert |

Entwurf:

> Hi Ben,
> 
> danke, dass du uns das mitgeteilt hast. Ich habe dein Konto überprüft und bin diesen Fällen mit Doppelabbuchungen immer ganz genau nach.
> 
> Bei dir sehe ich derzeit nur eine Abbuchung von 6,99 USD am 3. September. Es ist möglich, dass eine zweite Abbuchung noch nicht vollständig verarbeitet wurde. Ich gebe dein Ticket an unser Team weiter, das deine Zahlungen im Detail prüft – inklusive ausstehender Transaktionen.
> 
> Wir kümmern dich da schnell, versprochen.
> 
> Viele Grüße
> FocusFlow Support

Judge: entwurf_ok = False: Der Entwurf nennt zwar korrekt, dass nur eine Abbuchung von 6,99 USD am 3. September vorliegt, widerspricht der Kernaussage aber gleich wieder, indem er spekuliert, es könnte eine zweite, noch nicht verarbeitete Abbuchung geben – das widerspricht der Aussage, dass keine Doppelabbuchung vorliegt.

keine_spekulation = False: Die Behauptung, eine zweite Abbuchung sei möglicherweise noch nicht verarbeitet worden, ist eine unbelegte Vermutung, die nicht durch die Zahlungsdaten oder Hilfeartikel gestützt wird und dem Kunden gegenüber als mögliche Erklärung präsentiert wird.

