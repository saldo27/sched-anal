# 📚 Documentación - Índice de Archivos

## 🎯 Comienza Aquí

```
QUICKSTART.md          ← 👈 Comienza aquí (5 min de lectura)
    ↓
README.md              ← Descripción general del proyecto
    ↓
FILE_UPLOAD_GUIDE.md   ← Guía completa de carga y API
    ↓
DEVELOPMENT.md         ← Guía técnica de desarrollo
```

---

## 📖 Guías Completas

### Para Usuarios
- **QUICKSTART.md** - Instrucciones rápidas para empezar
- **README.md** - Descripción completa del proyecto

### Para Desarrolladores
- **DEVELOPMENT.md** - Configuración, instalación, testing
- **FILE_UPLOAD_GUIDE.md** - Especificación completa de API
- **examples.py** - Ejemplos de integración

### Para Seguimiento
- **CHANGELOG.md** - Cambios y nuevas características

---

## 🗂️ Estructura de Carpetas

```
📦 sched-anal/
│
├── 📄 Documentación
│   ├── README.md                  # Descripción general
│   ├── QUICKSTART.md             # Inicio rápido
│   ├── FILE_UPLOAD_GUIDE.md      # Guía de API
│   ├── DEVELOPMENT.md            # Guía de desarrollo
│   ├── CHANGELOG.md              # Cambios
│   └── INDEX.md                  # Este archivo
│
├── 🔧 Configuración
│   ├── package.json              # Node dependencies
│   ├── requirements.txt          # Python dependencies
│   ├── vite.config.js            # Vite config
│   ├── tailwind.config.js        # Tailwind config
│   ├── postcss.config.js         # PostCSS config
│   └── .gitignore               # Git ignore
│
├── 🎨 Frontend (React)
│   ├── index.html                # HTML
│   ├── main.jsx                  # React entry
│   ├── index.css                 # Styles
│   └── CalendarAnalyzer.jsx      # Main component
│
├── ⚙️ Backend (Python/Flask)
│   ├── app.py                    # Flask server
│   ├── file_processor.py         # File processing
│   ├── sched_analyzer.py         # Original analyzer
│   ├── examples.py               # Usage examples
│   └── test_file_processor.py    # Unit tests
│
└── 📊 Sample Files
    ├── test_calendar.pdf         # Sample PDF
    ├── sample_schedule.xlsx      # Sample Excel
    ├── results_test.csv          # Results example
    └── create_*.py              # Sample generators
```

---

## 🚀 Workflow Recomendado

### 1. Primera Vez
```
1. Lee: QUICKSTART.md (5 min)
2. Instala: pip install -r requirements.txt
3. Instala: npm install
4. Ejecuta: python app.py (Terminal 1)
5. Ejecuta: npm run dev (Terminal 2)
6. Abre: http://localhost:3000
```

### 2. Desarrollo
```
1. Lee: DEVELOPMENT.md
2. Modifica código
3. Tests: python -m unittest test_file_processor.py
4. Build: npm run build
```

### 3. Integración
```
1. Lee: FILE_UPLOAD_GUIDE.md
2. Revisa: examples.py
3. Implementa: Integración en tu sistema
```

---

## 🔍 Búsqueda Rápida

### "¿Cómo ...?"

| Pregunta | Respuesta |
|----------|-----------|
| ¿Empiezo desde cero? | → QUICKSTART.md |
| ¿Instalo todo? | → DEVELOPMENT.md |
| ¿Uso la API? | → FILE_UPLOAD_GUIDE.md |
| ¿Veo ejemplos? | → examples.py |
| ¿Tengo error? | → DEVELOPMENT.md (Troubleshooting) |
| ¿Qué cambió? | → CHANGELOG.md |

---

## 📞 Ayuda Rápida

### Errores Comunes

**"Port already in use"**
```bash
# Frontend
npm run dev -- --port 3001

# Backend
# Edita app.py, línea final:
# app.run(debug=True, host='0.0.0.0', port=5001)
```

**"Module not found"**
```bash
pip install -r requirements.txt
npm install
```

**"CORS error"**
```
- Verifica que Flask está corriendo en puerto 5000
- Verifica CORS en app.py
```

---

## 📝 Mapa de Características

```
🎯 Carga de Archivos
├── PDF ✅
├── Excel ✅
├── CSV ✅
└── Texto Manual ✅

📊 Análisis
├── Total Turnos ✅
├── Por Mes ✅
├── Fin de Semana ✅
└── Última Posición ✅

📈 Visualización
├── Gráficos ✅
├── Tablas ✅
├── Ordenamiento ✅
└── Filtros ✅

💾 Exportación
├── CSV ✅
└── JSON (API) ✅
```

---

## 🔧 Stack Tecnológico

**Frontend**
- React 18
- Vite
- Recharts (gráficos)
- Tailwind CSS
- Lucide React (iconos)
- XLSX (Excel)

**Backend**
- Flask 2.3+
- Flask-CORS
- Pandas
- pdfplumber (PDF)
- openpyxl (Excel)

---

## 📊 Archivos por Propósito

### Documentación (Lee estos)
- README.md
- QUICKSTART.md
- FILE_UPLOAD_GUIDE.md
- DEVELOPMENT.md
- CHANGELOG.md
- INDEX.md (este)

### Configuración (Edita si necesitas)
- package.json
- requirements.txt
- vite.config.js
- tailwind.config.js
- postcss.config.js

### Código (Modifica para mejorar)
- CalendarAnalyzer.jsx (frontend)
- app.py (backend API)
- file_processor.py (procesamiento)
- sched_analyzer.py (análisis)

### Testing (Ejecuta para validar)
- test_file_processor.py

### Ejemplos (Aprende de estos)
- examples.py
- create_*.py (generadores de datos)

---

## 🎓 Aprender Más

### Conceptos Clave

1. **Carga de Archivos**
   - Frontend: HTML input
   - Backend: Flask endpoint
   - Procesamiento: file_processor.py

2. **Análisis**
   - Parseo de texto
   - Estadísticas por trabajador
   - Análisis de fin de semana

3. **Visualización**
   - Gráficos con Recharts
   - Tablas dinámicas
   - Ordenamiento

4. **Exportación**
   - Generación de CSV
   - Download en cliente

---

## 📱 Plataformas Soportadas

- ✅ Desktop (Chrome, Firefox, Safari, Edge)
- ✅ Tablet (iPad, tablets Android)
- ✅ Mobile (responsive design)
- ✅ Backend: Linux, macOS, Windows

---

## 🚀 Deploy

Para desplegar en producción:

1. Lee: DEVELOPMENT.md (sección Docker/Production)
2. Build: `npm run build`
3. Server: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`
4. Serve: `npm install -g serve && serve -s dist`

---

## ✅ Checklist de Primer Uso

- [ ] Instalé Python dependencies: `pip install -r requirements.txt`
- [ ] Instalé Node dependencies: `npm install`
- [ ] Ejecuté backend: `python app.py`
- [ ] Ejecuté frontend: `npm run dev`
- [ ] Abrí http://localhost:3000
- [ ] Cargué un archivo de prueba
- [ ] Analicé el calendario
- [ ] Exporté resultados

---

**¿Todo configurado?** 🎉

¡Ahora estás listo para analizar calendarios de turnos!

Para más información, consulta los archivos de documentación listados arriba.

---

**Última actualización**: Nov 11, 2025
**Versión**: 1.0.0
