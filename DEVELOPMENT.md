# Development & Build Configuration Guide

## Estructura Completa

```
📦 sched-anal
 ┣ 📂 __pycache__
 ┣ 📄 README.md                 # Documentación principal
 ┣ 📄 FILE_UPLOAD_GUIDE.md      # Guía detallada de carga de archivos y API
 ┣ 📄 requirements.txt          # Dependencias Python
 ┣ 📄 package.json              # Dependencias Node.js
 ┣ 📄 index.html                # Página HTML
 ┣ 📄 index.css                 # Estilos globales
 ┣ 📄 main.jsx                  # Punto de entrada React
 ┣ 📄 vite.config.js            # Configuración Vite
 ┣ 📄 tailwind.config.js        # Configuración Tailwind
 ┣ 📄 postcss.config.js         # Configuración PostCSS
 ┣ 📄 CalendarAnalyzer.jsx      # Componente principal React (✨ ACTUALIZADO)
 ┣ 📄 app.py                    # Servidor Flask (✨ NUEVO)
 ┣ 📄 file_processor.py         # Procesador de archivos (✨ NUEVO)
 ┣ 📄 test_file_processor.py    # Tests unitarios (✨ NUEVO)
 ┣ 📄 sched_analyzer.py         # Analizador original
 ┣ 📄 create_sample_data.py
 ┣ 📄 create_multi_month_sample.py
 ┣ 📄 create_test_pdf.py
 └ 📄 results_test.csv
```

## Instalación Paso a Paso

### 1. Backend Setup (Python)

```bash
# En el directorio del proyecto
pip install -r requirements.txt

# Verificar que se instalaron correctamente
python -c "import pandas, pdfplumber, openpyxl, flask; print('✓ Backend OK')"
```

### 2. Frontend Setup (Node.js)

```bash
# Instalar dependencias
npm install

# Verificar instalación
npm list react react-dom recharts

# Verificación rápida
npm run build
```

## Ejecutar la Aplicación

### Opción A: Frontend Only (Sin Backend)

```bash
npm run dev
```

- Acceso: `http://localhost:3000`
- Funcionalidad: Carga de archivos, análisis local (sin procesamiento de PDF/Excel en servidor)

### Opción B: Full Stack (Recomendado)

**Terminal 1 - Backend:**
```bash
python app.py
# Output: Running on http://0.0.0.0:5000
```

**Terminal 2 - Frontend:**
```bash
npm run dev
# Output: VITE v4.x.x ready in xxx ms
#         ➜  Local:   http://localhost:3000
```

- Frontend accede a: `http://localhost:3000`
- Backend disponible en: `http://localhost:5000`
- Proxy automático: `/api/*` → `http://localhost:5000/api/*`

## Testing

### Tests Python
```bash
# Ejecutar tests
python -m pytest test_file_processor.py -v

# O con unittest
python -m unittest test_file_processor.py
```

### Tests JavaScript (próximamente)
```bash
# Ejecutar tests
npm test
```

## Build para Producción

### Frontend
```bash
# Compilar con optimizaciones
npm run build

# Verificar build
npm run preview
```

Salida en: `dist/`

### Backend
```bash
# Crear entorno production
pip install gunicorn

# Ejecutar con Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Configuración de Proxy (Vite)

El `vite.config.js` incluye proxy automático:

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:5000',
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, '/api')
  }
}
```

Esto permite que las llamadas desde React a `/api/upload` se redirijan a `http://localhost:5000/api/upload`

## Comandos Útiles

### Frontend

```bash
# Desarrollo
npm run dev

# Build
npm run build

# Preview de build
npm run preview

# Limpiar node_modules
rm -rf node_modules && npm install
```

### Backend

```bash
# Ejecutar servidor
python app.py

# Con hot-reload
pip install python-dotenv flask-debugtoolbar
python app.py

# Tests
python -m pytest test_file_processor.py -v --cov=file_processor
```

## Troubleshooting

### "CORS Error"
```
Solución: Verificar que Flask está corriendo en puerto 5000
y que está configurado: CORS(app) en app.py
```

### "Cannot find module 'xlsx'"
```
Solución: npm install
```

### "ModuleNotFoundError: No module named 'pdfplumber'"
```
Solución: pip install -r requirements.txt
```

### "Port already in use"
```
Frontend: npm run dev -- --port 3001
Backend: python app.py (cambia puerto en app.py)
```

## Variables de Entorno

Crear archivo `.env` en raíz:

```env
# Backend
FLASK_ENV=development
FLASK_DEBUG=1
MAX_CONTENT_LENGTH=52428800  # 50MB

# Frontend
VITE_API_URL=http://localhost:5000
```

Cargar en `app.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Docker (Opcional)

Crear `Dockerfile`:

```dockerfile
FROM node:18-alpine AS frontend
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
COPY --from=frontend /app/dist ./static

CMD ["python", "app.py"]
```

Ejecutar:
```bash
docker build -t sched-anal .
docker run -p 5000:5000 sched-anal
```

## Performance Tips

1. **Frontend**:
   - Usar `useMemo` para cálculos pesados ✓
   - Lazy loading de componentes
   - Code splitting con Vite

2. **Backend**:
   - Caché de archivos procesados
   - Limite de tamaño: 50MB
   - Compresión de respuestas

3. **General**:
   - CDN para librerías estáticas
   - Compresión gzip
   - Minificación

## Próximas Mejoras

- [ ] Tests e2e con Playwright
- [ ] Autenticación y autorización
- [ ] Almacenamiento en base de datos
- [ ] Websockets para actualizaciones en vivo
- [ ] Integración con CI/CD (GitHub Actions)
- [ ] Deployment automático

---

**Última actualización**: Nov 11, 2025
**Versión**: 1.0.0 con carga de archivos
