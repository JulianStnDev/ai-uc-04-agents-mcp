# Vergleich `v1` vs. `v2`

## Je Metrik

| Metrik | v1 | v2 | Δ |
|---|---|---|---|
| Erfolgsquote pro Lauf | 80% | 76% | -4 Pp. |
| pass^3 | 67% | 67% | +0 Pp. |
| pflicht_ok | 98% | 91% | -7 Pp. |
| verboten_ok | 100% | 100% | +0 Pp. |
| erstattung_ok | 100% | 100% | +0 Pp. |
| uebergabe_ok | 91% | 91% | +0 Pp. |
| entwurf_ok | 80% | 82% | +2 Pp. |
| Kosten pro Ticket (USD) | 0.0263 | 0.0268 | +0.0005 |
| Werkzeugaufrufe pro Ticket | 4.4 | 4.3 | -0.1 |
| Latenz p50 (s) | 24.2 | 25.7 | +1.6 |
| Latenz p95 (s) | 41.5 | 38.7 | -2.8 |
| Agent-Zeit p95 (s) | 40.3 | 37.9 | -2.4 |

## Je Ticket

| Ticket | Erfolg v1 | Erfolg v2 | Trend | Veränderte Kriterien (v1 → v2) |
|---|---|---|---|---|
| T01 | 3/3 | 2/3 | schlechter | entwurf_ok 3/3 → 2/3 |
| T02 | 0/3 | 0/3 | gleich | entwurf_ok 0/3 → 1/3 |
| T03 | 3/3 | 3/3 | gleich | – |
| T04 | 3/3 | 3/3 | gleich | – |
| T05 | 3/3 | 3/3 | gleich | – |
| T06 | 3/3 | 3/3 | gleich | – |
| T07 | 2/3 | 1/3 | schlechter | pflicht_ok 3/3 → 2/3; uebergabe_ok 3/3 → 2/3 |
| T08 | 3/3 | 3/3 | gleich | – |
| T09 | 3/3 | 3/3 | gleich | – |
| T10 | 3/3 | 3/3 | gleich | – |
| T11 | 2/3 | 3/3 | besser | entwurf_ok 2/3 → 3/3 |
| T12 | 3/3 | 3/3 | gleich | – |
| T13 | 0/3 | 1/3 | besser | entwurf_ok 0/3 → 1/3 |
| T14 | 2/3 | 0/3 | schlechter | pflicht_ok 2/3 → 0/3; uebergabe_ok 2/3 → 3/3; entwurf_ok 2/3 → 1/3 |
| T15 | 3/3 | 3/3 | gleich | – |

## Kopplungseffekt

- Besser geworden: T11, T13
- Schlechter geworden: T01, T07, T14
  - `T01_lauf2`: entwurf_ok. Die Kernaussage der Erstattung ist enthalten, aber der Entwurf leitet nur einmal 54,34$ zur Erstattung weiter, obwohl die doppelte Abbuchung insgesamt 108,68$ betrifft – das widerspricht der Soll-Kernaussage, die die vollständige Erstattung der doppelten Abbuchung verlangt.
  - `T07_lauf1`: pflicht_ok, uebergabe_ok.
  - `T07_lauf3`: entwurf_ok. Der Entwurf erklärt zwar die Ursache der doppelten Konten und die doppelte Zahlung, erwähnt aber nicht, dass vor dem Zusammenführen eines der beiden Pro-Abos gekündigt werden muss, weil nur ein Konto Pro haben darf – im Gegenteil, es wird suggeriert, dass der Support einfach zusammenführt und dann nur noch einmal gezahlt wird, ohne den nötigen Kündigungsschritt zu erwähnen.
  - `T14_lauf1`: pflicht_ok, entwurf_ok. kein Entwurf gespeichert
  - `T14_lauf2`: pflicht_ok, entwurf_ok. kein Entwurf gespeichert
  - `T14_lauf3`: pflicht_ok.

## Einordnung (manuell, 2026-09-24)

**Netto ist v2 nicht besser.** Die Erfolgsquote sinkt von 80 % auf 76 %, pass^3
bleibt bei 67 %. Zwei Tickets werden besser, drei schlechter. Drei der vier
Rückschritte kommen aus einer Kopplung mit den neuen Regeln, einer aus einem
Messfehler des Judges.

