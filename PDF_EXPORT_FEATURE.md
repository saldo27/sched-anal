# Exportación a PDF - Documentación

## Descripción
Se ha agregado una nueva funcionalidad de exportación a PDF que permite descargar un documento completo con:
- **Sección 1: Resumen Global** - Tabla con todos los trabajadores y estadísticas generales
- **Sección 2: Desglose Mensual** - Tabla con distribución de turnos por mes para cada trabajador

## Cambios Realizados

### Backend (app.py)
1. **Instalación de dependencias:**
   - `reportlab` - Librería para generar PDFs

2. **Nuevo endpoint:** `/api/export`
   - Método: POST
   - Formatos soportados: csv, json, **pdf** (nuevo)
   - Entrada JSON:
     ```json
     {
       "workers": [...],
       "monthlyData": [...],
       "format": "pdf",
       "analysisPeriod": "Diciembre 2024 - Marzo 2025"
     }
     ```
   - Salida: Archivo PDF descargable

3. **Características del PDF:**
   - Encabezado con período de análisis y timestamp
   - Tabla global: Trabajador, Total, Viernes, Sábado, Domingo, % Fin de Semana, Última Posición
   - Salto de página automático
   - Tabla mensual: Trabajador + todos los meses con datos + Total
   - Estilos profesionales con colores coordinados
   - Fuentes legibles y bien formateadas

### Frontend (CalendarAnalyzer.jsx)
1. **Nueva función:** `handleExportPDF()`
   - Prepara datos mensuales en formato compatible
   - Envía petición POST a `/api/export`
   - Descarga automática del PDF generado
   - Nombre de archivo: `analisis_turnos_YYYYMMDD.pdf`

2. **Nuevo botón en interfaz:**
   - Color: Rojo (contraste con botón CSV verde)
   - Ícono: Download
   - Texto: "Exportar PDF"
   - Posición: Al lado del botón "Exportar CSV"

## Uso

1. Carga un archivo PDF o Excel con el calendario de turnos
2. Ingresa la fecha de inicio
3. Haz clic en "Analizar Calendario"
4. Se mostrarán los resultados
5. Haz clic en "Exportar PDF" para descargar el documento

## Detalles Técnicos

### Estructura del PDF
```
┌─────────────────────────────────────────┐
│  Análisis de Turnos - Período           │
│  Generado: 11/11/2025 12:07             │
│                                         │
│  1. Resumen Global                      │
│  ┌─────────────────────────────────┐    │
│  │ Trabajador │ Total │ Viernes... │    │
│  ├─────────────────────────────────┤    │
│  │ Data cells...                   │    │
│  └─────────────────────────────────┘    │
│                                         │
│  [Página 2]                             │
│  2. Desglose Mensual                    │
│  ┌─────────────────────────────────┐    │
│  │ Trabajador │ Dic │ Ene │ Feb... │    │
│  ├─────────────────────────────────┤    │
│  │ Data cells...                   │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

### Colores Utilizados
- Encabezado de tabla: `#374151` (gris oscuro)
- Fondo alterno: Blanco y `#f3f4f6` (gris claro)
- Borde: Negro
- Título: `#1f2937` (gris carbón)

### Tamaño de Página
- Formato: Carta (8.5" x 11")
- Márgenes: Automáticos (por defecto de reportlab)

## Testing

Para probar la funcionalidad:

1. Usar un archivo de prueba con múltiples trabajadores
2. Verificar que ambas tablas se generan correctamente
3. Confirmar que los meses mostrados son solo los que tienen datos
4. Validar que el PDF se descarga con el nombre correcto

## Mejoras Futuras Posibles

- [ ] Agregar logos o encabezado personalizado
- [ ] Exportar con gráficos incluidos
- [ ] Soporte para múltiples idiomas
- [ ] Personalización de colores
- [ ] Incluir filtros/búsqueda en la exportación
- [ ] Exportación a Excel (.xlsx) con estilos
