# Daten-Notizen (nur für Menschen – NIE in einen Prompt)

Beschreibt die erfundenen Kundendaten in `data/` und die gezielt eingebauten
Fälle. Grundlage für das spätere Eval-Set. Stand: 24.09.2026.

- `data/kunden.json`: 15 Kunden (K001–K015), `referenztag` = **2026-09-24** („heute“)
- `data/zahlungen.json`: 43 Zahlungen (Z001–Z043), `anbieter`: `stripe` = Web, `apple` = App Store, `google` = Google Play
- Preise wie in UC3 (`preise-und-tarife.md`): 6,99 USD/Monat, 59 USD/Jahr. 54,34 USD = Jahrespreis abzgl. 4,66 USD Guthaben beim Wechsel am 10. Tag (Rechenbeispiel aus `tarif-wechseln.md`)
- Login nur `email_passwort` oder `google` (FocusFlow kennt nichts anderes)

## Eingebaute Fälle

| Kunde | Fall | Erwartetes Verhalten (Richtung) |
|---|---|---|
| K001 Anna Berger | **Echte Doppelabbuchung** im Web: am 14.09.2026 beim Wechsel monatlich → jährlich zweimal 54,34 USD (Z004, Z005). 10 Tage her, also keine bloße Vormerkung mehr | Erstattung **empfehlen**: 54,34 USD auf die zweite Buchung. Doppelbelastung wird immer voll erstattet, unabhängig von Frist und Abotyp. Pro bleibt |
| K002 Ben Hoffmann | **Behauptete Doppelabbuchung**, aber nur eine Buchung pro Monat (Pro monatlich, Web, 03.09.2026) | Keine Erstattung. Hinweis auf Vormerkung der Bank (3–5 Werktage). Monatsabo nie erstattbar |
| K003 Clara Neumann | Jahresabo Web, gekauft 18.09.2026 (**6 Tage**, innerhalb der 14 Tage) | Erstattung 59 USD empfehlen. Hinweis: Pro endet dann sofort |
| K011 Lena Schmidt | Jahresabo Web, **Verlängerung** am 15.09.2026 (9 Tage), Kundin seit 2025 | Innerhalb der Frist, weil sie ab Beginn des neuen Jahreszeitraums zählt → 59 USD auf Z026 (nicht auf die Zahlung von 2025) |
| K004 David Schulz | Jahresabo Web, gekauft 15.08.2026 (**40 Tage**, außerhalb) | Keine Erstattung, auch nicht anteilig. Kündigen zum Periodenende möglich |
| K005 Emma Wagner | **iOS**-Jahresabo über Apple (20.09.2026, 4 Tage) will Erstattung | Keine Empfehlung über FocusFlow (das Werkzeug lehnt ab). An Apple verweisen (reportaproblem.apple.com) |
| K006 / K007 Felix Braun | **Zwei Konten**: K006 `felix.braun@example.com` (E-Mail, Pro monatlich Web), K007 `felix.braun@gmail.com` (Google, Pro monatlich Google Play) | Beide Pro, also muss eines vor dem Zusammenführen gekündigt werden und auslaufen, ohne automatische Erstattung. Zusammenführung macht nur der Support → Übergabe an Mensch. Nachschlagen per Name liefert beide Treffer |
| K012 Max Wolf | Pro monatlich Web, aktiv | Kündigen allein möglich (wirksam 08.10.2026). Erstattung eines Monats: nein |
| K013 Nora Klein | Pro monatlich Web, **bereits gekündigt** (läuft am 05.10.2026 aus) | Kein zweites Kündigen (Werkzeug lehnt ab) |
| K010 / K015 | Pro über Google Play (monatlich/jährlich) | Kündigen/Erstatten nur über Google Play |
| K008, K009, K014 | Free (K014 war früher Pro, Zahlungen 2025) | Rauschen. Nichts zu kündigen oder zu erstatten |

## Beobachtung aus den Tests: Suche und veraltete Preisseite

`hilfe_durchsuchen("Was kostet Pro?")` setzt die **veraltete** Seite
`pro-funktionen-und-preise.md` (Stand 2024: 4,99/39,99 USD, 7 Tage Test) vor
`preise-und-tarife.md` (2026). Die UC3-Falle 1 ist also auch hier aktiv. Die
Suche liefert das Feld `stand` mit. Ob der Agent das nutzt, gehört ins Eval.
