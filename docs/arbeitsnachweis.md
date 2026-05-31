# Arbeitsnachweis

Projekt: Kochbuch – Rezeptverwaltung mit Kategorien und Einkaufsliste
Kurs: Verteilte Systeme, 4. Semester (DHBW)
Team: Selina, Isabell, Emily
Abgabe: 31.05.2026

## Aufgabenverteilung

| Person | Hauptbereich |
|--------|--------------|
| Isabell | Backend (FastAPI, Auth, REST-Endpoints, SQLAlchemy-Models) |
| Emily | Frontend (SvelteKit, UI/UX, API-Anbindung) |
| Selina | Datenbank-Design, Docker, Dokumentation, Seed-Daten |

## Detaillierte Beiträge

### Isabell – Backend
- SQLAlchemy-Models für alle Tabellen (User, Recipe, Category, Ingredient, Rating, ShoppingListItem) inkl. Cascade-Delete-Logik
- Auth-Implementierung: Register, Login, my-profile mit JWT-Token
- Argon2 Password-Hashing mit Timing-Schutz (DUMMY_HASH)
- CRUD-Endpoints für Rezepte (Create, Read, Update, Delete) mit Berechtigungsprüfung
- Endpoints für Bewertungen (mit Update-Logik für bereits abgegebene Bewertungen)
- Endpoints für Einkaufsliste (hinzufügen, abhaken, entfernen)
- Endpoint für Kategorien
- Pydantic-Schemas für Request/Response-Validierung
- CORS-Konfiguration für Frontend-Anbindung
- Suchfunktion und Kategorie-Filter in GET /recipes
- Bug-Fixes: Backend-Anpassungen für Rezept-Erstellung, private Rezepte, Bearbeitung fremder Rezepte

### Emily – Frontend
- Login- und Registrierungsseite mit Formular-Validierung
- Hauptnavigation mit Login-Status
- Startseite mit Rezeptliste, Suche und Kategorie-Filter
- Rezept-Detailseite mit Zutaten, Schritten und Bewertungen
- Seite "Neues Rezept erstellen" mit dynamischer Zutaten-Eingabe
- Seite "Rezept bearbeiten"
- Seite "Meine Rezepte" für eingeloggte User
- Einkaufslisten-Seite mit Abhaken/Entfernen
- Sternebewertung-Komponente (StarRating)
- API-Hilfsfunktionen in api.ts mit JWT-Handling
- Kategoriennamen-Anzeige im Frontend (statt IDs)
- Anpassung des Seed-Scripts an die finalen Kategorien
- Diverse UX-Verbesserungen und Bug-Fixes

### Selina – Datenbank, Docker, Dokumentation
- Datenbank-Schema entworfen und dokumentiert
- ERD als Mermaid-Diagramm in docs/db-schema.md
- Architekturdiagramm der Gesamt-Anwendung in docs/architektur.md
- README mit Projektbeschreibung, Setup-Anleitung, API-Übersicht, Projektstruktur
- .gitignore für Mac-System-Dateien angepasst (.DS_Store ignoriert)
- Seed-Script (backend/seed.py) für automatische Beispieldaten beim ersten Start:
  - 5 Kategorien mit Beschreibungen
  - 2 Test-User mit gehashten Passwörtern
  - 6 Beispielrezepte mit Zutaten und Zubereitungsschritten
  - 5 Beispielbewertungen
  - Idempotent: läuft nur, wenn DB leer ist
- Integration des Seed-Scripts in den Backend-Start (main.py)
- Docker-Healthcheck-Fix: Authentifizierter mysqladmin-ping mit start_period gegen Race-Condition beim Erststart
- End-to-End Testprotokoll mit allen getesteten Funktionen
- Aktualisierung der Doku an die tatsächliche Implementierung (Categories statt Tags)
- Foliengliederung für die Abschluss-Präsentation

## Nachvollziehbarkeit

Alle Beiträge sind über die Git-History des Repositories nachvollziehbar:
https://github.com/ezabell610/Verteilte-Systeme

Jede Person hat eigenständige Commits unter ihrem GitHub-Account:
- Isabell: ezabell610
- Emily: emsily23
- Selina: Selina663

Pull Requests wurden für strukturierte Reviews verwendet, sichtbare PRs:
- #1, #2 (Selina): README, .gitignore
- #3, #7, #8, #9, #10, #12, #13, #14 (Emily): Frontend-Seiten und Backend-Fixes
- #4 (Selina): Schema und Architektur Doku
- #5 (Selina): Seed-Script
- #6 (Selina): Arbeitsnachweis
- #11 (Selina): Docker-Healthcheck-Fix

## Kommunikation und Zusammenarbeit

- Regelmäßige Abstimmungen zur Synchronisation
- GitHub Pull Requests für gegenseitiges Code-Review
- Klare Aufgabenverteilung mit definierten Schnittstellen (API als Vertrag zwischen Backend und Frontend)
- Wechselseitige Bug-Fixes: Emily hat Backend-Bugs gefixt, wo sie sie beim Frontend-Anbinden bemerkt hat
- Gemeinsame Anpassung des Datenbank-Schemas (Kategorien) zwischen Backend und Seed-Script