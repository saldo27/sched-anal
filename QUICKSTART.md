# 🚀 Quick Start - Analizador de Calendarios de Turnos

## Inicio en 3 Pasos

### Paso 1: Instala Dependencias
```bash
# Instala Python dependencies
pip install -r requirements.txt

# Instala Node dependencies
npm install
```

### Paso 2: Inicia el Backend (Opcional pero Recomendado)
```bash
python app.py
# Output: Running on http://0.0.0.0:5000
```

### Paso 3: Inicia el Frontend
```bash
# En otra terminal
npm run dev
# Output: Local: http://localhost:3000
```

**¡Listo! Abre http://localhost:3000 en tu navegador**

---

## Uso Básico

### 1️⃣ Cargar Archivo
- **PDF**: Copia tu PDF del calendario
- **Excel**: Exporta tu calendario a .xlsx
- **CSV**: Convierte tu calendario a CSV
- **Texto**: Pega el texto directamente

### 2️⃣ Configurar
- **Fecha de inicio**: Cuando comienza el calendario
- **Mapeo de nombres**: Ej: REQUE=LUIS REQUENA

### 3️⃣ Analizar
- Click en "Analizar Calendario"
- Ver gráficos y estadísticas

### 4️⃣ Exportar
- Click en "Exportar CSV"
- Descargar resultados

---

## Comandos Útiles

```bash
# Frontend
npm run dev          # Modo desarrollo
npm run build        # Compilar para producción
npm run preview      # Ver build en local

# Backend
python app.py        # Ejecutar servidor
python -m unittest test_file_processor.py  # Tests
```

---

## Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| "Port 3000 in use" | `npm run dev -- --port 3001` |
| "Port 5000 in use" | Cambia puerto en `app.py` línea final |
| "No module named X" | `pip install -r requirements.txt` |
| "Cannot find module X" | `npm install` |
| CORS Error | Verifica que Flask esté corriendo |

---

## Formatos Soportados

✅ **PDF** - Calendarios en PDF (texto seleccionable)
✅ **Excel** - Archivos .xlsx y .xls
✅ **CSV** - Archivos separados por comas
✅ **Texto** - Entrada manual o pegada

---

## Características

📊 **Análisis Completo**
- Total de turnos
- Desglose por mes
- Análisis de fin de semana
- Última posición

📈 **Visualización**
- Gráficos interactivos
- Tablas ordenables
- Vista general y mensual

💾 **Exportación**
- Descarga en CSV
- Datos completos

---

## Próximos Pasos

1. Lee **FILE_UPLOAD_GUIDE.md** para detalles de API
2. Revisa **DEVELOPMENT.md** para configuración avanzada
3. Consulta **examples.py** para integración programática

---

## Soporte

- 📖 Documentación: README.md
- 🔌 API: FILE_UPLOAD_GUIDE.md  
- ⚙️ Desarrollo: DEVELOPMENT.md
- 💡 Ejemplos: examples.py
- 🧪 Tests: test_file_processor.py

---

**¿Problemas?** Abre un issue en GitHub
**¿Mejoras?** Envía un pull request

Happy analyzing! 🎉
