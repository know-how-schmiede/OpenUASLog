# OpenUASLog

**OpenUASLog** ist eine selbst hostbare Open-Source-Webanwendung zur Verwaltung und Dokumentation von UAS-/Drohnenflügen, eigenen Drohnen, Drohnen-Typen, Akkus, Wartungseinträgen und Benutzern.

Das Projekt richtet sich an Drohnen-Teams, Hochschulen, MakerSpaces, Vereine, Ausbildungsgruppen, Modellfluggruppen und Organisationen, die Drohnenflüge strukturiert dokumentieren möchten.

Der geplante Repository-Name lautet:

```text
open-uas-log
```

---

## Ziel des Projekts

OpenUASLog soll ein übersichtliches webbasiertes Flugbuch für Drohnenflüge bereitstellen.

Benutzer können eigene Drohnen verwalten, Flüge dokumentieren und Wartungs- sowie Akkudaten erfassen. Administratoren pflegen zentrale Drohnen-Typen als Vorlagen, aus denen Benutzer eigene Drohnen anlegen können.

Eine zentrale Idee des Systems ist die Trennung zwischen:

```text
Drohnen-Typ = allgemeine technische Vorlage
Eigene Drohne = konkretes Gerät eines Benutzers oder Teams
```

Beispiel:

```text
Drohnen-Typ:
    DJI Mavic 3 Classic

Eigene Drohne:
    Renes Mavic 3 Classic
    Seriennummer: individuell
    Kennzeichen: individuell
    Aufkleber: individuell
    Design/Bemerkung: individuell
```

Die eigene Drohne bleibt dauerhaft mit dem Drohnen-Typ verknüpft. Standardwerte werden aus der Vorlage übernommen, können aber durch benutzerspezifische Werte überschrieben werden.

---

## Projektcharakter

OpenUASLog ist als technisches Hilfsmittel zur strukturierten Dokumentation von UAS-/Drohnenflügen gedacht.

Das Projekt ersetzt keine rechtliche Beratung, keine behördlich vorgeschriebene Prüfung und keine verbindliche luftrechtliche Dokumentation. Je nach Land, Einsatzgebiet und Betriebskategorie können zusätzliche Anforderungen gelten.

---

## Technologischer Hintergrund

OpenUASLog dient gleichzeitig als überschaubares Referenzprojekt für moderne Webentwicklung.

Das Projekt verwendet:

```text
Backend:
    FastAPI
    Python
    SQLAlchemy
    SQLite
    Pydantic

Frontend:
    React
    Vite
    TypeScript
    MUI

Architektur:
    API-first Backend
    getrenntes React/MUI Frontend
    Rollen- und Rechteverwaltung
    Template-zu-Instanz-Prinzip
```

Damit eignet sich OpenUASLog auch als technisches Testprojekt für spätere größere Anwendungen wie NeoFab oder PrintFleet.

---

# Hauptfunktionen

## 1. Benutzerverwaltung

OpenUASLog unterstützt mehrere Benutzer mit unterschiedlichen Rollen.

Geplante Rollen:

```text
Admin
Pilot
Observer
Viewer
```

### Admin

Administratoren können:

```text
Benutzer verwalten
Drohnen-Typen anlegen und bearbeiten
systemweite Einstellungen ändern
alle Drohnen und Flüge einsehen
Wartungseinträge verwalten
Exporte durchführen
```

### Pilot

Piloten können:

```text
eigene Drohnen anlegen
eigene Flüge dokumentieren
eigene Flüge bearbeiten
eigene Flugstatistiken einsehen
Akkus und Wartungseinträge für eigene Drohnen dokumentieren
```

### Observer

Observer können:

```text
bei Flügen als Beobachter eingetragen werden
zugewiesene Flüge einsehen
optional eigene Notizen ergänzen
```

### Viewer

Viewer können:

```text
freigegebene Flüge ansehen
Statistiken lesen
keine eigenen Daten ändern
```

---

## 2. Drohnen-Typen als Admin-Vorlagen

Drohnen-Typen werden zentral durch Administratoren gepflegt.

Ein Drohnen-Typ beschreibt allgemeine technische Eigenschaften eines Modells.

Beispiele:

