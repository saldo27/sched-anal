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
- **💾 Exportación**: Descarga de resultados en CSV y PDF (A4 apaisado)
- **🎨 Interfaz moderna**: Diseño responsivo con Tailwind CSS
- **💻 Multiplataforma**: Windows, macOS y Linux

## 🚀 Instalación en Windows

### Requisitos previos

1. **Python 3.8+**: Descarga desde [python.org](https://www.python.org/downloads/)
   - ⚠️ **IMPORTANTE**: Marca "Add Python to PATH" durante la instalación
   
2. **Node.js 16+**: Descarga desde [nodejs.org](https://nodejs.org/)
   - Incluye npm (gestor de paquetes)

### Paso 1: Clonar o descargar el repositorio

```bash
git clone https://github.com/saldo27/sched-anal.git
cd sched-anal
```

### Paso 2: Ejecutar el instalador

Haz doble clic en `install.bat` o ejecuta desde terminal:

```bash
install.bat
```

Este script:
- ✅ Verifica que Python esté instalado
- ✅ Crea un entorno virtual Python
- ✅ Instala todas las dependencias (Flask, ReportLab, etc.)
- ✅ Instala dependencias del frontend (React, Vite)

### Paso 3: Ejecutar la aplicación

Haz doble clic en `run.bat` o ejecuta:

```bash
run.bat
```

Esto iniciará automáticamente:
- **Backend** (Flask) en `http://localhost:5000`
- **Frontend** (React) en `http://localhost:3000`

📱 Se abrirá automáticamente en tu navegador en `http://localhost:3000`

## 🖥️ Instalación en macOS/Linux

### Requisitos previos

```bash
# macOS
brew install python@3.12 node

# Linux (Ubuntu/Debian)
sudo apt-get install python3.12 python3.12-venv nodejs npm
```

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/saldo27/sched-anal.git
cd sched-anal

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

# Instalar dependencias
pip install -r requirements.txt
npm install

# Ejecutar aplicación
# Terminal 1 - Backend
python app.py

# Terminal 2 - Frontend
npm run dev
```

Accede a `http://localhost:3000`

## 🚀 Uso

1. **Cargar archivo**: Sube un PDF, Excel o ingresa texto manualmente
2. **Ver análisis**: Se genera automáticamente un resumen de turnos
3. **Visualizar datos**: 
   - Gráfico de barras por trabajador
   - Tabla con estadísticas completas
   - Desglose mensual
4. **Exportar**: 
   - CSV: Descarga datos tabulares
   - PDF: Genera reporte formateado (A4 apaisado)

## 📊 Estructura del Proyecto

```
sched-anal/
├── app.py                 # Backend Flask
├── file_processor.py      # Procesador de archivos
├── CalendarAnalyzer.jsx   # Componente principal React
├── requirements.txt       # Dependencias Python
├── package.json          # Dependencias Node.js
├── install.bat           # Instalador Windows
├── run.bat              # Ejecutor Windows
├── setup.py             # Configuración para distribución
└── README.md            # Este archivo
```

## 🛠️ Desarrollo

### Backend (Python)

```bash
# Activar entorno virtual
venv\Scripts\activate.bat  # Windows
source venv/bin/activate   # macOS/Linux

# Instalar en modo desarrollo
pip install -e .

# Ejecutar con modo debug
python app.py  # Escucha en http://localhost:5000
```

### Frontend (React)

```bash
# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo con hot reload
npm run dev

# Compilar para producción
npm run build

# Vista previa de build
npm run preview
```

## 📝 Requisitos de Dependencias

### Python
- Flask 3.1.2: Framework web
- flask-cors 4.0.0: CORS para comunicación frontend-backend
- pandas: Procesamiento de datos
- openpyxl: Lectura de archivos Excel
- pdfplumber: Extracción de texto de PDFs
- ReportLab: Generación de PDFs
- python-dateutil: Utilities de fechas

### Node.js
- React 18: UI framework
- Vite 4: Build tool y dev server
- Recharts: Visualización de gráficos
- Tailwind CSS: Estilos

## 🐛 Solución de Problemas

### "Python no está en el PATH"
- Desinstala Python
- Reinstala asegurándote de marcar "Add Python to PATH"
- Reinicia el computador

### Puerto 5000 o 3000 ya en uso
```bash
# Busca qué proceso usa el puerto
netstat -ano | findstr :5000  # Windows
lsof -i :5000                  # macOS/Linux

# Termina el proceso
taskkill /PID <PID> /F  # Windows
kill -9 <PID>           # macOS/Linux
```

### El PDF no se genera
- Asegúrate de que ReportLab esté instalado: `pip install --upgrade ReportLab`
- Verifica que tengas espacio en disco

## 📄 Licencia

MIT License - Ver LICENSE para detalles

## 👨‍💻 Autor

Desarrollado por el equipo de Análisis de Turnos

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit cambios (`git commit -m "Agregué mejora"`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

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
