# OpenUASLog

OpenUASLog ist eine selbst hostbare Open-Source-Webanwendung zur Dokumentation von UAS- und Drohnenflügen. Administratoren verwalten allgemeine Drohnen-Typen als Vorlagen. Piloten erstellen daraus konkrete Drohnen, überschreiben bei Bedarf einzelne technische Werte und dokumentieren ihre Flüge.

Aktuelle Version: **0.1.0**

## Funktionsumfang

- FastAPI-Backend mit OpenAPI-Dokumentation
- SQLite-Datenbank über SQLAlchemy
- Anmeldung mit den Rollen Admin und Pilot
- administrative Benutzerverwaltung über die API
- Verwaltung zentraler Drohnen-Typen
- eigene Drohnen mit dauerhafter Vorlagenverknüpfung
- individuelle Überschreibungen technischer Vorlagenwerte
- Flugbuch mit automatischer Berechnung der Flugdauer
- rollenabhängiges Dashboard
- CSV-Export für Flüge
- React-, TypeScript- und MUI-Frontend
- Docker-Compose-Setup

Akkuverwaltung und Wartungslog sind für Version 0.2 vorgesehen.

## Schnellstart mit Docker

Voraussetzungen:

- Docker
- Docker Compose

Eine lokale Konfigurationsdatei anlegen:

```powershell
Copy-Item .env.example .env
```

Vor dem ersten Start müssen in `.env` mindestens ein sicheres Secret und ein neues Admin-Passwort gesetzt werden.

Anwendung starten:

```powershell
docker compose up --build
```

Danach sind folgende Dienste erreichbar:

- Weboberfläche: <http://localhost:8080>
- API-Dokumentation: <http://localhost:8080/api/docs>
- Health-Check: <http://localhost:8080/health>

Beim ersten Backend-Start wird das konfigurierte Administratorkonto angelegt.

## Lokale Entwicklung

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m uvicorn app.main:app --reload
```

Die API läuft standardmäßig unter <http://localhost:8000>. Die interaktive Dokumentation befindet sich unter <http://localhost:8000/docs>.

Tests:

```powershell
cd backend
python -m pytest -q
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Das Frontend läuft unter <http://localhost:5173> und leitet API-Anfragen lokal an Port 8000 weiter.

## Konfiguration

Alle Backend-Variablen beginnen mit `OPENUASLOG_`.

| Variable | Bedeutung |
| --- | --- |
| `OPENUASLOG_DATABASE_URL` | SQLAlchemy-Datenbank-URL |
| `OPENUASLOG_SECRET_KEY` | Signaturschlüssel für Anmeldetoken |
| `OPENUASLOG_INITIAL_ADMIN_USERNAME` | Benutzername des initialen Administrators |
| `OPENUASLOG_INITIAL_ADMIN_EMAIL` | E-Mail des initialen Administrators |
| `OPENUASLOG_INITIAL_ADMIN_PASSWORD` | Passwort des initialen Administrators |
| `OPENUASLOG_CORS_ORIGINS` | Kommaseparierte erlaubte Frontend-Ursprünge |

Die Standardzugangsdaten `admin` / `admin` dienen ausschließlich der lokalen Entwicklung.

## Dokumentation

- [Projektbeschreibung](docs/project-description.md)
- [Architektur](docs/architecture.md)
- [Roadmap](docs/roadmap.md)
- [Änderungshistorie](docs/timeline.md)

## Rechtlicher Hinweis

OpenUASLog ersetzt keine rechtliche Beratung, behördlich vorgeschriebene Prüfung oder verbindliche luftrechtliche Dokumentation.
