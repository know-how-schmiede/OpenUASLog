# OpenUASLog Architektur

Dieses Dokument beschreibt die technische Architektur von OpenUASLog. Die Anwendung ist als selbst hostbares, API-first aufgebautes System mit getrenntem Backend und Frontend geplant.

---

## Technologie-Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite

### Frontend

- React
- Vite
- TypeScript
- MUI
- MUI DataGrid für tabellarische Ansichten

### Architekturprinzipien

- API-first Backend
- getrenntes React-Frontend
- rollenbasierte Rechteverwaltung
- zentrale Vorlagen und konkrete Benutzerinstanzen
- individuelle Überschreibungen von Vorlagenwerten
- nachvollziehbare Herkunft aufgelöster Werte
- selbst hostbares Deployment

---

## Systemübersicht

```text
Browser
  |
  v
React / TypeScript / MUI
  |
  v
FastAPI REST API
  |
  +-- Authentifizierung und Berechtigungen
  +-- Anwendungsservices
  +-- Pydantic-Schemas
  |
  v
SQLAlchemy
  |
  v
SQLite
```

Das Frontend kommuniziert ausschließlich über die REST-API mit dem Backend. Geschäftslogik wie die Auflösung von Drohnenwerten, Berechtigungsprüfungen, Berechnung von Flugdauern und Exporte liegt im Backend.

---

## Rollen und Berechtigungen

OpenUASLog sieht vier Rollen vor:

| Rolle | Berechtigungen |
| --- | --- |
| `admin` | Benutzer, Drohnen-Typen, systemweite Daten, Wartungen und Exporte verwalten |
| `pilot` | Eigene Drohnen, Flüge, Akkus und Wartungseinträge verwalten |
| `observer` | Zugewiesene Flüge einsehen und optional Notizen ergänzen |
| `viewer` | Freigegebene Flüge und Statistiken lesen |

Das MVP beginnt mit den Rollen `admin` und `pilot`. Weitere Rollen werden später ergänzt.

---

## Vorlage-zu-Instanz-Prinzip

Der zentrale Architekturbaustein ist die Trennung zwischen einem allgemeinen Drohnen-Typ und einer konkreten Drohne:

```text
DroneType
  |
  +-- zentrale technische Vorlage
  |
  v
Drone
  |
  +-- konkretes Gerät eines Benutzers oder Teams
  +-- individuelle Gerätedaten
  +-- optionale Überschreibungen der Vorlage
```

Eine konkrete Drohne bleibt dauerhaft mit ihrem Drohnen-Typ verknüpft. Nicht überschriebene technische Werte werden dynamisch aus der Vorlage gelesen.

### Auflösung eines Wertes

```text
Wenn Drone.custom_value gesetzt ist:
    verwende Drone.custom_value
    Quelle = custom
sonst:
    verwende DroneType.value
    Quelle = template
```

Beispiel:

```text
DroneType.max_flight_time_min = 46
Drone.custom_max_flight_time_min = 38

Aufgelöster Wert:
    value = 38
    source = custom
```

Das Frontend kennzeichnet die Herkunft eines Wertes, beispielsweise mit:

- Aus Vorlage
- Überschrieben
- Eigener Wert
- Nicht gesetzt

Die Auflösungslogik wird in einem Backend-Service zentral implementiert, damit Listen, Detailseiten, Exporte und externe API-Nutzer dieselben Ergebnisse erhalten.

---

## Datenmodell

### User

```text
User
├─ id
├─ username
├─ email
├─ password_hash
├─ full_name
├─ role
├─ is_active
├─ created_at
└─ updated_at
```

### DroneType

`DroneType` enthält die zentral gepflegten technischen Standardwerte eines Drohnenmodells.

```text
DroneType
├─ id
├─ manufacturer
├─ model
├─ variant
├─ category
├─ drone_class
├─ weight_g
├─ max_flight_time_min
├─ max_speed_kmh
├─ battery_type
├─ camera_info
├─ sensor_info
├─ remote_controller
├─ typical_use
├─ description
├─ image_url
├─ is_active
├─ created_by_user_id
├─ created_at
└─ updated_at
```

### Drone

`Drone` repräsentiert ein konkretes Gerät. Neben individuellen Stammdaten enthält das Modell optionale Überschreibungen für technische Vorlagenwerte.

