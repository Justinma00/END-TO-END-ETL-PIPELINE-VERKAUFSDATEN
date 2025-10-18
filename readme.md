# Verkaufsdaten Analyse & Dashboard

Eine umfassende End-to-End ETL-Pipeline zur Analyse von Verkaufsdaten mit Python, SQLite und Streamlit.

Dieses Projekt bietet eine vollständige Lösung für das Extrahieren, Transformieren und Laden von Verkaufsdaten mit erweiterten Analysen und einem interaktiven Dashboard für Business Intelligence.

## 🚀 Funktionen

- **Vollständige ETL-Pipeline**: Daten aus CSV-Dateien extrahieren, mit Berechnungen transformieren und in SQLite-Datenbank laden
- **Interaktives Dashboard**: Streamlit-basiertes Dashboard mit umfassenden Verkaufsanalysen
- **Erweiterte Analysen**: Umsatzanalyse, Kundeninsights, Produktperformance und zeitbasierte Trends
- **Datenvisualisierung**: Schöne Diagramme und Grafiken mit Matplotlib und Seaborn
- **Umfassende Tests**: Vollständiger Testsatz mit Unit- und Integrationstests
- **Professionelle Code-Qualität**: Type Hints, Fehlerbehandlung, Logging und Dokumentation

## 📊 Dashboard-Funktionen

- **Key Performance Indicators**: Gesamtumsatz, durchschnittlicher Bestellwert, Gesamtbestellungen, einzigartige Kunden
- **Umsatzanalyse**: Umsatzaufschlüsselung nach Produkten mit interaktiven Diagrammen
- **Kundenanalysen**: Top-Kunden, Bestellverteilung, kundenspezifische Analysen
- **Produktperformance**: Bestellanzahlen, durchschnittliche Bestellwerte, Produktvergleich
- **Zeitanalyse**: Datumsbereichsfilterung, tägliche Umsatztrends
- **Datenexplorer**: Rohe Datenfilterung und Exportfunktionalität

## 🛠️ Installation

### Voraussetzungen
- Python 3.8 oder neuer
- pip (Python Package Installer)

### Schnellstart

1. **Repository klonen:**
```bash
git clone <repository-url>
cd END-TO-END-ETL-PIPELINE-VERKAUFSDATEN
```

2. **Abhängigkeiten installieren:**
```bash
pip install -r requirements.txt
```

3. **ETL-Pipeline ausführen:**
```bash
python etl_pipeline.py
```

4. **Dashboard starten:**
```bash
streamlit run dashboard.py
```

### Entwicklungsumgebung

Für die Entwicklung mit zusätzlichen Tools:

```bash
# Entwicklungsabhängigkeiten installieren
pip install -e ".[dev]"

# Pre-commit Hooks installieren
pre-commit install

# Tests ausführen
pytest

# Linting ausführen
black .
isort .
flake8 .
mypy .
```

## 📁 Projektstruktur

```
END-TO-END-ETL-PIPELINE-VERKAUFSDATEN/
├── etl_pipeline.py          # Haupt-ETL-Pipeline mit SalesETLPipeline-Klasse
├── dashboard.py             # Interaktives Streamlit-Dashboard
├── sales_data.csv          # Beispieldaten
├── sales_analysis.sql      # SQL-Abfragen für Analysen
├── sales.db               # SQLite-Datenbank (generiert)
├── tests/                 # Umfassender Testsatz
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_etl_pipeline.py
│   └── test_dashboard.py
├── requirements.txt       # Python-Abhängigkeiten
├── pyproject.toml        # Projektkonfiguration
├── .pre-commit-config.yaml # Pre-commit Hooks
└── README.md             # Diese Datei
```

## 🎯 Verwendung

### ETL-Pipeline

Die ETL-Pipeline verarbeitet Verkaufsdaten in drei Hauptstufen:

1. **Extract**: Daten aus CSV-Dateien laden
2. **Transform**: Gesamtpreise berechnen und Daten validieren
3. **Load**: Daten in SQLite-Datenbank mit Indizes speichern

```python
from etl_pipeline import SalesETLPipeline

# Pipeline initialisieren
pipeline = SalesETLPipeline("sales_data.csv", "sales.db")

# Vollständige Pipeline ausführen
results = pipeline.run_pipeline()

# Visualisierung erstellen
pipeline.plot_revenue_by_product()
```