```text
DJI Mavic 3 Classic
DJI Mini 4 Pro
DJI Air 3
Autel EVO II
Eigenbau FPV Copter 5 Zoll
```

### Datenfelder eines Drohnen-Typs

```text
Hersteller
Modell
Variante
Kategorie
Drohnenklasse
Gewicht
maximale Flugzeit
maximale Geschwindigkeit
Akkutyp
Kamera-Informationen
Sensorik
Fernsteuerungssystem
typische Einsatzbereiche
Beschreibung
Bild
Status
technische Notizen
```

Beispiel:

```text
Hersteller: DJI
Modell: Mavic 3
Variante: Classic
Kategorie: Kameradrohne
Gewicht: 895 g
max. Flugzeit: 46 min
Akkutyp: DJI Intelligent Flight Battery
Kamera: 4/3 CMOS Hasselblad
Status: aktiv
```

---

## 3. Eigene Drohnen aus Vorlagen anlegen

Benutzer können eine neue eigene Drohne anlegen, indem sie einen bestehenden Drohnen-Typ auswählen.

Ablauf:

```text
1. Benutzer klickt auf „Neue Drohne anlegen“
2. Benutzer wählt einen Drohnen-Typ aus
3. OpenUASLog zeigt die Standarddaten der Vorlage an
4. Benutzer ergänzt individuelle Daten
5. Eigene Drohne wird gespeichert
```

Beispiel:

```text
Vorlage:
    DJI Mavic 3 Classic

Eigene Drohne:
    Name: Mavic 3 Classic - Rene
    Seriennummer: individuell
    Kennzeichen: individuell
    Aufkleber: THW UAS-Gruppe
    Design: gelber Case-Aufkleber
    Firmware-Version: individuell
    Bemerkung: Übungs- und Dokumentationsdrohne
```

---

## 4. Vorlage bleibt verknüpft, Felder können überschrieben werden

OpenUASLog verwendet von Anfang an das Prinzip:

```text
Vorlage bleibt verknüpft + Benutzer kann Felder überschreiben
```

Das bedeutet:

Eine eigene Drohne verweist dauerhaft auf einen Drohnen-Typ. Wenn ein Wert bei der eigenen Drohne nicht überschrieben wurde, wird der Wert aus dem Drohnen-Typ angezeigt.

Beispiel:

```text
DroneType.max_flight_time_min = 46
Drone.custom_max_flight_time_min = leer

Anzeige:
    46 min
```

Wenn der Benutzer einen eigenen Wert einträgt:

```text
DroneType.max_flight_time_min = 46
Drone.custom_max_flight_time_min = 38

Anzeige:
    38 min
```

Dadurch bleiben allgemeine technische Informationen zentral pflegbar, während individuelle Abweichungen pro Gerät dokumentiert werden können.

---

## 5. Sichtbarkeit von Standardwerten und Überschreibungen

In der Benutzeroberfläche soll klar sichtbar sein, ob ein Wert aus der Vorlage stammt oder individuell überschrieben wurde.

Beispiel:

```text
Gewicht: 895 g
Quelle: Vorlage

Firmware-Version: 01.00.1200
Quelle: Eigene Drohne

Design: gelbe Markierungsaufkleber
Quelle: Eigene Drohne
```

Mögliche Kennzeichnung:

```text
Aus Vorlage
Überschrieben
Eigener Wert
Nicht gesetzt
```

---

## 6. Flugbuch

Das Flugbuch ist der zentrale Bereich des Systems.

Jeder Flug wird als eigener Eintrag gespeichert.

### Datenfelder eines Fluges

```text
Datum
Startzeit
Endzeit
Dauer
Pilot
Observer
Drohne
Einsatzort
GPS-Koordinaten optional
Flugzweck
Flugart
Wetter
Wind
Temperatur
verwendete Akkus
besondere Vorkommnisse
Notizen
Status
```

### Mögliche Flugarten

```text
Training
Foto/Video
Inspektion
Kartierung
Testflug
Wartungsflug
Schulung
THW/BOS-Übung
Modellflug
Sonstiges
```

### Mögliche Statuswerte

```text
geplant
durchgeführt
abgebrochen
storniert
Nachbereitung offen
abgeschlossen
```

