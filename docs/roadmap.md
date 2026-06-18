# OpenUASLog Roadmap

Diese Roadmap beschreibt die geplante schrittweise Entwicklung von OpenUASLog. Der Schwerpunkt liegt zunächst auf einem kleinen, nutzbaren Flugbuch und wird anschließend um Akkuverwaltung, Wartung, Berichte und externe Integrationen erweitert.

Die Reihenfolge stellt die derzeitige Planung dar. Umfang und Prioritäten können sich während der Entwicklung ändern.

---

## Version 0.1 – MVP

Ziel der ersten Version ist ein lauffähiges Grundsystem zur Verwaltung eigener Drohnen und zur Dokumentation von Flügen.

Geplanter Umfang:

- Projektstruktur für Backend und Frontend
- Backend-Grundsystem mit FastAPI
- SQLite-Datenbank und grundlegende Datenmodelle
- React-Frontend mit Vite, TypeScript und MUI
- Login
- Rollen `Admin` und `Pilot`
- Verwaltung zentraler Drohnen-Typen durch Administratoren
- Anlegen eigener Drohnen aus Drohnen-Typ-Vorlagen
- Dauerhafte Verknüpfung zwischen eigener Drohne und Vorlage
- Überschreiben ausgewählter Vorlagenwerte pro Drohne
- Kennzeichnung von Vorlagenwerten und individuellen Werten
- Flugbuch mit Erfassung und Bearbeitung von Flügen
- Flugliste mit grundlegenden Filtern
- Dashboard mit einfachen Kennzahlen
- CSV-Export für Flüge
- README und grundlegende Projektdokumentation
- Docker-Setup

Nicht Bestandteil von Version 0.1:

- PDF-Export
- Kartenansicht
- Wetter-API
- Import von DJI-, ArduPilot- oder PX4-Fluglogs
- Mobile App
- Mehrsprachigkeit
- komplexe Compliance-Prüfungen
- automatische Luftraumprüfung
- Benachrichtigungen

---

## Version 0.2 – Akku und Wartung

Diese Version erweitert das Flugbuch um die technische Verwaltung und Zustandsdokumentation der Ausrüstung.

Geplanter Umfang:

- Akkuverwaltung
- Zuordnung von Akkus zu Benutzern und Drohnen
- Erfassung verwendeter Akkus pro Flug
- optionale Dokumentation von Spannung, Kapazität und Auffälligkeiten
- Wartungs- und Prüfprotokoll für Drohnen
- Wartungsstatus und nächste Prüftermine
- automatische Ableitung des Drohnenstatus aus offenen Wartungen
- erweiterte Filter für Flüge, Drohnen, Akkus und Wartung

---

## Version 0.3 – Reports und Dokumentation

Der Schwerpunkt dieser Version liegt auf auswertbaren und exportierbaren Betriebsdaten.

Geplanter Umfang:

- PDF-Export
- Jahresbericht
- Pilotenauswertung
- Drohnenauswertung
- Wartungsbericht
- Import und Export von Drohnen-Typ-Vorlagen

---

## Version 0.4 – Erweiterte Funktionen

Diese Version ergänzt Funktionen für den praktischen Einsatz und verbessert die Dokumentation direkt am Fluggerät.

Geplanter Umfang:

- Kartenansicht
- Checklisten vor dem Flug
- Dateianhänge
- Fotos
- QR-Codes für Drohnen und Akkus
- Mehrsprachigkeit in Deutsch und Englisch

---

## Version 0.5 – Integrationen

In dieser Version wird OpenUASLog stärker mit externen Datenquellen und Werkzeugen verbunden.

Geplanter Umfang:

- Import von Fluglogs
- Einbindung von Wetterdaten
- Kalenderansicht
- Benachrichtigungen
- REST-API-Dokumentation für externe Tools

---

## Langfristige Ausrichtung

OpenUASLog soll als selbst hostbare Open-Source-Anwendung eine nachvollziehbare Dokumentation von UAS- und Drohnenflügen ermöglichen. Die Architektur bleibt API-first und trennt zentral gepflegte Vorlagen von konkreten, individuell anpassbaren Geräten.

Das Projekt ersetzt keine rechtliche Beratung, behördliche Prüfung oder verbindliche luftrechtliche Dokumentation. Zusätzliche Anforderungen können abhängig von Land, Einsatzgebiet und Betriebskategorie gelten.