### Dashboard

Interaktives Dashboard starten:

```bash
streamlit run dashboard.py
```

Das Dashboard bietet:
- Echtzeit-Datenvisualisierung
- Interaktive Filterung und Analyse
- Export-Funktionalität
- Responsives Design

## 🧪 Tests

Umfassenden Testsatz ausführen:

```bash
# Alle Tests ausführen
pytest

# Mit Coverage ausführen
pytest --cov=.

# Spezifische Testtypen ausführen
pytest -m unit          # Nur Unit-Tests
pytest -m integration   # Nur Integrationstests
pytest -m "not slow"    # Langsame Tests überspringen
```

## 📈 Analyseabfragen

Das System enthält vordefinierte Analyseabfragen:

- **Revenue by Product / Umsatz nach Produkt**: Gesamtumsatzaufschlüsselung nach Produkt
- **Average Order Value / Durchschnittlicher Bestellwert**: Mittlerer Bestellwert über alle Verkäufe
- **Top Customer / Top-Kunde**: Kunde mit dem höchsten Gesamtumsatz
- **Total Sales Summary / Gesamtverkaufszusammenfassung**: Gesamte Verkaufsstatistiken

## 🔧 Konfiguration

### Datenbankkonfiguration
- Standarddatenbank: `sales.db`
- Automatische Indexerstellung für Performance
- Verbindungsverwaltung mit ordnungsgemäßer Bereinigung

### Logging
- Umfassendes Logging durch die gesamte Pipeline
- Konfigurierbare Log-Level
- Fehlerverfolgung und Debugging-Informationen

### Datenvalidierung
- Eingabedatenvalidierung
- Erkennung negativer Werte
- Behandlung fehlender Spalten
- Datentypverifizierung

## 🚀 Performance-Funktionen

- **Database Indexing / Datenbankindizierung**: Automatische Erstellung von Performance-Indizes
- **Efficient Queries / Effiziente Abfragen**: Optimierte SQL-Abfragen für Analysen
- **Memory Management / Speicherverwaltung**: Ordnungsgemäße Ressourcenbereinigung
- **Error Handling / Fehlerbehandlung**: Robuste Fehlerbehandlung und Wiederherstellung

## 📋 Anforderungen

### Kernabhängigkeiten
- `pandas>=1.5.0` - Datenmanipulation und -analyse
- `matplotlib>=3.5.0` - Datenvisualisierung
- `seaborn>=0.11.0` - Statistische Datenvisualisierung
- `streamlit>=1.28.0` - Interaktive Webanwendungen

### Entwicklungsabhängigkeiten
- `pytest>=7.0.0` - Testframework
- `black>=22.0.0` - Codeformatierung
- `isort>=5.10.0` - Import-Sortierung
- `flake8>=5.0.0` - Linting
- `mypy>=1.0.0` - Typüberprüfung

## 🤝 Beitragen

1. Repository forken
2. Feature-Branch erstellen (`git checkout -b feature/amazing-feature`)
3. Änderungen vornehmen
4. Tests ausführen (`pytest`)
5. Linting ausführen (`black . && isort . && flake8 .`)
6. Änderungen committen (`git commit -m 'Add amazing feature'`)
7. Branch pushen (`git push origin feature/amazing-feature`)
8. Pull Request öffnen

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe LICENSE-Datei für Details.

## 🆘 Support

Für Support bitte ein Issue im GitHub-Repository öffnen oder die Maintainer kontaktieren.

## 🔄 Versionshistorie

- **v1.0.0** - Erstveröffentlichung mit vollständiger ETL-Pipeline und Dashboard
  - Umfassende ETL-Pipeline mit Fehlerbehandlung
  - Interaktives Streamlit-Dashboard
  - Vollständiger Testsatz
  - Professionelle Code-Qualitätsstandards

---

# Sales Data Analysis & Dashboard

A comprehensive end-to-end ETL pipeline for sales data analysis using Python, SQLite, and Streamlit.

This project provides a complete solution for extracting, transforming, and loading sales data, with advanced analytics and an interactive dashboard for business intelligence.

## 🚀 Features

