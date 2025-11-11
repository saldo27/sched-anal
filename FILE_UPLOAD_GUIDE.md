# 📊 Analizador de Calendarios de Turnos - Guía de Uso

## Características Nuevas

### 1. **Carga de Archivos PDF**
- Extrae automáticamente texto de archivos PDF
- Soporta calendarios en formato de tabla o texto
- Compatible con documentos de múltiples páginas

### 2. **Carga de Archivos Excel**
- Soporta formatos `.xlsx` y `.xls`
- Procesa datos directamente desde hojas de cálculo
- Maneja automáticamente el formato de celda a calendario

### 3. **Carga de Archivos CSV**
- Importa datos de archivos CSV
- Flexible con separadores

### 4. **Entrada Manual**
- Opción de pegar texto directamente
- Útil para calendarios copiados de sistemas internos

## Estructura del Proyecto

### Frontend (React)
```
CalendarAnalyzer.jsx
├── Carga de archivos (PDF, Excel, CSV)
├── Entrada de texto manual
├── Visualización de datos
├── Gráficos interactivos
└── Exportación de resultados
```

### Backend (Python/Flask)
```
app.py                    # API Flask
file_processor.py         # Procesamiento de archivos
requirements.txt          # Dependencias Python
```

## Instalación

### Backend
```bash
# Instalar dependencias Python
pip install -r requirements.txt

# Ejecutar servidor Flask
python app.py
```

El servidor estará disponible en `http://localhost:5000`

### Frontend
```bash
# Instalar dependencias Node.js
npm install

# Ejecutar servidor de desarrollo
npm run dev

# Compilar para producción
npm run build
```

## Endpoints API

### 1. Health Check
```
GET /health
```
Verifica que el servidor está funcionando.

**Respuesta:**
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

### 2. Cargar Archivo
```
POST /api/upload
Content-Type: multipart/form-data
```

**Parámetros:**
- `file`: Archivo (PDF, Excel o CSV)

**Respuesta:**
```json
{
  "success": true,
  "filename": "calendario.pdf",
  "text": "...",
  "structure": {
    "days_count": 30,
    "lines_per_week": 5,
    "detected_format": "week_based"
  },
  "lines": 150
}
```

**Códigos de error:**
- `400`: Archivo no válido o no proporcionado
- `413`: Archivo demasiado grande (máximo 50 MB)
- `500`: Error en el procesamiento

### 3. Analizar Calendario
```
POST /api/analyze
Content-Type: application/json
```

**Body:**
```json
{
  "calendarText": "...",
  "startDate": "2025-12-22",
  "nameMapping": "REQUE=LUIS R\nROBER=ROBERTO"
}
```

**Respuesta:**
```json
{
  "success": true,
  "structure": {
    "days_count": 30,
    "lines_per_week": 5,
    "detected_format": "week_based"
  },
  "textLength": 5000,
  "lines": 150
}
```

### 4. Exportar Resultados
```
POST /api/export
Content-Type: application/json
```

**Body:**
```json
{
  "workers": [
    {
      "name": "LUIS R",
      "total": 28,
      "friday": 4,
      "saturday": 4,
      "sunday": 4,
      "weekendPercentage": "42.8",
      "lastPosition": 7
    }
  ],
  "format": "csv"
}
```

**Respuesta (CSV):**
```json
{
  "success": true,
  "format": "csv",
  "content": "Trabajador,Total,Viernes,Sábado,Domingo,% Fin de Semana,Última Posición\n..."
}
```

## Formatos Soportados

### PDF
- Texto simple o basado en tablas
- Múltiples páginas
- Cualquier idioma

### Excel
- `.xlsx` (recomendado)
- `.xls` (legacy)
- Cualquier número de hojas

### CSV
- Separado por comas
- Una fila por línea de calendario

## Ejemplos de Uso

### Ejemplo 1: Cargar PDF
```javascript
const formData = new FormData();
formData.append('file', pdfFile);

const response = await fetch('/api/upload', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log(data.text); // Texto extraído
```

### Ejemplo 2: Analizar Calendario
```javascript
const response = await fetch('/api/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    calendarText: calendarText,
    startDate: '2025-12-22',
    nameMapping: 'REQUE=LUIS R\nROBER=ROBERTO'
  })
});

const data = await response.json();
console.log(data.structure);
```

### Ejemplo 3: Exportar Resultados
```javascript
const response = await fetch('/api/export', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    workers: sortedWorkers,
    format: 'csv'
  })
});

const data = await response.json();
console.log(data.content); // CSV content
```

## Limitaciones y Consideraciones

1. **Tamaño de archivo**: Máximo 50 MB
2. **Formatos PDF**: Funciona mejor con texto seleccionable
3. **Formatos Excel**: Optimizado para disposición de calendarios estándar
4. **Codificación**: Se recomienda UTF-8 para caracteres especiales

## Solución de Problemas

### Error: "Archivo no válido"
- Verifica que la extensión sea `.pdf`, `.xlsx`, `.xls` o `.csv`
- Comprueba que el archivo no esté corrupto

### Error: "Archivo demasiado grande"
- Reduce el tamaño del archivo
- Intenta dividir calendarios grandes en múltiples partes

### Error: "Texto no detectado (PDF)"
- El PDF puede tener texto como imagen
- Intenta copiar-pegar manualmente o usar OCR

### Parseo incorrecto
- Verifica el formato del calendario
- Asegúrate de que coincida con el formato esperado (5 líneas por semana)
- Ajusta la fecha de inicio si es necesario

## Próximas Mejoras

- [ ] Soporte para OCR en PDFs con texto de imagen
- [ ] Detección automática de formato de calendario
- [ ] Importación desde URL
- [ ] Sincronización con Google Calendar
- [ ] Análisis predictivo de equidad de turnos
- [ ] Historial de análisis

## Licencia

Este proyecto está bajo licencia MIT.