---

## 7. Akkuverwaltung

OpenUASLog soll optional Akkus verwalten können.

Akkus können einer Drohne oder einem Benutzer zugeordnet werden.

### Datenfelder eines Akkus

```text
Akku-ID
Bezeichnung
Typ
Zellenzahl
Kapazität
Hersteller
Kaufdatum
Zyklenzahl
Status
Notizen
```

### Akku-Status

```text
aktiv
in Prüfung
beschädigt
außer Betrieb
archiviert
```

Beim Flug können verwendete Akkus dokumentiert werden.

Optionale Werte:

```text
Startspannung
Endspannung
verbrauchte Kapazität
Auffälligkeiten
```

---

## 8. Wartungslog

Für jede Drohne können Wartungs- und Prüfeinträge gespeichert werden.

### Datenfelder eines Wartungseintrags

```text
Drohne
Datum
Wartungstyp
Beschreibung
durchgeführt von
nächster Prüftermin
Status
Notizen
Anhänge optional
```

### Wartungstypen

```text
Sichtprüfung
Firmware-Update
Propellerwechsel
Akkukontrolle
Reinigung
Reparatur
Kalibrierung
sonstige Wartung
```

### Wartungsstatus

```text
geplant
durchgeführt
offen
überfällig
archiviert
```

---

## 9. Dashboard

Das Dashboard zeigt eine schnelle Übersicht über das System.

Mögliche Kennzahlen:

```text
Flüge gesamt
Flüge diesen Monat
Gesamtflugzeit
aktive Drohnen
Drohnen in Wartung
aktive Akkus
Akkus mit Auffälligkeiten
offene Wartungen
geplante Flüge
```

Für Piloten zeigt das Dashboard hauptsächlich eigene Daten.

Für Administratoren zeigt es systemweite Daten.

---

## 10. Tabellen und Filter

Die Anwendung verwendet MUI DataGrid oder vergleichbare MUI-Tabellenkomponenten.

Wichtige Tabellen:

```text
Flugliste
Drohnenliste
Drohnen-Typen
Akkus
Wartung
Benutzer
```

Filtermöglichkeiten:

```text
Zeitraum
Pilot
Drohne
Drohnen-Typ
Status
Flugart
Wartungsstatus
Akku-Status
```

---

## 11. Exportfunktionen

Für Version 0.1 ist ein CSV-Export vorgesehen.

Mögliche Exporte:

```text
Flüge als CSV
Drohnen als CSV
Akkus als CSV
Wartungen als CSV
```

Spätere Erweiterungen:

```text
PDF-Flugbuch
Jahresbericht
Pilotenauswertung
Drohnenauswertung
Wartungsbericht
```

---

# Datenmodell

## User

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

Rollen:

```text
admin
pilot
observer
viewer
```

---

## DroneType

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

---

## Drone

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

Status:

```text
active
maintenance
inactive
retired
archived
```

---

## Resolved Drone Values

Die Anzeige einer Drohne verwendet aufgelöste Werte.

Beispiel:

```text
resolved_manufacturer
resolved_model
resolved_weight_g
resolved_max_flight_time_min
```

Logik:

```text
Wenn custom_value gesetzt ist:
    verwende custom_value
sonst:
    verwende Wert aus DroneType
```

Beispiel:

```text
DroneType.weight_g = 895
Drone.custom_weight_g = leer
Anzeige: 895 g aus Vorlage

Drone.custom_weight_g = 910
Anzeige: 910 g überschrieben
```

---

## Flight

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

---

## Battery

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

---

## FlightBattery

Zwischentabelle zwischen Flug und Akku:

```text
FlightBattery
├─ id
├─ flight_id
├─ battery_id
├─ start_voltage
├─ end_voltage
├─ used_capacity_mah
├─ notes
```

---

## MaintenanceRecord

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

---

# API-Konzept

## Auth

```text
POST   /api/auth/login
POST   /api/auth/logout
GET    /api/auth/me
```

## Benutzer

```text
GET    /api/users
POST   /api/users
GET    /api/users/{id}
PATCH  /api/users/{id}
DELETE /api/users/{id}
```

## Drohnen-Typen

