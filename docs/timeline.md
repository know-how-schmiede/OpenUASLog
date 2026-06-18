# OpenUASLog Änderungshistorie

Diese Datei dokumentiert alle Änderungen mit Versionsnummer und Datum.

Die Versionsnummer wird ausschließlich auf ausdrückliche Anweisung geändert. Änderungen ohne Versionsanhebung werden unter der aktuell gesetzten Version ergänzt.

Die zentrale Versionsnummer befindet sich in [`version.py`](../version.py).

---

## Version 0.1.0 – 18. Juni 2026

### Dokumentation

- Eigenständige Roadmap in `docs/roadmap.md` erstellt.
- Architekturinformationen in `docs/architecture.md` ausgelagert.
- Projektbeschreibung in `docs/project-description.md` ausgelagert.
- `docs/README.md` als zentralen Dokumentationsindex eingerichtet.
- Zentrale Versionsinformation in `version.py` angelegt.
- Änderungshistorie in `docs/timeline.md` eingeführt.
- Root-README um Funktionsumfang, Schnellstart, Entwicklung und Konfiguration ergänzt.
- Architekturdokumentation an die implementierte MVP-Struktur angepasst.

### Backend

- FastAPI-Anwendung mit CORS, Health-Check und OpenAPI-Dokumentation eingerichtet.
- SQLAlchemy-Datenbankzugriff und automatische SQLite-Initialisierung umgesetzt.
- Initiales Administratorkonto über Umgebungsvariablen konfigurierbar gemacht.
- Datenmodelle für Benutzer, Drohnen-Typen, eigene Drohnen und Flüge implementiert.
- Anmeldung mit signierten Bearer-Token und PBKDF2-Passwort-Hashing umgesetzt.
- Rollen- und Eigentümerprüfungen für Admins und Piloten ergänzt.
- CRUD-APIs für Benutzer, Drohnen-Typen, Drohnen und Flüge erstellt.
- Template-zu-Instanz-Prinzip mit individuellen Überschreibungen und Quellenkennzeichnung umgesetzt.
- Automatische Berechnung der Flugdauer ergänzt.
- Rollenabhängige Dashboard-Auswertung implementiert.
- CSV-Export für Flüge ergänzt.
- Integrationstests für Health-Check, vollständigen MVP-Workflow sowie Rollen- und Eigentümerrechte erstellt.

### Frontend

- React-, Vite-, TypeScript- und MUI-Projekt eingerichtet.
- Anmeldeseite und persistente Browser-Sitzung umgesetzt.
- Responsives Dashboard-Layout mit rollenabhängiger Navigation erstellt.
- Dashboard mit zentralen Flug- und Drohnenkennzahlen ergänzt.
- Tabellen und Erfassungsdialoge für Drohnen-Typen, eigene Drohnen und Flüge umgesetzt.
- CSV-Download für Flüge in die Oberfläche integriert.

### Betrieb

- Dockerfiles für Backend und Frontend ergänzt.
- Nginx-Konfiguration für Single-Page-App und API-Proxy erstellt.
- Docker-Compose-Setup mit persistentem SQLite-Volume angelegt.
- Beispielkonfiguration in `.env.example` ergänzt.
- Beispielvorlagen für DJI Mavic 3 Classic und DJI Mini 4 Pro hinzugefügt.
