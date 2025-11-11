# 📊 Sched-Anal - Calendar Schedule Analyzer

**Aplicación para analizar calendarios de turnos desde PDF, Excel, CSV o texto**

[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)
[![React](https://img.shields.io/badge/React-18.2+-blue)](https://react.dev)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🎯 ¿Qué es?

**Sched-Anal** es una herramienta que te permite:

- 📤 **Cargar** calendarios en formato PDF, Excel, CSV o texto
- 📊 **Analizar** automáticamente la estructura de turnos
- 📈 **Visualizar** estadísticas y gráficos
- 📋 **Exportar** resultados en CSV o JSON
- 🎨 **Interfaz amigable** con soporte para múltiples archivos

---

## ✅ Características

### ✨ Formatos Soportados

| Formato | Ubicación | Estado |
|---------|-----------|--------|
| **PDF** | Backend (Flask) | ✅ |
| **Excel** (.xlsx, .xls) | Frontend (XLSX) | ✅ |
| **CSV** | Frontend (XLSX) | ✅ |
| **Texto** | Frontend | ✅ |

### 🔄 Flujo Completo

```
Usuario carga archivo
    ↓
Frontend valida
    ↓
Envía a Backend API
    ↓
Backend procesa (PDF) o Frontend procesa (Excel/CSV)
    ↓
Detecta estructura de calendario
    ↓
Muestra análisis y gráficos
    ↓
Usuario exporta resultados
```

---

## 🚀 Inicio Rápido

### Windows

**Lo más fácil - Haz doble clic en:**

```
start-all.bat
```

Espera 20 segundos y abre: http://localhost:3000

**Ver detalles en**: [WINDOWS_QUICKSTART.md](WINDOWS_QUICKSTART.md)

---

### Mac/Linux

**Terminal 1 - Backend:**
```bash
python app.py
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

Luego abre: http://localhost:3000

---

## 📋 Requisitos

- **Python 3.8+** - [python.org](https://python.org)
- **Node.js 16+** - [nodejs.org](https://nodejs.org)
- **Git** (opcional) - [git-scm.com](https://git-scm.com)

---

## 📦 Instalación

### 1. Clonar o descargar

```bash
git clone https://github.com/saldo27/sched-anal.git
cd sched-anal
```

### 2. Instalar dependencias Python

```bash
pip install -r requirements.txt
```

### 3. Instalar dependencias Node.js

```bash
npm install
```

---

## 🎮 Uso

### Opción 1: Script Todo en Uno (Windows)

```bash
start-all.bat
```

### Opción 2: Ejecución Manual

**Terminal 1 - Backend (Python):**
```bash
# Windows:
run-server.bat

# Mac/Linux:
python app.py
```

**Terminal 2 - Frontend (Node.js):**
```bash
npm run dev
```

### Opción 3: Scripts Alternativos

```bash
# Windows - Backend
run-server.bat
run-server.ps1    # PowerShell (colores)

# Windows - Frontend
run-frontend.bat
```

---

## 🌐 Acceso

- **Frontend**: http://localhost:3000
- **Backend**: http://127.0.0.1:5000
- **Health Check**: http://127.0.0.1:5000/health

---

## 📚 Documentación

### Para Empezar Rápido

- **[WINDOWS_QUICKSTART.md](WINDOWS_QUICKSTART.md)** - Guía para Windows
- **[QUICKSTART.md](QUICKSTART.md)** - Guía general 5 minutos
- **[PARA_TI.md](PARA_TI.md)** - Instrucciones específicas

### Guías Técnicas

- **[FILE_UPLOAD_GUIDE.md](FILE_UPLOAD_GUIDE.md)** - API endpoints
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Desarrollo técnico
- **[STATUS.md](STATUS.md)** - Estado del proyecto

### Solución de Problemas

- **[WINDOWS_FIX.md](WINDOWS_FIX.md)** - Problemas en Windows (5 soluciones)
- **[WATCHDOG_FIX.md](WATCHDOG_FIX.md)** - Error de watchdog/Flask
- **[PDF_FIX.md](PDF_FIX.md)** - Error de carga de PDF
- **[WINDOWS_RESOLUTION.md](WINDOWS_RESOLUTION.md)** - Resumen de resoluciones

### Información General

- **[START_HERE.md](START_HERE.md)** - Punto de entrada
- **[README.md](README.md)** - Este archivo
- **[NEXT_STEPS.md](NEXT_STEPS.md)** - Próximos pasos

---

## 🔧 API Endpoints

### GET /health
Verifica que el servidor está activo

```bash
curl http://127.0.0.1:5000/health
```

**Respuesta:**
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

---

### POST /api/upload
Carga y procesa un archivo

**Formato:** `multipart/form-data`

```bash
curl -F "file=@calendar.pdf" http://127.0.0.1:5000/api/upload
```

**Respuesta:**
```json
{
  "success": true,
  "filename": "calendar.pdf",
  "text": "...extracted text...",
  "structure": "detected_structure",
  "lines": 245
}
```

---

### POST /api/analyze
Analiza estructura de calendario

**Body:** JSON
```json
{
  "calendarText": "...",
  "startDate": "2025-12-22",
  "nameMapping": "..."
}
```

---

### POST /api/export
Exporta resultados

**Body:** JSON
```json
{
  "workers": [...],
  "format": "csv" // o "json"
}
```

---

## 💾 Archivos Principales

```
sched-anal/
├── 📁 src/                    # Frontend React (si existe)
│   └── CalendarAnalyzer.jsx   # Componente principal
│
├── 🐍 app.py                  # Backend Flask
├── 🐍 file_processor.py       # Procesador de archivos
│
├── ⚙️  package.json            # Dependencias Node.js
├── ⚙️  requirements.txt        # Dependencias Python
├── ⚙️  vite.config.js         # Configuración Vite
│
├── 🖥️  run-server.bat         # Ejecutar backend (Windows)
├── 🖥️  run-frontend.bat       # Ejecutar frontend (Windows)
├── 🖥️  start-all.bat          # Ejecutar todo (Windows)
├── 🖥️  run-server.ps1        # Ejecutar backend (PowerShell)
│
└── 📄 *.md                    # Documentación
    ├── WINDOWS_QUICKSTART.md
    ├── WINDOWS_FIX.md
    ├── FILE_UPLOAD_GUIDE.md
    └── ...más guías
```

---

## 🔌 Stack Tecnológico

### Backend
- **Framework**: Flask 2.3
- **API**: Flask-CORS para CORS
- **PDF**: pdfplumber
- **Excel**: openpyxl, pandas
- **CSV**: pandas

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite 4
- **Styling**: Tailwind CSS
- **Gráficos**: Recharts
- **Excel**: XLSX library

---

## 🐛 Solucionar Problemas

### Windows

Si tienes problemas en Windows, lee en orden:

1. **[PARA_TI.md](PARA_TI.md)** - Instrucciones específicas
2. **[WINDOWS_QUICKSTART.md](WINDOWS_QUICKSTART.md)** - Setup detallado
3. **[WINDOWS_FIX.md](WINDOWS_FIX.md)** - 5 soluciones diferentes

### General

- **Problemas de Flask**: Ver [WATCHDOG_FIX.md](WATCHDOG_FIX.md)
- **Problemas de PDF**: Ver [PDF_FIX.md](PDF_FIX.md)
- **Problemas de puerto**: `netstat -ano | findstr :5000` (Windows)
- **Problemas de módulos**: `pip install -r requirements.txt`

---

## 📊 Ejemplos de Uso

### Ejemplo 1: Cargar PDF

1. Abre http://localhost:3000
2. Haz clic en "📄 Cargar PDF"
3. Selecciona un PDF con calendario
4. Espera a que se procese
5. Ver resultados en la interfaz

### Ejemplo 2: Cargar Excel

1. Haz clic en "📊 Cargar Excel"
2. Selecciona un archivo `.xlsx`
3. Los datos se muestran automáticamente
4. Analiza en la tabla

### Ejemplo 3: Exportar Resultados

1. Después de analizar
2. Haz clic en "📥 Exportar"
3. Elige formato: CSV o JSON
4. Se descarga el archivo

---

## 🔄 Workflow Recomendado

### Desarrollo

```bash
# Terminal 1 - Backend con auto-reload
python app.py

# Terminal 2 - Frontend con hot-reload
npm run dev

# Abre navegador
http://localhost:3000

# Los cambios se reflejan automáticamente
```

### Producción

```bash
# Build frontend
npm run build

# Usar server WSGI en lugar de Flask debug
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📈 Estadísticas del Proyecto

| Métrica | Valor |
|---------|-------|
| **Líneas de código** | 3,000+ |
| **Documentación** | 2,000+ líneas |
| **Endpoints API** | 4 |
| **Formatos soportados** | 4 (PDF, Excel, CSV, Texto) |
| **Plataformas** | Windows, Mac, Linux |
| **Lenguajes** | Python, JavaScript, React |

---

## 🎯 Roadmap

### v1.0 (Actual)
- ✅ Carga de PDF, Excel, CSV
- ✅ Análisis básico de estructura
- ✅ Gráficos y visualización
- ✅ Exportar resultados

### v1.1 (Próximo)
- [ ] Autenticación de usuarios
- [ ] Base de datos para historial
- [ ] Comparación de períodos
- [ ] Exportar a PDF

### v2.0 (Futuro)
- [ ] API pública
- [ ] Aplicación móvil
- [ ] Integración con calendarios
- [ ] Notificaciones

---

## 📝 Licencia

MIT License - Ver [LICENSE](LICENSE)

---

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📞 Soporte

- 📖 Lee la documentación en `/docs`
- 🐛 Reporta bugs en GitHub Issues
- 💡 Sugiere mejoras en Discussions

---

## 🙏 Agradecimientos

- **Flask** - Backend web framework
- **React** - Frontend UI framework
- **pdfplumber** - PDF processing
- **Pandas** - Data manipulation
- **Vite** - Build tool
- **Tailwind CSS** - Styling

---

## 🔗 Enlaces

- **GitHub**: https://github.com/saldo27/sched-anal
- **Python**: https://python.org
- **Node.js**: https://nodejs.org
- **React**: https://react.dev
- **Flask**: https://flask.palletsprojects.com

---

## ✅ Quick Checklist

- [ ] Python 3.8+ instalado
- [ ] Node.js 16+ instalado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] npm packages instalados (`npm install`)
- [ ] Backend ejecutándose (`python app.py`)
- [ ] Frontend ejecutándose (`npm run dev`)
- [ ] Navegador abierto en http://localhost:3000
- [ ] ✅ ¡A disfrutar!

---

**Última actualización**: Noviembre 11, 2025

**Status**: ✅ Completamente Funcional

**Versión**: 1.0.0

---

**¡Gracias por usar Sched-Anal! 🚀**
