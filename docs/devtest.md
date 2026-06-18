# OpenUASLog testen

Diese Anleitung führt Anfänger Schritt für Schritt durch einen vollständigen Funktionstest von OpenUASLog Version 0.1.0.

Die Anleitung setzt voraus, dass die App nach [setup.md](setup.md) eingerichtet und gestartet wurde.

---

## 1. Testziel

Am Ende des Tests wurde geprüft, dass:

- Backend und Frontend erreichbar sind
- die Admin-Anmeldung funktioniert
- ein Drohnen-Typ angelegt werden kann
- eine konkrete Drohne aus der Vorlage erzeugt werden kann
- ein Flug dokumentiert wird
- die Flugdauer automatisch berechnet wird
- das Dashboard die neuen Daten anzeigt
- ein CSV-Export heruntergeladen werden kann
- die automatisierten Backend-Tests erfolgreich laufen

---

## 2. Dienste prüfen

### Docker-Status prüfen

Im Projektordner ausführen:

```powershell
docker compose ps
```

Erwartetes Ergebnis:

- Backend läuft.
- Frontend läuft.
- Für das Frontend wird Port `8080` angezeigt.

Wenn ein Dienst nicht läuft:

```powershell
docker compose logs backend
docker compose logs frontend
```

### Health-Check prüfen

Im Browser <http://localhost:8080/health> öffnen.

Erwartete Antwort:

```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

Damit ist geprüft, dass das Backend erreichbar ist und die erwartete Version ausführt.

---

## 3. Anmeldung testen

1. <http://localhost:8080> öffnen.
2. Den in `.env` gesetzten Admin-Benutzernamen eingeben.
3. Das in `.env` gesetzte Admin-Passwort eingeben.
4. Auf **Anmelden** klicken.

Erwartetes Ergebnis:

- Das Dashboard wird geöffnet.
- Oben rechts werden der Benutzername beziehungsweise vollständige Name und die Rolle `admin` angezeigt.
- Im Seitenmenü sind Dashboard, Flüge, Drohnen und Drohnen-Typen sichtbar.

Bei einer Fehlermeldung die Hinweise im Abschnitt „Anmeldung funktioniert nicht“ in [setup.md](setup.md) prüfen.

---

## 4. Drohnen-Typ anlegen

1. Im Seitenmenü **Drohnen-Typen** wählen.
2. Auf **Neuer Typ** klicken.
3. Folgende Testdaten eintragen:

| Feld | Testwert |
| --- | --- |
| Hersteller | DJI |
| Modell | Mavic 3 |
| Variante | Classic |
| Kategorie | Kameradrohne |
| Drohnenklasse | C1 |
| Gewicht | 895 |
| Max. Flugzeit | 46 |

4. Auf **Speichern** klicken.

Erwartetes Ergebnis:

- Der Dialog wird geschlossen.
- Der neue Drohnen-Typ erscheint in der Tabelle.
- Hersteller, Modell, Gewicht und Flugzeit stimmen mit den Testdaten überein.
- Der Typ wird als aktiv angezeigt.

---

## 5. Eigene Drohne aus der Vorlage anlegen

1. Im Seitenmenü **Drohnen** wählen.
2. Auf **Neue Drohne** klicken.
3. Den zuvor angelegten Drohnen-Typ `DJI Mavic 3 Classic` auswählen.
4. Folgende Daten eintragen:

| Feld | Testwert |
| --- | --- |
| Name | Testdrohne Mavic 3 |
| Seriennummer | TEST-SN-001 |
| Kennzeichen | DEU-TEST |
| Firmware-Version | 01.00.1200 |

5. Auf **Speichern** klicken.

Erwartetes Ergebnis:

- Die Drohne erscheint in der Drohnenliste.
- Der gewählte Drohnen-Typ wird angezeigt.
- Seriennummer, Kennzeichen und Firmware-Version stimmen.
- Der Status lautet `active`.

Die konkrete Drohne bleibt intern mit dem Drohnen-Typ verknüpft. Technische Werte wie Gewicht und maximale Flugzeit stammen aus der Vorlage, solange sie nicht individuell überschrieben werden.

---

## 6. Flug dokumentieren

1. Im Seitenmenü **Flüge** wählen.
2. Auf **Neuer Flug** klicken.
3. Folgende Daten eintragen:

| Feld | Testwert |
| --- | --- |
| Drohne | Testdrohne Mavic 3 |
| Datum | heutiges Datum |
| Startzeit | 10:00 |
| Endzeit | 10:25 |
| Ort | Testgelände |
| Flugart | Training |
| Status | durchgeführt |
| Zweck | Funktionstest Version 0.1.0 |

4. Auf **Speichern** klicken.

Erwartetes Ergebnis:

- Der Flug erscheint in der Flugliste.
- Die Dauer beträgt `25` Minuten.
- Drohne, Ort, Flugart und Status stimmen mit den eingegebenen Daten überein.

Die Dauer wird aus Start- und Endzeit automatisch vom Backend berechnet.

---

## 7. Dashboard prüfen

1. Im Seitenmenü **Dashboard** wählen.
2. Die Kennzahlen kontrollieren.

Nach dem beschriebenen Test sollten mindestens folgende Werte enthalten sein:

- Flüge gesamt: mindestens `1`
- Flüge diesen Monat: mindestens `1`, wenn das heutige Datum verwendet wurde
- Gesamtflugzeit: mindestens `25 min`
- Aktive Drohnen: mindestens `1`

Sind bereits weitere Daten vorhanden, können die Zahlen entsprechend höher sein.

---

## 8. CSV-Export testen

1. Wieder **Flüge** öffnen.
2. Auf **CSV** klicken.
3. Den Download im Browser bestätigen, falls erforderlich.
4. Die Datei `openuaslog-flights.csv` öffnen.

Erwartetes Ergebnis:

- Die Datei wurde heruntergeladen.
- Die erste Zeile enthält Spaltenüberschriften.
- Der Testflug enthält unter anderem:
  - das gewählte Datum
  - `10:00`
  - `10:25`
  - `25`
  - `Testdrohne Mavic 3`
  - `Testgelände`
  - `Training`

Die Datei ist UTF-8-kodiert und kann beispielsweise mit Excel oder LibreOffice Calc geöffnet werden.

---

## 9. API-Dokumentation testen

Die interaktive API-Dokumentation ist erreichbar unter:

- Docker: <http://localhost:8080/api/docs>
- lokale Entwicklung: <http://localhost:8000/api/docs>

### Health-Check über Swagger

Der Health-Check liegt außerhalb des `/api`-Bereichs und wird am einfachsten direkt über <http://localhost:8080/health> geprüft.

### Anmeldung über Swagger

1. In Swagger den Bereich `auth` öffnen.
2. `POST /api/auth/login` auswählen.
3. Auf **Try it out** klicken.
4. Folgenden Request-Body eintragen:

```json
{
  "username": "admin",
  "password": "DAS_PASSWORT_AUS_DER_ENV_DATEI"
}
```

5. Auf **Execute** klicken.

Erwartetes Ergebnis:

- HTTP-Status `200`
- Die Antwort enthält `access_token`, `token_type` und `user`.

Den Wert von `access_token` kopieren.

### Geschützte API-Endpunkte autorisieren

1. Oben rechts in Swagger auf **Authorize** klicken.
2. Den kopierten Token einfügen.
3. Auf **Authorize** und anschließend **Close** klicken.
4. `GET /api/auth/me` öffnen.
5. **Try it out** und danach **Execute** wählen.

Erwartetes Ergebnis:

- HTTP-Status `200`
- Die Antwort enthält den angemeldeten Admin-Benutzer.

Nun können weitere Endpunkte aus der API-Dokumentation getestet werden. Änderungen über `POST`, `PATCH` und `DELETE` wirken auf die verwendete Datenbank.

---

## 10. Automatisierte Backend-Tests ausführen

Die automatisierten Tests verwenden eine separate Testdatenbank und verändern die normale App-Datenbank nicht.

### Lokale Python-Umgebung

Im Projektordner:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m pytest -q
```

