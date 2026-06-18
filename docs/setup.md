# OpenUASLog einrichten

Diese Anleitung beschreibt die Einrichtung von OpenUASLog unter Windows. Für Anfänger wird der Start mit Docker empfohlen, weil dabei Backend, Frontend und Datenbank gemeinsam eingerichtet werden.

---

## 1. Voraussetzungen

Für die empfohlene Einrichtung werden benötigt:

- Windows 10 oder Windows 11
- Git
- Docker Desktop
- eine PowerShell
- ein moderner Webbrowser

Installationsseiten:

- Git: <https://git-scm.com/download/win>
- Docker Desktop: <https://www.docker.com/products/docker-desktop/>

Nach der Installation von Docker Desktop muss das Programm gestartet werden. Warten, bis Docker den Status **Running** anzeigt.

### Installation prüfen

PowerShell öffnen und folgende Befehle einzeln ausführen:

```powershell
git --version
docker --version
docker compose version
```

Jeder Befehl muss eine Versionsnummer ausgeben. Erscheint stattdessen eine Meldung wie „Befehl wurde nicht gefunden“, muss das betreffende Programm installiert oder das Terminal neu geöffnet werden.

---

## 2. Repository herunterladen

In PowerShell in den gewünschten übergeordneten Ordner wechseln:

```powershell
cd C:\Data\GitHub
```

Repository klonen:

```powershell
git clone <URL-DES-REPOSITORY>
cd OpenUASLog
```

Wenn das Repository bereits vorhanden ist, nur in den Projektordner wechseln:

```powershell
cd C:\Data\GitHub\OpenUASLog
```

Die folgenden Befehle müssen immer im Root-Verzeichnis des Projekts ausgeführt werden. Dort befinden sich unter anderem `docker-compose.yml`, `backend`, `frontend` und `docs`.

---

## 3. Konfiguration anlegen

Die Beispielkonfiguration kopieren:

```powershell
Copy-Item .env.example .env
```

Die neue Datei `.env` mit einem Texteditor öffnen:

```powershell
notepad .env
```

Beispiel:

```dotenv
OPENUASLOG_SECRET_KEY=hier-einen-langen-zufaelligen-geheimen-wert-eintragen
OPENUASLOG_INITIAL_ADMIN_USERNAME=admin
OPENUASLOG_INITIAL_ADMIN_EMAIL=admin@example.com
OPENUASLOG_INITIAL_ADMIN_PASSWORD=hier-ein-sicheres-passwort-eintragen
```

Wichtig:

- `OPENUASLOG_SECRET_KEY` muss in einer produktiven Installation lang und zufällig sein.
- Das Standardpasswort `admin` darf außerhalb einer lokalen Testumgebung nicht verwendet werden.
- Die Zugangsdaten werden nur beim erstmaligen Anlegen der Datenbank für das initiale Administratorkonto verwendet.
- Die Datei `.env` darf nicht in Git eingecheckt oder weitergegeben werden.

Datei speichern und den Editor schließen.

---

## 4. Anwendung mit Docker starten

Im Root-Verzeichnis ausführen:

```powershell
docker compose up --build
```

Beim ersten Start werden die benötigten Container-Images heruntergeladen, Python- und Node-Abhängigkeiten installiert und beide Anwendungsteile gebaut. Das kann einige Minuten dauern.

Der Start ist abgeschlossen, wenn keine Fehlermeldungen mehr erscheinen und die Container weiterlaufen.

Danach im Browser öffnen:

| Bereich | Adresse |
| --- | --- |
| Weboberfläche | <http://localhost:8080> |
| API-Dokumentation | <http://localhost:8080/api/docs> |
| Health-Check | <http://localhost:8080/health> |

Am Webinterface mit den in `.env` gesetzten Admin-Zugangsdaten anmelden.

### Anwendung im Hintergrund starten

Nach dem erfolgreichen ersten Aufbau kann OpenUASLog im Hintergrund gestartet werden:

```powershell
docker compose up -d
```

Status prüfen:

```powershell
docker compose ps
```

Beide Dienste sollten als laufend angezeigt werden:

- `backend`
- `frontend`

Protokolle anzeigen:

```powershell
docker compose logs -f
```

Die Protokollansicht wird mit `Strg+C` beendet. Die Container laufen dabei weiter.

---

## 5. Anwendung stoppen und erneut starten

Anwendung stoppen:

```powershell
docker compose down
```

Die SQLite-Datenbank bleibt dabei im Docker-Volume erhalten.

Erneut starten:

```powershell
docker compose up -d
```

Nach Änderungen am Quellcode neu bauen:

```powershell
docker compose up --build
```

---

## 6. Lokale Entwicklungsumgebung ohne Docker

Für die lokale Entwicklung werden zusätzlich benötigt:

- Python 3.11 oder neuer
- Node.js 22 oder neuer
- npm

Prüfen:

```powershell
python --version
node --version
npm --version
```

### Backend einrichten

Vom Root-Verzeichnis aus:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Backend starten:

```powershell
python -m uvicorn app.main:app --reload
```

Das Backend ist anschließend erreichbar unter:

- API: <http://localhost:8000/api>
- API-Dokumentation: <http://localhost:8000/api/docs>
- Health-Check: <http://localhost:8000/health>

Dieses PowerShell-Fenster geöffnet lassen.

### Frontend einrichten

Ein zweites PowerShell-Fenster öffnen und in den Projektordner wechseln:

```powershell
cd C:\Data\GitHub\OpenUASLog\frontend
npm install
npm run dev
```

Danach die Weboberfläche unter <http://localhost:5173> öffnen.

### Lokale Datenbank

Beim ersten Backend-Start wird standardmäßig die Datei angelegt:

```text
backend/data/openuaslog.db
```

Sie enthält die lokalen Benutzer-, Drohnen- und Flugdaten.

---

## 7. Häufige Probleme

### Docker-Befehl wurde nicht gefunden

Docker Desktop installieren oder neu starten. Danach PowerShell schließen und neu öffnen.

### Port 8080 oder 8000 ist bereits belegt

Prüfen, ob eine andere Instanz der App läuft:

```powershell
docker compose ps
```

Vorhandene Instanz stoppen:

```powershell
docker compose down
```

### Anmeldung funktioniert nicht

- Benutzername und Passwort aus `.env` prüfen.
- Beachten, dass das initiale Konto nur beim ersten Erstellen der Datenbank angelegt wird.
- Groß- und Kleinschreibung des Passworts kontrollieren.

### Änderung an `.env` wird nicht übernommen

Container neu erstellen:

```powershell
docker compose down
docker compose up --build
```

Änderungen an den initialen Admin-Daten verändern kein bereits vorhandenes Benutzerkonto.

### Fehler genauer untersuchen

```powershell
docker compose logs backend
docker compose logs frontend
```

Der Health-Check unter <http://localhost:8080/health> sollte folgende Struktur liefern:

```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

---

## 8. Nächster Schritt

Nach erfolgreichem Start die [Schritt-für-Schritt-Testanleitung](devtest.md) durcharbeiten.
