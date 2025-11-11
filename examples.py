"""
Example usage and integration guide for the Calendar Analyzer application.
"""

# ============================================================================
# EJEMPLO 1: Procesar archivo PDF desde línea de comandos
# ============================================================================

from file_processor import CalendarFileProcessor

def example_1_process_pdf():
    """Process a PDF file and extract calendar text."""
    processor = CalendarFileProcessor()
    
    try:
        # Procesar archivo PDF
        extracted_text = processor.process_file('calendario.pdf')
        print("Texto extraído del PDF:")
        print(extracted_text)
        
        # Detectar estructura
        structure = processor.detect_calendar_structure(extracted_text)
        print("\nEstructura detectada:")
        print(f"  Días detectados: {structure['days_count']}")
        print(f"  Formato: {structure['detected_format']}")
        
    except Exception as e:
        print(f"Error: {e}")


# ============================================================================
# EJEMPLO 2: Procesar múltiples archivos
# ============================================================================

from pathlib import Path

def example_2_batch_process():
    """Process multiple calendar files in a directory."""
    processor = CalendarFileProcessor()
    
    # Procesar todos los PDFs en un directorio
    directory = './calendarios'
    
    for file_path in Path(directory).glob('*.pdf'):
        try:
            print(f"\nProcesando: {file_path.name}")
            extracted_text = processor.process_file(str(file_path))
            print(f"  ✓ {len(extracted_text)} caracteres extraídos")
        except Exception as e:
            print(f"  ✗ Error: {e}")


# ============================================================================
# EJEMPLO 3: Usar la API Flask desde Python
# ============================================================================

import requests
import json

def example_3_api_upload():
    """Upload a file using the Flask API."""
    
    # URL del servidor Flask
    api_url = 'http://localhost:5000/api/upload'
    
    # Archivo a cargar
    with open('calendario.pdf', 'rb') as f:
        files = {'file': f}
        response = requests.post(api_url, files=files)
    
    if response.status_code == 200:
        data = response.json()
        print("Archivo procesado exitosamente:")
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def example_3_api_analyze():
    """Analyze calendar using the API."""
    
    api_url = 'http://localhost:5000/api/analyze'
    
    payload = {
        'calendarText': '22 23 24\nMANUEL MAR SANTI\nELENA JOSE REQUE\nPATRICIA LAURA MANUEL',
        'startDate': '2025-12-22',
        'nameMapping': 'REQUE=LUIS R\nROBER=ROBERTO'
    }
    
    response = requests.post(api_url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("Análisis completado:")
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.status_code}")


# ============================================================================
# EJEMPLO 4: Usar desde JavaScript/React
# ============================================================================

JAVASCRIPT_EXAMPLE = """
// En React, dentro de CalendarAnalyzer.jsx

// 1. Cargar archivo PDF
const handlePDFUpload = async (event) => {
  const file = event.target.files?.[0];
  if (!file) return;
  
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData
    });
    
    const data = await response.json();
    setCalendarText(data.text);  // Establecer el texto extraído
    setFileName(file.name);
  } catch (error) {
    console.error('Error:', error);
  }
};

// 2. Analizar calendario
const response = await fetch('/api/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    calendarText: calendarText,
    startDate: startDate,
    nameMapping: nameMapping
  })
});

const data = await response.json();
console.log('Estructura detectada:', data.structure);

// 3. Exportar resultados
const response = await fetch('/api/export', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    workers: sortedWorkers,
    format: 'csv'
  })
});

const data = await response.json();
console.log('CSV generado:', data.content);
"""


# ============================================================================
# EJEMPLO 5: Integración con Pandas para análisis adicionales
# ============================================================================

import pandas as pd
from datetime import datetime