```text
Drone
├─ id
├─ owner_user_id
├─ drone_type_id
├─ name
├─ serial_number
├─ registration_mark
├─ inventory_number
├─ sticker_label
├─ design_notes
├─ firmware_version
├─ purchase_date
├─ insurance_info
├─ status
├─ notes
│
├─ custom_manufacturer
├─ custom_model
├─ custom_variant
├─ custom_category
├─ custom_drone_class
├─ custom_weight_g
├─ custom_max_flight_time_min
├─ custom_max_speed_kmh
├─ custom_battery_type
├─ custom_camera_info
├─ custom_sensor_info
├─ custom_remote_controller
│
├─ created_at
└─ updated_at
```

Mögliche Statuswerte:

```text
active
maintenance
inactive
retired
archived
```

### Flight

```text
Flight
├─ id
├─ drone_id
├─ pilot_user_id
├─ observer_user_id
├─ date
├─ start_time
├─ end_time
├─ duration_minutes
├─ location_name
├─ latitude
├─ longitude
├─ flight_type
├─ purpose
├─ weather
├─ wind
├─ temperature_c
├─ incidents
├─ notes
├─ status
├─ created_at
└─ updated_at
```

### Battery

```text
Battery
├─ id
├─ owner_user_id
├─ assigned_drone_id
├─ label
├─ manufacturer
├─ battery_type
├─ cell_count
├─ capacity_mah
├─ serial_number
├─ purchase_date
├─ cycle_count
├─ status
├─ notes
├─ created_at
└─ updated_at
```

### FlightBattery

`FlightBattery` bildet die n:m-Beziehung zwischen Flügen und Akkus ab und speichert flugspezifische Messwerte.

```text
FlightBattery
├─ id
├─ flight_id
├─ battery_id
├─ start_voltage
├─ end_voltage
├─ used_capacity_mah
└─ notes
```

### MaintenanceRecord

```text
MaintenanceRecord
├─ id
├─ drone_id
├─ maintenance_date
├─ maintenance_type
├─ description
├─ performed_by_user_id
├─ next_due_date
├─ status
├─ notes
├─ created_at
└─ updated_at
```

### Beziehungen

```text
User 1 ─── n Drone
User 1 ─── n Flight              als Pilot
User 1 ─── n Flight              als Observer
User 1 ─── n Battery
User 1 ─── n MaintenanceRecord   als ausführende Person

DroneType 1 ─── n Drone
Drone     1 ─── n Flight
Drone     1 ─── n Battery
Drone     1 ─── n MaintenanceRecord

Flight n ─── m Battery           über FlightBattery
```

---

## API-Konzept

### Authentifizierung

```http
POST   /api/auth/login
POST   /api/auth/logout
GET    /api/auth/me
```

### Benutzer

```http
GET    /api/users
POST   /api/users
GET    /api/users/{id}
PATCH  /api/users/{id}
DELETE /api/users/{id}
```

### Drohnen-Typen

```http
GET    /api/drone-types
POST   /api/drone-types
GET    /api/drone-types/{id}
PATCH  /api/drone-types/{id}
DELETE /api/drone-types/{id}
```

### Eigene Drohnen

```http
GET    /api/drones
POST   /api/drones
POST   /api/drones/from-template
GET    /api/drones/{id}
GET    /api/drones/{id}/resolved
PATCH  /api/drones/{id}
DELETE /api/drones/{id}
```

### Flüge

```http
GET    /api/flights
POST   /api/flights
GET    /api/flights/{id}
PATCH  /api/flights/{id}
DELETE /api/flights/{id}
```

### Akkus

```http
GET    /api/batteries
POST   /api/batteries
GET    /api/batteries/{id}
PATCH  /api/batteries/{id}
DELETE /api/batteries/{id}
```

### Wartung

```http
GET    /api/maintenance
POST   /api/maintenance
GET    /api/maintenance/{id}
PATCH  /api/maintenance/{id}
DELETE /api/maintenance/{id}
```

### Reports und Exporte

```http
GET    /api/reports/dashboard
GET    /api/reports/flight-hours
GET    /api/export/flights.csv
GET    /api/export/drones.csv
GET    /api/export/maintenance.csv
```

### Beispiel: Drohne aus Vorlage erstellen

```http
POST /api/drones/from-template
Content-Type: application/json
```

