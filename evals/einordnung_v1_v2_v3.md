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
