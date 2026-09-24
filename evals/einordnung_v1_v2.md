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