```json
{
  "drone_type_id": 1,
  "name": "Mavic 3 Classic - Rene",
  "serial_number": "SN-123456",
  "registration_mark": "DEU-XXXX",
  "sticker_label": "THW UAS-Gruppe",
  "design_notes": "Gelber Case-Aufkleber, markierte Akkus",
  "firmware_version": "01.00.1200",
  "notes": "Für Übungsflüge und Dokumentation"
}
```

### Beispiel: Aufgelöste Drohnendaten

```http
GET /api/drones/12/resolved
```

```json
{
  "id": 12,
  "name": "Mavic 3 Classic - Rene",
  "manufacturer": {
    "value": "DJI",
    "source": "template"
  },
  "model": {
    "value": "Mavic 3",
    "source": "template"
  },
  "weight_g": {
    "value": 895,
    "source": "template"
  },
  "max_flight_time_min": {
    "value": 38,
    "source": "custom"
  }
}
```

---

## Frontend-Architektur

Das Frontend verwendet ein responsives Dashboard-Layout mit Seitenmenü, Kopfzeile, Benutzer-Menü, Hauptbereich und Statusmeldungen. Die Navigation wird anhand der Rolle des angemeldeten Benutzers gefiltert.

Geplante Hauptseiten:

| Seite | Aufgabe |
| --- | --- |
| `DashboardPage` | Kennzahlen, offene Wartungen und aktuelle Hinweise |
| `DroneTypesPage` | Administrative Verwaltung der Drohnen-Typen |
| `DronesPage` | Verwaltung konkreter Benutzerdrohnen |
| `DroneDetailPage` | Stammdaten, aufgelöste Werte, Flüge, Akkus und Wartung |
| `FlightsPage` | Filterbare Flugliste und Export |
| `FlightDetailPage` | Anzeige und Bearbeitung eines Fluges |
| `BatteriesPage` | Akkuverwaltung |
| `MaintenancePage` | Wartungsübersicht |
| `UsersPage` | Benutzerverwaltung |

Wiederverwendbare Komponenten kapseln Statusanzeigen, Quellenkennzeichnungen und Bestätigungsdialoge:

```text
StatusChip
SourceBadge
ConfirmDialog
```

---

## Vorgeschlagene Projektstruktur

```text
open-uas-log/
├─ backend/
│  ├─ app/
│  │  ├─ api/
│  │  │  ├─ routes_auth.py
│  │  │  ├─ routes_users.py
│  │  │  ├─ routes_drone_types.py
│  │  │  ├─ routes_drones.py
│  │  │  ├─ routes_flights.py
│  │  │  ├─ routes_batteries.py
│  │  │  └─ routes_maintenance.py
│  │  ├─ core/
│  │  │  ├─ config.py
│  │  │  ├─ security.py
│  │  │  └─ permissions.py
│  │  ├─ db/
│  │  │  ├─ database.py
│  │  │  └─ init_db.py
│  │  ├─ models/
│  │  ├─ schemas/
│  │  ├─ services/
│  │  │  ├─ drone_value_resolver.py
│  │  │  ├─ flight_duration.py
│  │  │  └─ export_service.py
│  │  └─ main.py
│  └─ requirements.txt
├─ frontend/
│  ├─ src/
│  │  ├─ api/
│  │  ├─ components/
│  │  ├─ pages/
│  │  ├─ types/
│  │  ├─ App.tsx
│  │  └─ main.tsx
│  ├─ package.json
│  └─ vite.config.ts
├─ docs/
│  ├─ architecture.md
│  ├─ project-description.md
│  ├─ roadmap.md
│  ├─ timeline.md
│  └─ README.md
├─ templates/
│  └─ drone-types/
├─ docker-compose.yml
├─ LICENSE
├─ README.md
└─ version.py
```

---

## Erweiterbarkeit

Das Muster aus Vorlage, konkreter Instanz und individuellen Überschreibungen ist nicht auf Drohnen beschränkt:

```text
Drohnen-Typ  → konkrete Drohne
Drucker-Typ  → konkreter Drucker
Materialprofil → konkretes Material
```

Die Architektur dient deshalb zugleich als überschaubares Referenzprojekt für API-first Anwendungen mit Rollenverwaltung, Formularvalidierung, Tabellen, Filtern, Exporten und Docker-Deployment.