```text
GET    /api/drone-types
POST   /api/drone-types
GET    /api/drone-types/{id}
PATCH  /api/drone-types/{id}
DELETE /api/drone-types/{id}
```

## Eigene Drohnen

```text
GET    /api/drones
POST   /api/drones
POST   /api/drones/from-template
GET    /api/drones/{id}
GET    /api/drones/{id}/resolved
PATCH  /api/drones/{id}
DELETE /api/drones/{id}
```

## Flüge

```text
GET    /api/flights
POST   /api/flights
GET    /api/flights/{id}
PATCH  /api/flights/{id}
DELETE /api/flights/{id}
```

## Akkus

```text
GET    /api/batteries
POST   /api/batteries
GET    /api/batteries/{id}
PATCH  /api/batteries/{id}
DELETE /api/batteries/{id}
```

## Wartung

```text
GET    /api/maintenance
POST   /api/maintenance
GET    /api/maintenance/{id}
PATCH  /api/maintenance/{id}
DELETE /api/maintenance/{id}
```

## Reports und Exporte

```text
GET    /api/reports/dashboard
GET    /api/reports/flight-hours
GET    /api/export/flights.csv
GET    /api/export/drones.csv
GET    /api/export/maintenance.csv
```

---

# Beispiel: Eigene Drohne aus Vorlage erstellen

## Request

```http
POST /api/drones/from-template
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

## Response

```json
{
  "success": true,
  "drone_id": 12
}
```

---

# Beispiel: Aufgelöste Drohnendaten abrufen

## Request

```http
GET /api/drones/12/resolved
```

## Response

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
  "variant": {
    "value": "Classic",
    "source": "template"
  },
  "weight_g": {
    "value": 895,
    "source": "template"
  },
  "max_flight_time_min": {
    "value": 38,
    "source": "custom"
  },
  "firmware_version": {
    "value": "01.00.1200",
    "source": "custom"
  }
}
```

---

# Frontend-Konzept

## Layout

Die Anwendung verwendet ein Dashboard-Layout mit:

```text
Seitenmenü
Kopfzeile
Benutzer-Menü
Hauptbereich
Statusmeldungen
Responsive Layout
```

Hauptnavigation:

```text
Dashboard
Flüge
Drohnen
Drohnen-Typen
Akkus
Wartung
Benutzer
Einstellungen
```

Je nach Benutzerrolle werden Menüpunkte ein- oder ausgeblendet.

---

## Wichtige Seiten

### DashboardPage

Zeigt Kennzahlen und aktuelle Hinweise.

```text
Flüge diesen Monat
Gesamtflugzeit
aktive Drohnen
offene Wartungen
Drohnen in Wartung
Akkus mit Auffälligkeiten
```

---

### DroneTypesPage

Admin-Seite zur Verwaltung der Drohnen-Typen.

Funktionen:

```text
Drohnen-Typen anzeigen
Drohnen-Typ anlegen
Drohnen-Typ bearbeiten
Drohnen-Typ deaktivieren
Drohnen-Typ duplizieren
```

---

### DronesPage

Benutzerseite für eigene Drohnen.

Funktionen:

```text
eigene Drohnen anzeigen
neue Drohne aus Vorlage anlegen
Drohne bearbeiten
Status ändern
Drohnen-Details öffnen
```

---

### DroneDetailPage

Detailseite einer konkreten Drohne.

Bereiche:

```text
Stammdaten
Technische Daten
Vorlagenwerte
Überschriebene Werte
Flüge
Akkus
Wartung
Notizen
```

Werte aus der Vorlage und überschreibende Werte werden klar markiert.

---

### FlightsPage

Flugliste mit Filter und Export.

Spalten:

```text
Datum
Startzeit
Dauer
Pilot
Drohne
Drohnen-Typ
Ort
Flugart
Status
```

---

### FlightDetailPage

Detailansicht und Bearbeitung eines Fluges.

Bereiche:

```text
Flugdaten
Drohne
Pilot / Observer
Ort
Wetter
Akkus
Vorkommnisse
Notizen
```

---

### BatteriesPage

Akkuverwaltung.

Spalten:

```text
Akku-ID
Typ
Kapazität
Zellenzahl
Zyklen
Status
zugeordnete Drohne
```

