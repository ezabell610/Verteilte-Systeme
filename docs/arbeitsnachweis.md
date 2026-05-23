# Arbeitsnachweis

Projekt: Kochbuch – Rezeptverwaltung mit Kategorien und Einkaufsliste
Kurs: Verteilte Systeme, 4. Semester (DHBW)
Team: Selina, Isabell, Emily

## Aufgabenverteilung

| Person | Hauptbereich |
|--------|--------------|
| Isabell | Backend (FastAPI, Auth, REST-Endpoints, SQLAlchemy-Models) |
| Emily | Frontend (SvelteKit, UI/UX, API-Anbindung) |
| Selina | Datenbank-Design, Docker, Dokumentation, Seed-Daten |

## Detaillierte Beiträge

### Isabell (Backend)
- SQLAlchemy-Models für alle Tabellen (User, Recipe, Category, Ingredient, Rating, ShoppingListItem)
- Implementierung der Auth-Funktionen (Register, Login, my-profile)
- JWT-Token Erzeugung und Validierung
- Argon2 Password-Hashing
- CRUD-Endpoints für Rezepte (Create, Read, Update, Delete)
- Endpoint für Rezeptbewertungen
- Pydantic-Schemas für Request/Response

### Emily (Frontend)
- Login- und Registrierungsseite
- Hauptnavigation
- Startseite mit Rezeptliste
- Rezept-Detailseite
- API-Hilfsfunktionen in api.ts
- Komponenten und Routing-Struktur

### Selina (Datenbank, Docker, Dokumentation)
- Datenbank-Schema entworfen und dokumentiert
- ERD als Mermaid-Diagramm
- Architekturdiagramm der Gesamt-Anwendung
- README mit Projektbeschreibung, Setup-Anleitung, API-Übersicht
- `.gitignore` für Mac-System-Dateien angepasst
- Seed-Script (`backend/seed.py`) für automatische Beispieldaten:
  - 5 Kategorien
  - 2 Test-User
  - 6 Beispielrezepte mit Zutaten
  - 5 Beispielbewertungen
- Integration des Seed-Scripts in den Backend-Start
- Dokumentation in `docs/`-Ordner (architektur.md, db-schema.md)

## Nachvollziehbarkeit

Alle Beiträge sind über die Git-History des Repositories nachvollziehbar:
https://github.com/ezabell610/Verteilte-Systeme

Jede Person hat eigenständige Commits unter ihrem GitHub-Account:
- Isabell: `ezabell610`
- Emily: `emsily23`
- Selina: `Selina663`

Pull Requests wurden für strukturierte Reviews verwendet, wo möglich.

## Kommunikation und Zusammenarbeit

- Wöchentliche Abstimmungen zur Synchronisation
- GitHub Pull Requests für gegenseitiges Code-Review
- Klare Aufgabenverteilung mit definierten Schnittstellen (API als Vertrag zwischen Backend und Frontend)