Erwartetes Ergebnis:

```text
3 passed
```

Die Tests prüfen:

- Health-Check und Versionsnummer
- Anmeldung und vollständigen MVP-Ablauf
- Auflösung von Vorlagen- und Überschreibungswerten
- automatische Flugdauer
- Dashboard-Auswertung
- CSV-Export
- Rollen- und Eigentümerrechte

### Tests ohne vorhandene virtuelle Umgebung

Zuerst die Entwicklungsabhängigkeiten installieren:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

---

## 11. Frontend technisch prüfen

Node.js und npm müssen installiert sein.

```powershell
cd frontend
npm install
npm run build
```

Erwartetes Ergebnis:

- TypeScript wird ohne Fehler kompiliert.
- Vite erzeugt den Ordner `frontend/dist`.
- Der Befehl endet erfolgreich.

Zusätzlich kann die statische Prüfung ausgeführt werden:

```powershell
npm run lint
```

---

## 12. Testdaten zurücksetzen

Dieser Schritt löscht die lokale Docker-Datenbank vollständig. Nur verwenden, wenn alle Testdaten entfernt werden dürfen.

Anwendung und Daten-Volume löschen:

```powershell
docker compose down -v
```

Danach neu starten:

```powershell
docker compose up --build
```

Beim Neustart wird eine leere Datenbank mit dem initialen Admin-Benutzer aus `.env` angelegt.

---

## 13. Fehler dokumentieren

Bei einem Fehler folgende Informationen notieren:

- ausgeführter Schritt
- erwartetes Ergebnis
- tatsächliches Ergebnis
- vollständige Fehlermeldung
- Browser und Browserversion
- Ausgabe von `docker compose ps`
- relevante Ausgabe aus `docker compose logs backend` oder `docker compose logs frontend`
- Version aus <http://localhost:8080/health>

Passwörter, Token und Inhalte der `.env`-Datei dürfen nicht in Fehlerberichte kopiert werden.

---

## 14. Test erfolgreich abgeschlossen

Der Grundtest ist erfolgreich, wenn:

- der Health-Check `status: ok` meldet
- die Anmeldung funktioniert
- Drohnen-Typ, Drohne und Flug gespeichert werden
- die Flugdauer korrekt berechnet wird
- das Dashboard aktualisierte Werte zeigt
- der CSV-Export den Testflug enthält
- die automatisierten Backend-Tests bestehen
