# Verkaufsdaten Analyse & Dashboard

End-to-End-Lösung Zur Analyse Von Verkaufsdaten Mit Python, SQLite and Streamlit.

Im Kern ist es eine ETL-Pipeline Zum Laden, Analysieren Mit SQL und Visualisieren Von Verkaufsdaten sowie einem Benutzerfreundlichen Dashboard Zum Einfachen Analysieren.

---

## Projektübersicht
- **ETL-Pipeline (`etl_pipeline.py`):**
 Generische Verkaufsdaten extrahieren, den Gesamtpreis berechnen, in eine SQLite-Datenbank (`sales.db`) laden und Sample SQL Querys ausführen.

- **Interaktives Dashboard (`dashboard.py`):
 Streamlit zur Darstellung Von Verkaufs-KPIs nutzen, darunter:
 - Umsatz nach Produktvisualisieren
 - Durchschnittlicher Bestellwert
 - Top Kunden Nach Umsatz
 - Anzahl Der Verkäufe Nach Produktvisualisieren
 - grafischer Filter Nach Kunden

- **SQL-Abfragen (`sales_data_analysis.sql`):
 Alle wichtigen SQL-Abfragen, die im Rahmen der Verkaufsanalyse genutzt werden.

- **Beispieldaten (`sales_data.csv`):**
 CSV-Datei mit generischen Verkaufsdaten als Zieldatenquelle.

---

## Voraussetzungen
- Python 3.8 oder neuer
- SQLite (optional, falls direkt mit DB gearbeitet werden soll)

---

## Installation
1. Repo klonen oder Dateien herunterladen.
2. Sämtliche Bibliotheken installieren:

```bash
pip install pandas urllib3 matplotlib seaborn streamlit