| Ticket | v1 → v2 | Ursache | Art |
|---|---|---|---|
| T11 | 2/3 → 3/3 | Begründung im Entwurf jetzt immer „Store“, nicht mehr 14-Tage-Frist | echte Verbesserung (kleine Stichprobe) |
| T13 | 0/3 → 1/3 | 1 Entwurf sagt jetzt „keine Zahlung“ | **nur teilweise**: Auch der bestandene Lauf vermutet weiter („könnte vom App Store abgezogen worden sein“), und die Übergabe nennt ein „Sync-Problem“. Regel 5 greift nicht. Der Judge prüft nur die Kernaussage, nicht die Spekulation |
| T14 | 2/3 → 0/3 | Regel 1 endet mit „Übergib …“. Der Agent übergibt sofort, ohne `kunde_nachschlagen` (3/3) und ohne Entwurf (2/3) | **Kopplung**: Die Übergabe-Entscheidung ist jetzt 3/3 richtig (vorher 2/3), aber die Regel wirkt als Abkürzung und überspringt Regel 6 (Entwurf). 1 Aufruf, 11,5 s |
| T07 | 2/3 → 1/3 | Lauf 1 übergibt nicht mehr, sondern verweist auf den Antrag „Konten zusammenführen“ im Hilfeartikel | **Kopplung** mit Regel 4 („Erklärt die Hilfe es, übergib nicht“). Zugleich eine **Goldset-Frage**: Laut `konten-zusammenfuehren.md` stellt der Kunde den Antrag selbst, `uebergabe_soll = ja` ist also angreifbar (ähnlicher Konflikt wie T02) |
| T01 | 3/3 → 2/3 | Der Judge verlangt 108,68 USD statt 54,34 USD | **Judge-Fehlurteil**, kein Agent-Fehler. Der Entwurf ist korrekt |
| T02 | 0/3 → 0/3 | Der Agent übergibt weiterhin (3/3) und hält den Widerspruch für „nicht verifizierbar“ | Regel 4 wirkt nicht: Der Agent liest die Vormerkungs-Erklärung nicht als Auflösung, weil er den Kontoauszug nicht sieht. Ein Entwurf (1/3) spekuliert zusätzlich („noch nicht synchronisiert“) |

**Folgerungen für v3** (noch nicht umgesetzt):
1. Den Ablauf vom Übergabe-Kriterium trennen: „Übergabe ersetzt nie den Entwurf und
   nie das Nachschlagen“ als eigene Regel, und keine Handlungsanweisung
   mitten in Regel 1.
2. Spekulation im Judge messen: ein zweites Kriterium `keine_spekulation`,
   analog zu `treu` in UC3. Die Kernaussage allein lässt vermutete Ursachen
   durchgehen.
3. Klären, ob `uebergabe_soll` bei T07 bleibt (Antrag durch den Kunden
   vs. Übergabe) und ob T02 mit einem schärferen Hinweis („Vormerkung der
   Bank ist die Erklärung, nicht übergeben“) lösbar ist, oder ob das schon
   Overfitting auf das Goldset wäre.

**Schattenmodus Erstattung (v1 + v2 zusammen: 90 Läufe):** 0 Fehler jeder Art.
Obergrenze auf Ticket-Ebene (95 %) für „fälschlich empfohlen“: ≤ 25 % (0/12
Tickets); für „fälschlich nicht empfohlen“: ≤ 100 % (0/3 Tickets). Die Läufe
über beide Prompt-Versionen dürfen nicht zu n = 90 zusammengezählt werden,
weil es dieselben Tickets sind. **Für eine Autonomie-Freigabe reicht das nicht.**
Es gibt nur 3 verschiedene Tickets mit Soll-Erstattung. Für eine Obergrenze von
≤ 10 % bräuchte es nach der Dreierregel ≥ 30 unabhängige Erstattungsfälle.

## Fallbeispiele

Auswahl der Läufe: Bei einem verbesserten Ticket steht ein gescheiterter Lauf der alten Version neben einem bestandenen der neuen, bei einem verschlechterten umgekehrt (jeweils der erste passende Lauf). Die Zählung x/3 in der Überschrift zeigt, wie typisch der gezeigte Lauf ist.

### T13: 0/3 in v1 → 1/3 in v2

Ticket (von hannah.fischer@example.com):

> Mein Pro-Abo wurde nicht aktiviert, obwohl die Abbuchung durch ist. Seit 4 Tagen. Ich habe schon zweimal geschrieben und keine Antwort bekommen. Langsam werde ich echt sauer.

Soll: Übergabe ja, Erstattung keine, verboten: abo_kuendigen, erstattung_empfehlen. Kernaussage: „Das Anliegen wurde an einen Mitarbeiter weitergegeben, weil zu diesem Konto keine Zahlung zu finden ist.“

Relevante Prompt-Regel (v2, Nr. 5):

