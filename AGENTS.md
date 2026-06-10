## Projektkontext
- Dieses Repository ist ein Lernprojekt fuer Python, Streamlit und Codex.
- Ziel ist verstaendlicher, wartbarer Code, der Lernfortschritt sichtbar macht.
- Bevorzuge einfache Loesungen vor cleveren Abkuerzungen.

## Arbeitsweise
- Lies vorhandene Dateien zuerst und folge bestehenden Mustern.
- Aendere nur Dateien, die fuer die aktuelle Aufgabe noetig sind.
- Erklaere nicht offensichtliche Entscheidungen kurz im Code oder in der Antwort.
- Halte Commits, Patches und Antworten klein, nachvollziehbar und fokussiert.

## Entwicklungsprozess
Fuer jede neue Anforderung:
1. Anforderungen analysieren
2. Akzeptanzkriterien formulieren
3. Zielarchitektur skizzieren
4. Implementierung in kleinen Schritten
5. Tests und Checks durchfuehren
6. Manuelle Testschritte dokumentieren
7. Refactoring nur bei erkennbarem Nutzen
Nicht direkt mit der Implementierung beginnen, wenn Anforderungen oder Akzeptanzkriterien unklar sind.

## Code Style
- Schreibe idiomatisches Python mit klaren Namen und kleinen Funktionen.
- Nutze Type Hints dort, wo sie Verstaendnis oder Sicherheit verbessern.
- Vermeide globale Seiteneffekte ausserhalb klarer App-Initialisierung.
- Bevorzuge Standardbibliothek und vorhandene Dependencies.
- Kommentare sollen Warum erklaeren, nicht offensichtliches Was.

## Streamlit Styleguide
- Baue Seiten von oben nach unten: Import, Konstanten, Hilfsfunktionen, UI.
- Nutze `st.session_state` bewusst und initialisiere Keys explizit.
- Halte Widgets beschriftet, eindeutig und fuer Lernende verstaendlich.
- Trenne Datenlogik von UI-Code, wenn Funktionen wachsen.
- Verwende `st.cache_data` oder `st.cache_resource` nur bei klarem Nutzen.

## Secure Coding
- Keine Secrets, Tokens oder lokalen Pfade in Code oder Beispieldaten committen.
- Validere und bereinige Benutzereingaben, bevor sie verarbeitet werden.
- Oeffne Dateien nur aus erwarteten Pfaden und mit minimal noetigen Rechten.
- Verwende keine unsicheren Ausfuehrungen wie `eval`, `exec` oder Shell-Strings.
- Behandle externe Daten als unvertrauenswuerdig.

## Test- und Qualitaetsanforderungen
- Fuehre passende Tests oder Checks aus, wenn Codeverhalten geaendert wurde.
- Ergaenze Tests fuer neue Logik, Fehlerfaelle und sicherheitsrelevante Pfade.
- Pruefe Streamlit-Aenderungen mindestens manuell im Browser, wenn moeglich.
- Halte Linting-/Formatierungsfehler aus geaenderten Dateien heraus.
- Dokumentiere nicht ausgefuehrte Checks kurz mit Grund.