---

### MaintenancePage

Wartungsübersicht.

Spalten:

```text
Datum
Drohne
Wartungstyp
Status
durchgeführt von
nächster Termin
```

---

# Vorgeschlagene Projektstruktur

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
│  │  │
│  │  ├─ core/
│  │  │  ├─ config.py
│  │  │  ├─ security.py
│  │  │  └─ permissions.py
│  │  │
│  │  ├─ db/
│  │  │  ├─ database.py
│  │  │  └─ init_db.py
│  │  │
│  │  ├─ models/
│  │  │  ├─ user.py
│  │  │  ├─ drone_type.py
│  │  │  ├─ drone.py
│  │  │  ├─ flight.py
│  │  │  ├─ battery.py
│  │  │  └─ maintenance.py
│  │  │
│  │  ├─ schemas/
│  │  │  ├─ user.py
│  │  │  ├─ drone_type.py
│  │  │  ├─ drone.py
│  │  │  ├─ flight.py
│  │  │  ├─ battery.py
│  │  │  └─ maintenance.py
│  │  │
│  │  ├─ services/
│  │  │  ├─ drone_value_resolver.py
│  │  │  ├─ flight_duration.py
│  │  │  └─ export_service.py
│  │  │
│  │  └─ main.py
│  │
│  ├─ requirements.txt
│  └─ README.md
│
├─ frontend/
│  ├─ src/
│  │  ├─ api/
│  │  │  ├─ client.ts
│  │  │  ├─ drones.ts
│  │  │  ├─ droneTypes.ts
│  │  │  ├─ flights.ts
│  │  │  └─ auth.ts
│  │  │
│  │  ├─ components/
│  │  │  ├─ AppLayout.tsx
│  │  │  ├─ StatusChip.tsx
│  │  │  ├─ SourceBadge.tsx
│  │  │  └─ ConfirmDialog.tsx
│  │  │
│  │  ├─ pages/
│  │  │  ├─ DashboardPage.tsx
│  │  │  ├─ LoginPage.tsx
│  │  │  ├─ DroneTypesPage.tsx
│  │  │  ├─ DronesPage.tsx
│  │  │  ├─ DroneDetailPage.tsx
│  │  │  ├─ FlightsPage.tsx
│  │  │  ├─ FlightDetailPage.tsx
│  │  │  ├─ BatteriesPage.tsx
│  │  │  ├─ MaintenancePage.tsx
│  │  │  └─ UsersPage.tsx
│  │  │
│  │  ├─ types/
│  │  │  ├─ drone.ts
│  │  │  ├─ flight.ts
│  │  │  └─ user.ts
│  │  │
│  │  ├─ App.tsx
│  │  └─ main.tsx
│  │
│  ├─ package.json
│  └─ vite.config.ts
│
├─ docs/
│  ├─ architecture.md
│  ├─ api.md
│  ├─ data-model.md
│  └─ screenshots/
│
├─ templates/
│  └─ drone-types/
│     ├─ dji-mavic-3-classic.json
│     ├─ dji-mini-4-pro.json
│     └─ example-custom-drone.json
│
├─ docker-compose.yml
├─ LICENSE
├─ README.md
└─ .gitignore
```

---

# MVP-Version 0.1

Die erste Version soll bewusst klein bleiben.

## Enthalten in Version 0.1

```text
Backend mit FastAPI
SQLite-Datenbank
React + Vite + TypeScript + MUI Frontend
Login
Rollen Admin und Pilot
Admin kann Drohnen-Typen anlegen
User kann Drohnen aus Vorlagen anlegen
Vorlage bleibt mit eigener Drohne verknüpft
User kann ausgewählte Felder überschreiben
Flüge können dokumentiert werden
Flugliste mit Filtern
Dashboard mit einfachen Kennzahlen
CSV-Export für Flüge
```

## Nicht enthalten in Version 0.1

```text
PDF-Export
Kartenansicht
Wetter-API
DJI-Logimport
ArduPilot/PX4-Logimport
Mobile App
Mehrsprachigkeit
komplexe Compliance-Prüfung
automatische Luftraumprüfung
Benachrichtigungen
```

---

# Roadmap

## Version 0.1 - MVP

```text
Projektstruktur
Backend-Grundsystem
Datenbankmodelle
Login
Rollen Admin/Pilot
Drohnen-Typen
Eigene Drohnen mit Template-Verknüpfung
Override-Logik
Flugbuch
Dashboard
CSV-Export
README
Docker-Setup
```

## Version 0.2 - Akku und Wartung

```text
Akkuverwaltung
Akkus pro Flug erfassen
Wartungslog
Wartungsstatus
Drohnenstatus automatisch aus Wartung ableiten
erweiterte Filter
```

## Version 0.3 - Reports und Dokumentation

```text
PDF-Export
Jahresbericht
Pilotenauswertung
Drohnenauswertung
Wartungsbericht
Import/Export von Drohnen-Typ-Vorlagen
```

## Version 0.4 - Erweiterte Funktionen

```text
Kartenansicht
Checklisten vor dem Flug
Anhänge
Fotos
QR-Codes für Drohnen und Akkus
Mehrsprachigkeit Deutsch/Englisch
```

## Version 0.5 - Integrationen

```text
Import von Fluglogs
Wetterdaten
Kalenderansicht
Benachrichtigungen
REST-API-Dokumentation für externe Tools
```

---

# Open-Source-Ansatz

OpenUASLog soll als Open-Source-Repository auf GitHub veröffentlicht werden.

Empfohlene Lizenz:

```text
MIT License
```

Alternativ:

```text
Apache 2.0
```

Das Repository soll enthalten:

```text
README.md
Installationsanleitung
Entwicklungsanleitung
Screenshots
API-Dokumentation
Beispieldaten
Demo-Drohnen-Typen
Docker-Setup
Contribution Guide
License
```

---

# Beispielhafte README-Kurzbeschreibung

```text
OpenUASLog is a self-hosted open-source web application for documenting UAS and drone flights, drones, drone type templates, batteries and maintenance records. It is built with FastAPI, React, Vite, TypeScript and MUI.