def example_5_advanced_analysis():
    """Advanced analysis using Pandas."""
    processor = CalendarFileProcessor()
    
    # Procesar archivo
    extracted_text = processor.process_file('calendario.pdf')
    
    # Aquí iría la lógica de parseo del calendario
    # Convertir a DataFrame de Pandas para análisis avanzados
    
    # Ejemplo de estructura de datos
    data = {
        'date': pd.date_range('2025-12-22', periods=31),
        'worker_1': ['MANUEL'] * 31,
        'worker_2': ['ELENA'] * 31,
        'worker_3': ['SANTI'] * 31,
        'worker_4': ['LOLA'] * 31,
    }
    
    df = pd.DataFrame(data)
    
    # Análisis
    print("Primeras líneas del análisis:")
    print(df.head())
    
    # Estadísticas por trabajador
    print("\nTrabajadores únicos por posición:")
    for col in df.columns[1:]:
        print(f"  {col}: {df[col].nunique()} trabajadores únicos")


# ============================================================================
# EJEMPLO 6: Crear calendario de prueba
# ============================================================================

def example_6_create_test_calendar():
    """Create a test calendar file for development."""
    
    test_calendar = """22 23 24 25 26 27 28
MANUEL MAR SANTI LOLA ELENA MANUEL SANTI
ELENA JOSE REQUE MARINA KIKO MAR LAURA
PATRICIA LAURA MANUEL JOSE SANTI ELENA REQUE
MARINA SANTI ELENA MAR MANUEL PATRICIA JOSE

29 30 31 1 2 3 4
REQUE ELENA MAR SANTI PATRICIA JOSE MANUEL
SANTI LOLA MANUEL MAR ELENA REQUE JOSE
LOLA MARINA SANTI ELENA MANUEL SANTI MAR
ELENA REQUE JOSE PATRICIA LAURA MANUEL SANTI

5 6 7 8 9 10 11
MANUEL PATRICIA SANTI LAURA ELENA JOSE REQUE
MARINA MANUEL MAR SANTI ELENA LAURA PATRICIA
JOSE ELENA REQUE MANUEL SANTI MAR LOLA
SANTI LOLA ELENA PATRICIA MANUEL JOSE MARINA"""
    
    with open('test_calendar.txt', 'w') as f:
        f.write(test_calendar)
    
    print("✓ Archivo test_calendar.txt creado")
    
    # Procesar el archivo de prueba
    processor = CalendarFileProcessor()
    structure = processor.detect_calendar_structure(test_calendar)
    print(f"Estructura detectada: {structure}")


# ============================================================================
# EJEMPLO 7: Validación de formatos
# ============================================================================

def example_7_validate_formats():
    """Validate different file formats."""
    processor = CalendarFileProcessor()
    
    test_files = [
        'calendar.pdf',
        'calendar.xlsx',
        'calendar.csv',
        'calendar.txt',  # Esto debería fallar
    ]
    
    for filename in test_files:
        try:
            processor.process_file(filename)
            print(f"✓ {filename}: Formato soportado")
        except ValueError as e:
            print(f"✗ {filename}: {e}")
        except FileNotFoundError:
            print(f"- {filename}: No existe (ejemplo)")


# ============================================================================
# EJEMPLO 8: Configuración de API (para integración)
# ============================================================================

API_CONFIGURATION = """
# En app.py, ejemplo de configuración

from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Configuración CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:5000"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

# Limitador de velocidad
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Configuración de tamaño máximo
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB

# Ruta segura
@app.route('/api/upload', methods=['POST'])
@limiter.limit("10 per hour")
def upload_file():
    # Lógica...
    pass
"""


if __name__ == '__main__':
    print("Ejemplos de uso del Analizador de Calendarios")
    print("=" * 50)
    print()
    
    # Descomenta el ejemplo que deseas ejecutar
    
    # example_1_process_pdf()
    # example_2_batch_process()
    # example_3_api_upload()
    # example_3_api_analyze()
    example_5_advanced_analysis()
    # example_6_create_test_calendar()
    # example_7_validate_formats()
    
    print("\n" + "=" * 50)
    print("Para ver más ejemplos, revisa los comentarios en este archivo")
