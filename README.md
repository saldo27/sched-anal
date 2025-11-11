# 📊 Analizador de Calendarios de Turnos (sched-anal)

Aplicación web para analizar horarios de turnos desde archivos PDF, Excel o texto. Genera estadísticas detalladas por trabajador con visualización de datos interactiva.

## 🎯 Características

- **📤 Carga de archivos**: PDF, Excel (.xlsx, .xls), CSV y entrada de texto manual
- **📊 Estadísticas detalladas**:
  - Total de turnos por trabajador
  - Desglose por mes
  - Análisis de fin de semana (viernes, sábado, domingo)
  - Porcentaje de turnos en fin de semana
  - Análisis de última posición
  
- **📈 Visualización**: Gráficos interactivos con Recharts
- **📋 Tablas**: Ordenamiento y filtrado de datos
- **💾 Exportación**: Descarga de resultados en CSV
- **🎨 Interfaz moderna**: Diseño responsivo con Tailwind CSS

## 🚀 Inicio Rápido

### Opción 1: Frontend Solo (sin backend)

```bash
# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev

# Compilar para producción
npm run build
```

Accede a `http://localhost:3000`

### Opción 2: Full Stack (Frontend + Backend)

#### Backend (Python/Flask)

```bash
# Instalar dependencias Python
pip install -r requirements.txt

# Ejecutar servidor Flask
python app.py
```

El backend estará disponible en `http://localhost:5000`

#### Frontend (React/Vite)

```bash
# En otra terminal
npm install
npm run dev
```

Frontend en `http://localhost:3000` (proxy automático a backend)

## 📁 Estructura del Proyecto

```
sched-anal/
├── Frontend (React)
│   ├── CalendarAnalyzer.jsx      # Componente principal
│   ├── main.jsx                  # Entrada React
│   ├── index.html                # HTML
│   ├── index.css                 # Estilos
│   ├── vite.config.js            # Config Vite
│   ├── tailwind.config.js        # Config Tailwind
│   └── postcss.config.js         # Config PostCSS
│
├── Backend (Python)
│   ├── app.py                    # API Flask
│   ├── file_processor.py         # Procesamiento de archivos
│   └── requirements.txt          # Dependencias Python
│
├── package.json                  # Dependencias Node.js
├── README.md                     # Este archivo
└── FILE_UPLOAD_GUIDE.md         # Guía completa de API
```

## 📖 Uso

### Interfaz Web

1. **Cargar archivo o texto**:
   - Carga un archivo PDF, Excel o CSV
   - O pega el texto del calendario directamente

2. **Configurar parámetros**:
   - Fecha de inicio del calendario
   - Mapeo de nombres (ej: REQUE=LUIS REQUENA)

3. **Analizar**: Haz clic en "Analizar Calendario"

4. **Visualizar y exportar**:
   - Ve gráficos y tablas de resultados
   - Descarga resultados en CSV

### Uso Programático (Python)

```python
from file_processor import CalendarFileProcessor

# Procesar archivo
processor = CalendarFileProcessor()
text = processor.process_file('calendario.pdf')

# Detectar estructura
structure = processor.detect_calendar_structure(text)
print(structure)
```bash
python sched_analyzer.py schedule.xlsx
```

### Output Formats

Display results in different formats:
```bash
# Table format (default)
python sched_analyzer.py schedule.xlsx

# CSV format
python sched_analyzer.py schedule.xlsx --format csv

# JSON format
python sched_analyzer.py schedule.xlsx --format json
```

### Save Results to File

Save the analysis results to a file:
```bash
python sched_analyzer.py schedule.xlsx -o results.csv
```

### Supported File Formats

- Excel files: `.xlsx`, `.xls`
- PDF files: `.pdf`

## Input File Format

The application expects shift schedule files in calendar format with:
- Calendar layout with days of the week (Monday-Sunday)
- Dates or day numbers (1-31) in the header or cells
- Worker names in cells corresponding to their assigned shifts
- Supports PDF files with table-based calendars or Excel spreadsheets

### Supported Formats

**PDF Format**: Calendar-style PDFs with:
- Day numbers (1-31) in cells
- Worker names assigned under each day
- Multiple calendars on separate pages (one per month)

**Excel Format**: Spreadsheets with:
- Dates in the first column or first row
- Worker names in cells corresponding to shifts
- Optional position columns for tracking shift positions

### Example Excel Format

| Date       | Position 1 | Position 2 | Position 3 |
|------------|------------|------------|------------|
| 2024-11-01 | Alice      | Bob        | Charlie    |
| 2024-11-02 | Bob        | Charlie    | Diana      |
| 2024-11-03 | Charlie    | Diana      | Eve        |

## Testing with Sample Data

Generate and analyze sample data:
```bash
# Create sample schedule
python create_sample_data.py

# Analyze the sample
python sched_analyzer.py sample_schedule.xlsx
```

## Requirements

- Python 3.7+
- pandas
- openpyxl (for Excel files)
- pdfplumber (for PDF files)
- tabulate (for formatted output)

See `requirements.txt` for full dependency list.

## License

MIT License