The application uses a template-based drone model: administrators maintain general drone types, while users create their own drones from these templates and can override individual fields.
```

Deutsche Beschreibung:

```text
OpenUASLog ist eine selbst hostbare Open-Source-Webanwendung zur Dokumentation von UAS-/Drohnenflügen, Drohnen, Drohnen-Typen, Akkus und Wartungsdaten.

Administratoren verwalten allgemeine Drohnen-Typen als Vorlagen. Benutzer können daraus eigene Drohnen anlegen. Die eigene Drohne bleibt mit der Vorlage verknüpft, einzelne Felder können jedoch individuell überschrieben werden.
```

---

# Nutzen als Referenzprojekt

OpenUASLog dient auch als technisches Referenzprojekt für spätere größere Anwendungen.

Die folgenden Architekturprinzipien können später in anderen Projekten wiederverwendet werden:

```text
API-first Backend
React/MUI Frontend
Rollen- und Rechteverwaltung
Vorlage-zu-Instanz-Prinzip
Override-Logik
Tabellen und Filter
Formularvalidierung
CSV/PDF-Export
Dashboard-Struktur
Docker-Deployment
```

Insbesondere das Muster:

```text
Vorlage → konkrete Instanz → individuelle Überschreibungen
```

ist später auch für Systeme wie NeoFab oder PrintFleet relevant.

Beispiele:

```text
Drohnen-Typ → konkrete Drohne
Drucker-Typ → konkreter Drucker
Auftrags-Typ → konkreter Auftrag
Materialprofil → konkretes Material
Slicer-Profil → konkrete G-Code-Datei
```

---

# Zusammenfassung

OpenUASLog ist ein überschaubares, aber praxisnahes Open-Source-Projekt zur Dokumentation von UAS-/Drohnenflügen.

Der wichtigste Architekturpunkt ist die Trennung zwischen zentral gepflegten Drohnen-Typen und individuell verwalteten Benutzerdrohnen.

Das System verwendet von Beginn an eine verknüpfte Vorlagenstruktur mit überschreibbaren Feldern.

Dadurch entsteht ein sauberes, modernes Webprojekt, mit dem sich die spätere Architektur größerer Systeme wie NeoFab oder PrintFleet sehr gut vorbereiten und testen lässt.