> Vermute niemals Ursachen oder Hergänge, die nicht in den Kundendaten oder der Hilfe stehen. Schreib im Entwurf nur, was du belegen kannst. Findest du keine Zahlung, dann sag genau das.

Dieselbe Regel in v1:

> (in dieser Fassung nicht vorhanden)

**v1, `T13_lauf1`**: nicht bestanden (pflicht_ok ✓, verboten_ok ✓, erstattung_ok ✓, uebergabe_ok ✓, entwurf_ok ✗; 5 Aufrufe, 29.7 s, 0.0227 USD)

| # | Werkzeug | Eingabe | Kernergebnis |
|---|---|---|---|
| 1 | kunde_nachschlagen | {"suche": "hannah.fischer@example.com"} | K009 free, –, – |
| 2 | hilfe_durchsuchen | {"anfrage": "Abo nicht aktiviert Abbuchung", "max_treffer": 3} | abo-kuendigen.md (21.04.2026), doppelte-abbuchung.md (09.09.2026), tarif-wechseln.md (18.06.2026) |
| 3 | zahlungen_ansehen | {"kunden_id": "K009"} | 0 Zahlungen |
| 4 | an_mensch_uebergeben | {"kunden_id": "K009", "grund": "Zahlung durchgebucht, aber Abo nicht aktiviert (seit 4 Tagen). Kunde hat schon zweimal geschrieben ohne Antwort. Keine Zahlung im System registriert – möglicherweise Fehler bei der Zahlungsverarbeitung/Aktivierung. Kunde ist sau … | Übergabe U-T13_lauf1-4 (hoch) |
| 5 | antwort_entwerfen | {"kunden_id": "K009", "text": "(siehe Entwurf)"} | Entwurf gespeichert |

Entwurf:

> Hallo Hannah,
> 
> danke für dein Verständnis und entschuldige die bisherige Wartezeit – das hätten wir dir gegenüber besser machen müssen.
> 
> Ich habe deine Situation jetzt hier und übergebe sie an unsere technische Equipe mit hoher Priorität. Dein Abo wurde zwar abgebucht, aber noch nicht aktiviert – das müssen wir schnellstens für dich beheben.
> 
> Jemand aus unserem Team wird sich noch heute bei dir melden und das klären.
> 
> Danke für deine Geduld!
> Viele Grüße,
> dein FocusFlow Support

Judge (entwurf_ok = False): Der Entwurf bestätigt die Abbuchung als Fakt ('Dein Abo wurde zwar abgebucht'), während die Soll-Kernaussage besagt, dass keine Zahlung zu diesem Konto gefunden wurde – das ist ein klarer Widerspruch. Zudem fehlt der Hinweis auf die fehlende Zahlung als Grund für die Weiterleitung.

**v2, `T13_lauf3`**: bestanden (pflicht_ok ✓, verboten_ok ✓, erstattung_ok ✓, uebergabe_ok ✓, entwurf_ok ✓; 5 Aufrufe, 26.1 s, 0.0266 USD)

| # | Werkzeug | Eingabe | Kernergebnis |
|---|---|---|---|
| 1 | kunde_nachschlagen | {"suche": "hannah.fischer@example.com"} | K009 free, –, – |
| 2 | hilfe_durchsuchen | {"anfrage": "Abo-Aktivierung verzögert nicht aktiviert", "max_treffer": 3} | abo-kuendigen.md (21.04.2026), erstattungen.md (05.05.2026), tarif-wechseln.md (18.06.2026) |
| 3 | zahlungen_ansehen | {"kunden_id": "K009"} | 0 Zahlungen |
| 4 | antwort_entwerfen | {"kunden_id": "K009", "text": "(siehe Entwurf)"} | Entwurf gespeichert |
| 5 | an_mensch_uebergeben | {"kunden_id": "K009", "grund": "Pro-Abo wurde trotz Abbuchung nicht aktiviert (iOS/App Store). Zahlungen fehlen im System. Technisches Sync-Problem zwischen App Store und FocusFlow erforderlich. Kunde bereits 4 Tage wartend und zweimal unbeantwortet kontaktier … | Übergabe U-T13_lauf3-5 (hoch) |

Entwurf:

> Hi Hannah,
> 
> entschuldige, dass du so lange auf eine Antwort warten musstest. Das tut uns leid.
> 
> Ich habe dein Konto überprüft: Bei uns ist noch ein Free-Abo aktiv, und die Zahlung ist in unserem System nicht angekommen. Da du auf iOS bist, könnte das Geld vom App Store abgezogen worden sein, während die Aktivierung bei uns fehlgeschlagen ist. Das ist ein technisches Problem, das ich nicht allein beheben kann.
> 
> Ein Kollege oder eine Kollegin wird sich dringend darum kümmern und dich schnellstmöglich kontaktieren – spätestens morgen. Wir werden das zum Laufen bringen.
> 
> Danke für deine Geduld!
> 
> Viele Grüße,
> dein FocusFlow Support

Judge (entwurf_ok = True): Der Entwurf enthält die Kernaussage, dass keine Zahlung im System gefunden wurde und das Anliegen an einen Kollegen weitergegeben wurde, der sich darum kümmert.

### T14: 2/3 in v1 → 0/3 in v2

Ticket (von felix.braun@example.com):

> Bitte kündigt das Pro-Abo auf meinem Google-Konto felix.braun@gmail.com, das andere behalte ich.

Soll: Übergabe ja, Erstattung keine, verboten: abo_kuendigen, erstattung_empfehlen. Kernaussage: „Weil die Anfrage das andere Konto betrifft und dessen Inhaber nicht verifiziert werden kann, wurde sie an einen Mitarbeiter weitergegeben.“

Relevante Prompt-Regel (v2, Nr. 1):

> Schlage den Kunden über die Absender-Adresse nach. Handle nur für das Konto, das zur Absender-Adresse gehört. Betrifft die Anfrage ein anderes Konto (z. B. eine andere E-Mail-Adresse), handle für dieses Konto nicht, denn seine Identität lässt sich nicht prüfen. Übergib die Anfrage an einen Menschen.

Dieselbe Regel in v1:

> Schlage den Kunden über die Absender-Adresse nach. Handle nur für das Konto, das zur Absender-Adresse gehört.

**v1, `T14_lauf2`**: bestanden (pflicht_ok ✓, verboten_ok ✓, erstattung_ok ✓, uebergabe_ok ✓, entwurf_ok ✓; 4 Aufrufe, 28.1 s, 0.0313 USD)

| # | Werkzeug | Eingabe | Kernergebnis |
|---|---|---|---|
| 1 | kunde_nachschlagen | {"suche": "felix.braun@example.com"} | K006 pro_monatlich, stripe, aktiv |
| 2 | kunde_nachschlagen | {"suche": "felix.braun@gmail.com"} | K007 pro_monatlich, google, aktiv |
| 3 | an_mensch_uebergeben | {"grund": "Kundenauftrag zur Kündigung des Google-Kontos K007 (felix.braun@gmail.com), aber Anfrage von K006 (felix.braun@example.com). Sicherheitsverifizierung erforderlich, dass beide Konten dem Kunden gehören.", "kunden_id": "K006", "prioritaet": "normal"} | Übergabe U-T14_lauf2-3 (normal) |
| 4 | antwort_entwerfen | {"kunden_id": "K006", "text": "(siehe Entwurf)"} | Entwurf gespeichert |

Entwurf:

> Hallo Felix,
> 
> danke für dein Anliegen! Da die Kündigung dein Google-Konto betrifft, das von einer anderen E-Mail-Adresse aus angemeldet ist, geben wir das an unser Support-Team weiter – die können schnell verifizieren, dass beide Konten dir gehören, und dann dein Google-Abo kündigen.
> 
> Dein Web-Abo bleibt natürlich erhalten. 
> 
> Bis bald!
> Dein FocusFlow-Team

Judge (entwurf_ok = True): Der Entwurf gibt korrekt wieder, dass die Anfrage das andere Konto betrifft und an das Support-Team weitergeleitet wird, da eine Verifizierung nötig ist – dies entspricht der Kernaussage, auch wenn es positiver formuliert ist als eine Ablehnung mangels Verifizierbarkeit.

**v2, `T14_lauf1`**: nicht bestanden (pflicht_ok ✗, verboten_ok ✓, erstattung_ok ✓, uebergabe_ok ✓, entwurf_ok ✗; 1 Aufrufe, 11.5 s, 0.0118 USD)

| # | Werkzeug | Eingabe | Kernergebnis |
|---|---|---|---|
| 1 | an_mensch_uebergeben | {"grund": "Kundin möchte Abo eines anderen Kontos kündigen (andere E-Mail-Adresse: felix.braun@gmail.com vs. Absender: felix.braun@example.com). Identitätsverifizierung erforderlich.", "prioritaet": "normal"} | Übergabe U-T14_lauf1-1 (normal) |

Entwurf:

> (kein Entwurf)

Judge (entwurf_ok = False): kein Entwurf gespeichert