- **Complete ETL Pipeline**: Extract data from CSV files, transform with calculations, and load into SQLite database
- **Interactive Dashboard**: Streamlit-based dashboard with comprehensive sales analytics
- **Advanced Analytics**: Revenue analysis, customer insights, product performance, and time-based trends
- **Data Visualization**: Beautiful charts and graphs using Matplotlib and Seaborn
- **Comprehensive Testing**: Full test suite with unit and integration tests
- **Professional Code Quality**: Type hints, error handling, logging, and documentation

## 📊 Dashboard Features

- **Key Performance Indicators**: Total revenue, average order value, total orders, unique customers
- **Revenue Analysis**: Revenue breakdown by product with interactive charts
- **Customer Analytics**: Top customers, order distribution, customer-specific analysis
- **Product Performance**: Order counts, average order values, product comparison
- **Time Analysis**: Date range filtering, daily revenue trends
- **Data Explorer**: Raw data filtering and export functionality

## 🛠️ Installation

### Prerequisites
- Python 3.8 or newer
- pip (Python package installer)

### Quick Start

1. **Clone the repository:**
```bash
git clone <repository-url>
cd END-TO-END-ETL-PIPELINE-VERKAUFSDATEN
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the ETL pipeline:**
```bash
python etl_pipeline.py
```

4. **Launch the dashboard:**
```bash
streamlit run dashboard.py
```

### Development Setup

For development with additional tools:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run linting
black .
isort .
flake8 .
mypy .
```

## 📁 Project Structure

```
END-TO-END-ETL-PIPELINE-VERKAUFSDATEN/
├── etl_pipeline.py          # Main ETL pipeline with SalesETLPipeline class
├── dashboard.py             # Interactive Streamlit dashboard
├── sales_data.csv          # Sample sales data
├── sales_analysis.sql      # SQL queries for analysis
├── sales.db               # SQLite database (generated)
├── tests/                 # Comprehensive test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_etl_pipeline.py
│   └── test_dashboard.py
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration
├── .pre-commit-config.yaml # Pre-commit hooks
└── README.md             # This file
```

## 🎯 Usage

### ETL Pipeline

The ETL pipeline processes sales data through three main stages:

1. **Extract**: Load data from CSV files
2. **Transform**: Calculate total prices and validate data
3. **Load**: Store data in SQLite database with indexes

```python
from etl_pipeline import SalesETLPipeline

# Initialize pipeline
pipeline = SalesETLPipeline("sales_data.csv", "sales.db")

# Run complete pipeline
results = pipeline.run_pipeline()

# Create visualization
pipeline.plot_revenue_by_product()
```

### Dashboard

Launch the interactive dashboard:

```bash
streamlit run dashboard.py
```

The dashboard provides:
- Real-time data visualization
- Interactive filtering and analysis
- Export functionality
- Responsive design

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test types
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m "not slow"    # Skip slow tests
```

## 📈 Analytics Queries

The system includes predefined analytical queries:

- **Revenue by Product**: Total revenue breakdown by product
- **Average Order Value**: Mean order value across all sales
- **Top Customer**: Customer with highest total revenue
- **Total Sales Summary**: Overall sales statistics

## 🔧 Configuration

### Database Configuration
- Default database: `sales.db`
- Automatic index creation for performance
- Connection management with proper cleanup

### Logging
- Comprehensive logging throughout the pipeline
- Configurable log levels
- Error tracking and debugging information

### Data Validation
- Input data validation
- Negative value detection
- Missing column handling
- Data type verification

## 🚀 Performance Features

- **Database Indexing**: Automatic creation of performance indexes
- **Efficient Queries**: Optimized SQL queries for analytics
- **Memory Management**: Proper resource cleanup
- **Error Handling**: Robust error handling and recovery

## 📋 Requirements

### Core Dependencies
- `pandas>=1.5.0` - Data manipulation and analysis
- `matplotlib>=3.5.0` - Data visualization
- `seaborn>=0.11.0` - Statistical data visualization
- `streamlit>=1.28.0` - Interactive web applications

### Development Dependencies
- `pytest>=7.0.0` - Testing framework
- `black>=22.0.0` - Code formatting
- `isort>=5.10.0` - Import sorting
- `flake8>=5.0.0` - Linting
- `mypy>=1.0.0` - Type checking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Run linting (`black . && isort . && flake8 .`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## 🔄 Version History

- **v1.0.0** - Initial release with complete ETL pipeline and dashboard
  - Comprehensive ETL pipeline with error handling
  - Interactive Streamlit dashboard
  - Full test suite
  - Professional code quality standards

