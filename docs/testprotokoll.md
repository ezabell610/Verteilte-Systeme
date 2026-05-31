# Testprotokoll

End-to-End Testprotokoll der Kochbuch-App.
Durchgeführt am: 31.05.2026 (vor Abgabe)
Getestet von: Selina

## Setup-Test

| # | Test | Erwartung | Ergebnis | Status |
|---|------|-----------|----------|--------|
| 1 | `docker compose down -v` && `docker compose up` | Alle 3 Services starten ohne manuelle Eingriffe | MySQL, Backend und Frontend fahren sauber hoch, Backend wartet auf DB dank Healthcheck | ✅ |
| 2 | Seed-Script läuft automatisch | 5 Kategorien, 2 User, 6 Rezepte, 5 Bewertungen werden angelegt | Alle Daten erfolgreich angelegt | ✅ |
| 3 | Frontend erreichbar | http://localhost:5173 zeigt Startseite | Startseite mit Rezeptliste lädt | ✅ |
| 4 | Backend API erreichbar | http://localhost:8000/docs zeigt Swagger UI | Swagger UI lädt mit allen Endpoints | ✅ |

## Authentifizierung

| # | Test | Erwartung | Ergebnis | Status |
|---|------|-----------|----------|--------|
| 5 | Registrierung via Swagger (POST /auth/register) | Code 201, User wird angelegt | Code 201, User mit ID zurückgegeben | ✅ |
| 6 | Duplikat-Registrierung mit gleichem Username | Code 400 | Code 400, Fehlermeldung "existiert bereits" | ✅ |
| 7 | Login via Swagger (POST /token) | Code 200, JWT-Token zurück | Code 200 mit access_token und token_type "bearer" | ✅ |
| 8 | Login mit falschem Passwort | Code 401 | Code 401, "Ungültige Anmeldedaten" | ✅ |
| 9 | Login im Frontend | Erfolgreiche Anmeldung, Weiterleitung | Login funktioniert, User ist eingeloggt | ✅ |
| 10 | Geschützter Endpoint /my-profile mit JWT | Code 200, User-Daten zurück | User-Daten korrekt zurückgegeben | ✅ |
| 11 | Geschützter Endpoint ohne JWT | Code 401 | Code 401 wie erwartet | ✅ |

## Rezept-Funktionen

| # | Test | Erwartung | Ergebnis | Status |
|---|------|-----------|----------|--------|
| 12 | Öffentliche Rezeptliste laden (GET /recipes) | 6 Seed-Rezepte sichtbar, ohne Login | Liste mit 6 Rezepten zurück | ✅ |
| 13 | Einzelnes Rezept ansehen (GET /recipes/{id}) | Details mit Zutaten und Schritten | Komplette Rezeptdaten | ✅ |
| 14 | Neues Rezept erstellen (eingeloggt) | Code 201, Rezept gespeichert | Rezept wird in DB angelegt und ist in Liste sichtbar | ✅ |
| 15 | Rezept erstellen ohne Login | Code 401 | Code 401 wie erwartet | ✅ |
| 16 | Eigenes Rezept bearbeiten | Änderungen werden gespeichert | Update erfolgreich | ✅ |
| 17 | Fremdes Rezept bearbeiten | Code 404/403 | Wird blockiert | ✅ |
| 18 | Eigenes Rezept löschen | Code 200, Rezept verschwindet | Rezept ist gelöscht, auch zugehörige Zutaten weg (Cascade) | ✅ |

## Kategorien & Filter

| # | Test | Erwartung | Ergebnis | Status |
|---|------|-----------|----------|--------|
| 19 | Kategorien laden (GET /categories) | 5 Kategorien zurück | Alle 5 Kategorien (Vegan, Italienisch, Dessert, Asiatisch, Schnelle Küche) | ✅ |
| 20 | Filter nach Kategorie | Nur Rezepte dieser Kategorie | Filter funktioniert wie erwartet | ✅ |
| 21 | Suche nach Rezepttitel | Nur passende Rezepte | Suche funktioniert (z.B. "Pasta" → Spaghetti Carbonara) | ✅ |

## Bewertungen

| # | Test | Erwartung | Ergebnis | Status |
|---|------|-----------|----------|--------|
| 22 | Rezept mit Sternen bewerten | Bewertung wird gespeichert | Sterne werden in DB gespeichert, sichtbar auf Karte | ✅ |
| 23 | Eigene Bewertung aktualisieren | Stars ändern sich, kein doppelter Eintrag | Update funktioniert | ✅ |

## Einkaufsliste

| # | Test | Erwartung | Ergebnis | Status |
|---|------|-----------|----------|--------|
| 24 | Zutat zur Einkaufsliste hinzufügen | Eintrag erscheint in Einkaufsliste | Funktioniert | ✅ |
| 25 | Eintrag als "gekauft" markieren | Checkbox umgeschaltet | Toggle funktioniert | ✅ |
| 26 | Eintrag aus Einkaufsliste entfernen | Eintrag verschwindet | Funktioniert | ✅ |

## Robustheit

| # | Test | Erwartung | Ergebnis | Status |
|---|------|-----------|----------|--------|
| 27 | App-Neustart ohne Volume-Löschung | Daten bleiben erhalten | DB-Volume persistiert, Daten sind nach `docker compose restart` da | ✅ |
| 28 | Frischer Start mit `docker compose down -v` | Seed-Script läuft, App neu befüllt | Idempotent: Daten sind wieder da | ✅ |
| 29 | Backend wartet auf DB (Healthcheck) | Kein "Connection refused" beim Erststart | Backend startet erst nach gesundem MySQL | ✅ |

## Bekannte Einschränkungen

- Frontend zeigt aktuell beim ersten Laden Loading-States (keine Skeletons), das ist UX-mäßig okay
- Sterne-Komponente löst beim Linting kleinere Accessibility-Warnungen aus (nicht funktional, nur Empfehlungen)

## Zusammenfassung

29 von 29 Tests bestanden. Die App ist funktional vollständig und 
startet auf einem frischen System ohne manuelle Eingriffe via 
`docker compose up`.