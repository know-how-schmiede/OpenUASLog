# OpenUASLog Projektbeschreibung

OpenUASLog ist eine selbst hostbare Open-Source-Webanwendung zur Verwaltung und Dokumentation von UAS-/Drohnenflügen, eigenen Drohnen, Drohnen-Typen, Akkus, Wartungseinträgen und Benutzern.

Das Projekt richtet sich an Drohnen-Teams, Hochschulen, MakerSpaces, Vereine, Ausbildungsgruppen, Modellfluggruppen und Organisationen, die Drohnenflüge strukturiert dokumentieren möchten.

---

## Ziel des Projekts

OpenUASLog stellt ein übersichtliches webbasiertes Flugbuch für Drohnenflüge bereit. Benutzer verwalten eigene Drohnen, dokumentieren Flüge und erfassen Wartungs- sowie Akkudaten.

Administratoren pflegen zentrale Drohnen-Typen als Vorlagen, aus denen Benutzer eigene Drohnen anlegen:

```text
Drohnen-Typ = allgemeine technische Vorlage
Eigene Drohne = konkretes Gerät eines Benutzers oder Teams
```

Eine eigene Drohne bleibt mit ihrem Drohnen-Typ verknüpft. Standardwerte werden aus der Vorlage übernommen und können durch individuelle Werte überschrieben werden.

Die technische Umsetzung dieses Prinzips ist in der [Architekturdokumentation](architecture.md) beschrieben.

---

## Projektcharakter

OpenUASLog ist ein technisches Hilfsmittel zur strukturierten Dokumentation von UAS-/Drohnenflügen.

Das Projekt ersetzt keine rechtliche Beratung, behördlich vorgeschriebene Prüfung oder verbindliche luftrechtliche Dokumentation. Abhängig von Land, Einsatzgebiet und Betriebskategorie können zusätzliche Anforderungen gelten.

---

## Hauptfunktionen

### Benutzerverwaltung

Geplante Rollen:

- Admin
- Pilot
- Observer
- Viewer

Administratoren verwalten Benutzer, Drohnen-Typen, systemweite Einstellungen, Wartungsdaten und Exporte. Piloten verwalten eigene Drohnen, Flüge, Akkus und Wartungseinträge. Observer und Viewer erhalten eingeschränkte Lese- und Dokumentationsrechte.

### Drohnen-Typen

Administratoren pflegen allgemeine technische Vorlagen, beispielsweise:

- Hersteller und Modell
- Variante und Kategorie
- Drohnenklasse und Gewicht
- maximale Flugzeit und Geschwindigkeit
- Akku-, Kamera- und Sensorinformationen
- Fernsteuerungssystem
- typische Einsatzbereiche
- Beschreibung, Bild und Status

### Eigene Drohnen

Benutzer wählen einen Drohnen-Typ aus und ergänzen individuelle Gerätedaten:

- Name
- Seriennummer
- Kennzeichen und Inventarnummer
- Aufkleber und Designmerkmale
- Firmware-Version
- Kauf- und Versicherungsdaten
- Status und Notizen

Vorlagenwerte und individuelle Überschreibungen werden in der Oberfläche klar gekennzeichnet.

### Flugbuch

Jeder Flug wird als eigener Eintrag gespeichert. Erfasst werden unter anderem:

- Datum, Startzeit, Endzeit und Dauer
- Pilot und Observer
- Drohne
- Einsatzort und optionale GPS-Koordinaten
- Flugzweck und Flugart
- Wetter, Wind und Temperatur
- verwendete Akkus
- besondere Vorkommnisse
- Notizen und Status

### Akkuverwaltung

Akkus können Benutzern oder Drohnen zugeordnet und bei Flügen dokumentiert werden. Neben Stammdaten sind Zyklenzahl, Status, Spannungswerte, verbrauchte Kapazität und Auffälligkeiten vorgesehen.

### Wartungslog

Für jede Drohne können Wartungs- und Prüfeinträge mit Datum, Wartungstyp, ausführender Person, nächstem Prüftermin, Status, Notizen und optionalen Anhängen gespeichert werden.

### Dashboard

Das Dashboard zeigt abhängig von der Benutzerrolle eigene oder systemweite Kennzahlen:

- Flüge und Gesamtflugzeit
- aktive Drohnen
- Drohnen in Wartung
- aktive oder auffällige Akkus
- offene Wartungen
- geplante Flüge

### Tabellen und Filter

Flüge, Drohnen, Drohnen-Typen, Akkus, Wartungen und Benutzer werden in filterbaren Tabellen dargestellt. Geplante Filter umfassen Zeitraum, Pilot, Drohne, Drohnen-Typ, Flugart und verschiedene Statuswerte.

### Exporte

Für die erste Version ist ein CSV-Export für Flüge vorgesehen. Spätere Versionen ergänzen weitere CSV- und PDF-Berichte.

---

## MVP-Version 0.1

Die erste Version bleibt bewusst klein und umfasst:

- FastAPI-Backend
- SQLite-Datenbank
- React-, Vite-, TypeScript- und MUI-Frontend
- Login
- Rollen Admin und Pilot
- Verwaltung von Drohnen-Typen
- eigene Drohnen aus Vorlagen
- verknüpfte Vorlagen und individuelle Überschreibungen
- Flugbuch
- Flugliste mit Filtern
- Dashboard mit einfachen Kennzahlen
- CSV-Export für Flüge
- Docker-Setup

Nicht im MVP enthalten sind unter anderem PDF-Export, Kartenansicht, Wetter-API, Fluglog-Import, Mobile App, Mehrsprachigkeit, automatische Luftraumprüfung und Benachrichtigungen.

Die weitere Entwicklung ist in der [Roadmap](roadmap.md) beschrieben.

---

## Open-Source-Ansatz

OpenUASLog soll als Open-Source-Repository auf GitHub veröffentlicht werden. Vorgesehen ist eine MIT- oder Apache-2.0-Lizenz.

Das Repository soll neben dem Quellcode folgende Inhalte bereitstellen:

- Installations- und Entwicklungsanleitung
- Architektur- und API-Dokumentation
- Screenshots
- Beispieldaten und Demo-Drohnen-Typen
- Docker-Setup
- Contribution Guide
- Lizenz

---

## Kurzbeschreibung

> OpenUASLog is a self-hosted open-source web application for documenting UAS and drone flights, drones, drone type templates, batteries and maintenance records. Administrators maintain general drone types, while users create their own drones from these templates and can override individual fields.
